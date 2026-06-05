//! LLVM Backend for FlameLang

use inkwell::context::Context;
use inkwell::module::Module;
use inkwell::builder::Builder;
use inkwell::values::{FunctionValue, BasicValueEnum};
use inkwell::types::{BasicTypeEnum, BasicMetadataTypeEnum};
use inkwell::targets::{Target, TargetMachine, RelocMode, CodeModel, FileType, InitializationConfig};
use inkwell::OptimizationLevel;
use std::path::Path;

use crate::ir::*;
use crate::{FlameResult, FlameError};

pub struct LLVMBackend<'ctx> {
    context: &'ctx Context,
    module: Module<'ctx>,
    builder: Builder<'ctx>,
}

impl<'ctx> LLVMBackend<'ctx> {
    pub fn new(context: &'ctx Context, module_name: &str) -> Self {
        let module = context.create_module(module_name);
        let builder = context.create_builder();
        
        Self {
            context,
            module,
            builder,
        }
    }
    
    /// Emit LLVM IR for the entire module
    pub fn emit_module(&mut self, ir: &FlameIR) -> FlameResult<()> {
        // Emit all functions
        for func in &ir.functions {
            self.emit_function(func)?;
        }
        
        Ok(())
    }
    
    /// Emit a single function
    fn emit_function(&mut self, func: &FlameFunction) -> FlameResult<FunctionValue<'ctx>> {
        // Build parameter types
        let param_types: Vec<BasicMetadataTypeEnum> = func.params.iter()
            .map(|p| self.flame_type_to_llvm(&p.param_type).into())
            .collect();
        
        // Build function type
        let fn_type = match &func.return_type {
            FlameType::Void => self.context.void_type().fn_type(&param_types, false),
            FlameType::I32 => self.context.i32_type().fn_type(&param_types, false),
            FlameType::I64 => self.context.i64_type().fn_type(&param_types, false),
            FlameType::F64 => self.context.f64_type().fn_type(&param_types, false),
            _ => self.context.i32_type().fn_type(&param_types, false),
        };
        
        // Create function
        let function = self.module.add_function(&func.name, fn_type, None);
        let basic_block = self.context.append_basic_block(function, "entry");
        self.builder.position_at_end(basic_block);
        
        // Emit function body
        let mut return_value = None;
        for expr in &func.body {
            let val = self.emit_expr(expr)?;
            if matches!(expr, FlameExpr::Return(_)) {
                return_value = Some(val);
            }
        }
        
        // Add return
        match &func.return_type {
            FlameType::Void => {
                self.builder.build_return(None);
            }
            FlameType::I32 | FlameType::I64 | FlameType::F64 | FlameType::Bool => {
                if let Some(ret_val) = return_value {
                    self.builder.build_return(Some(&ret_val));
                } else {
                    // Default return value
                    let zero = self.context.i32_type().const_int(0, false);
                    self.builder.build_return(Some(&zero));
                }
            }
            _ => {
                let zero = self.context.i32_type().const_int(0, false);
                self.builder.build_return(Some(&zero));
            }
        }
        
