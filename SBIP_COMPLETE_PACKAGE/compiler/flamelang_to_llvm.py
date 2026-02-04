import llvmlite.ir as ir
import llvmlite.binding as llvm
import subprocess

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

def emit_ir(ops):
    module = ir.Module(name="flamelang")
    func_type = ir.FunctionType(ir.IntType(32), [])
    func = ir.Function(module, func_type, name="main")
    block = func.append_basic_block("entry")
    builder = ir.IRBuilder(block)
    result = ir.Constant(ir.IntType(32), 0)
    for op in ops:
        if op[0] == 'add':
            a = ir.Constant(ir.IntType(32), op[1])
            b = ir.Constant(ir.IntType(32), op[2])
            result = builder.add(a, b)
    builder.ret(result)
    return module

def optimize_and_compile(module):
    llvm_mod = llvm.parse_assembly(str(module))
    pm = llvm.create_module_pass_manager()
    pm.add_global_dce_pass()
    pm.add_aggressive_dce_pass()
    pm.add_loop_vectorize_pass()
    pm.add_instruction_combining_pass()
    pm.run(llvm_mod)
    target = llvm.Target.from_default_triple().create_target_machine(options="-O3 -mcpu=native")
    obj = target.emit_object(llvm_mod)
    with open("flamelang.o", "wb") as f:
        f.write(obj)
    subprocess.run(["ld", "flamelang.o", "-o", "flamelang_exec"])
    return "flamelang_exec"