        Ok(function)
    }
    
    /// Emit an expression
    fn emit_expr(&mut self, expr: &FlameExpr) -> FlameResult<BasicValueEnum<'ctx>> {
        match expr {
            FlameExpr::Constant(val) => self.emit_constant(val),
            FlameExpr::BinaryOp { op, left, right } => {
                let lhs = self.emit_expr(left)?;
                let rhs = self.emit_expr(right)?;
                self.emit_binary_op(*op, lhs, rhs)
            }
            FlameExpr::UnaryOp { op, operand } => {
                let val = self.emit_expr(operand)?;
                self.emit_unary_op(*op, val)
            }
            FlameExpr::Call { function, args } => {
                self.emit_call(function, args)
            }
            FlameExpr::Variable(_name) => {
                // Simplified: return a default value
                Ok(self.context.i32_type().const_int(0, false).into())
            }
            FlameExpr::Return(val) => {
                self.emit_expr(val)
            }
        }
    }
    
    /// Emit a constant value
    fn emit_constant(&self, val: &FlameValue) -> FlameResult<BasicValueEnum<'ctx>> {
        match val {
            FlameValue::Integer(n) => {
                Ok(self.context.i64_type().const_int(*n as u64, true).into())
            }
            FlameValue::Float(f) => {
                Ok(self.context.f64_type().const_float(*f).into())
            }
            FlameValue::Boolean(b) => {
                Ok(self.context.bool_type().const_int(*b as u64, false).into())
            }
            FlameValue::String(_) | FlameValue::Codon(_) => {
                // Simplified: return 0
                Ok(self.context.i32_type().const_int(0, false).into())
            }
        }
    }
    
    /// Emit binary operation
    fn emit_binary_op(&mut self, op: FlameOp, lhs: BasicValueEnum<'ctx>, rhs: BasicValueEnum<'ctx>) -> FlameResult<BasicValueEnum<'ctx>> {
        match (lhs, rhs) {
            (BasicValueEnum::IntValue(l), BasicValueEnum::IntValue(r)) => {
                let result = match op {
                    FlameOp::Add => self.builder.build_int_add(l, r, "add"),
                    FlameOp::Sub => self.builder.build_int_sub(l, r, "sub"),
                    FlameOp::Mul => self.builder.build_int_mul(l, r, "mul"),
                    FlameOp::Div => self.builder.build_int_signed_div(l, r, "div"),
                    FlameOp::Mod => self.builder.build_int_signed_rem(l, r, "mod"),
                    _ => l, // Simplified
                };
                Ok(result.into())
            }
            (BasicValueEnum::FloatValue(l), BasicValueEnum::FloatValue(r)) => {
                let result = match op {
                    FlameOp::Add => self.builder.build_float_add(l, r, "fadd"),
                    FlameOp::Sub => self.builder.build_float_sub(l, r, "fsub"),
                    FlameOp::Mul => self.builder.build_float_mul(l, r, "fmul"),
                    FlameOp::Div => self.builder.build_float_div(l, r, "fdiv"),
                    _ => l, // Simplified
                };
                Ok(result.into())
            }
            _ => {
                // Type mismatch, return lhs
                Ok(lhs)
            }
        }
    }
    
    /// Emit unary operation
    fn emit_unary_op(&mut self, op: FlameOp, val: BasicValueEnum<'ctx>) -> FlameResult<BasicValueEnum<'ctx>> {
        match val {
            BasicValueEnum::IntValue(i) => {
                let result = match op {
                    FlameOp::Sub => self.builder.build_int_neg(i, "neg"),
                    _ => i,
                };
                Ok(result.into())
            }
            BasicValueEnum::FloatValue(f) => {
                let result = match op {
                    FlameOp::Sub => self.builder.build_float_neg(f, "fneg"),
                    _ => f,
                };
                Ok(result.into())
            }
            _ => Ok(val),
        }
    }
    
    /// Emit function call
    fn emit_call(&mut self, function: &str, args: &[FlameExpr]) -> FlameResult<BasicValueEnum<'ctx>> {
        // Emit arguments
        let arg_values: Result<Vec<_>, _> = args.iter()
            .map(|arg| self.emit_expr(arg))
            .collect();
        let arg_values = arg_values?;
        
        // For intrinsic functions
        match function {
            "sin" | "cos" | "tan" => {
                if let Some(arg) = arg_values.first() {
                    // Simplified: just return the argument
                    Ok(*arg)
                } else {
                    Ok(self.context.f64_type().const_float(0.0).into())
                }
            }
            "bend" | "codon" | "perm" | "frequency" | "gematria" => {
                // FlameLang-specific operations (simplified)
                if let Some(arg) = arg_values.first() {
                    Ok(*arg)
                } else {
                    Ok(self.context.i32_type().const_int(0, false).into())
                }
            }
            _ => {
                // Try to find the function in the module
                if let Some(func) = self.module.get_function(function) {
                    let args_as_basic: Vec<_> = arg_values.iter()
                        .map(|v| (*v).into())
                        .collect();
                    
                    let call_site = self.builder.build_call(func, &args_as_basic, "call");
                    
                    if let Some(result) = call_site.try_as_basic_value().left() {
                        Ok(result)
                    } else {
                        Ok(self.context.i32_type().const_int(0, false).into())
                    }
                } else {
                    // Function not found, return 0
                    Ok(self.context.i32_type().const_int(0, false).into())
                }
            }
        }
    }
    
    /// Convert FlameType to LLVM BasicTypeEnum
    fn flame_type_to_llvm(&self, ty: &FlameType) -> BasicTypeEnum<'ctx> {
        match ty {
            FlameType::I32 => self.context.i32_type().into(),
            FlameType::I64 => self.context.i64_type().into(),
            FlameType::F64 => self.context.f64_type().into(),
            FlameType::Bool => self.context.bool_type().into(),
            FlameType::String => self.context.i8_type().ptr_type(inkwell::AddressSpace::default()).into(),
            FlameType::Codon => {
                // [u8; 3] as array
                self.context.i8_type().array_type(3).into()
            }
            FlameType::Array(inner, size) => {
                let inner_type = self.flame_type_to_llvm(inner);
                // Use BasicType trait method
                match inner_type {
                    BasicTypeEnum::ArrayType(t) => t.array_type(*size as u32).into(),
                    BasicTypeEnum::FloatType(t) => t.array_type(*size as u32).into(),
                    BasicTypeEnum::IntType(t) => t.array_type(*size as u32).into(),
                    BasicTypeEnum::PointerType(t) => t.array_type(*size as u32).into(),
                    BasicTypeEnum::StructType(t) => t.array_type(*size as u32).into(),
                    BasicTypeEnum::VectorType(t) => t.array_type(*size as u32).into(),
                }
            }
            FlameType::Void => self.context.i32_type().into(), // Fallback
        }
    }
    
    /// Write object file
    pub fn write_object(&self, path: &str) -> FlameResult<()> {
        // Initialize target
        Target::initialize_native(&InitializationConfig::default())
            .map_err(|e| FlameError::BackendError(format!("Failed to initialize target: {}", e)))?;
        
        let target_triple = TargetMachine::get_default_triple();
        let target = Target::from_triple(&target_triple)
            .map_err(|e| FlameError::BackendError(format!("Failed to create target: {}", e)))?;
        
        let target_machine = target.create_target_machine(
            &target_triple,
            "generic",
            "",
            OptimizationLevel::Default,
            RelocMode::Default,
            CodeModel::Default,
        ).ok_or_else(|| FlameError::BackendError("Failed to create target machine".to_string()))?;
        
        // Write object file
        target_machine.write_to_file(&self.module, FileType::Object, Path::new(path))
            .map_err(|e| FlameError::BackendError(format!("Failed to write object file: {}", e)))?;
        
        Ok(())
    }
    
    /// Get LLVM IR as string (for debugging)
    pub fn print_ir(&self) -> String {
        self.module.print_to_string().to_string()
    }
}
