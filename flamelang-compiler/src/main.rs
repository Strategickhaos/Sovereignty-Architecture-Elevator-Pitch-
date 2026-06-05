use std::env;
use std::fs::{read_to_string, File};
use std::io::Write;
use crate::lexer::scanner::scan;
use crate::parser::grammar::parse;

mod lexer { 
    pub mod scanner; 
}
mod parser { 
    pub mod grammar; 
}
mod transform {
    pub mod layer1_linguistic;
    pub mod layer2_hebrew;
    pub mod layer3_unicode;
    pub mod layer4_wave;
    pub mod layer5_dna_llvm;
    pub mod layer6_cmb;
    pub mod layer7_llvm;
}

#[derive(Debug)] 
pub enum FlameError { 
    Parse(String), 
    Transform(String), 
    Io(std::io::Error) 
}

impl From<std::io::Error> for FlameError { 
    fn from(e: std::io::Error) -> Self { 
        Self::Io(e) 
    } 
}

impl std::fmt::Display for FlameError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            FlameError::Parse(s) => write!(f, "Parse error: {}", s),
            FlameError::Transform(s) => write!(f, "Transform error: {}", s),
            FlameError::Io(e) => write!(f, "IO error: {}", e),
        }
    }
}

impl std::error::Error for FlameError {}

fn main() -> Result<(), FlameError> {
    let args: Vec<_> = env::args().collect();
    if args.len() != 3 { 
        eprintln!("Usage: flamec <in.flame> <out.ll>"); 
        std::process::exit(1); 
    }

    let source = read_to_string(&args[1])?;
    let tokens = scan(&source).map_err(FlameError::Parse)?;
    let ast = parse(&tokens).map_err(FlameError::Parse)?;

    // Apply 7-layer transform pipeline
    let ling_ast = transform::layer1_linguistic::transform(ast)
        .map_err(FlameError::Transform)?;
    let heb_ast = transform::layer2_hebrew::transform(ling_ast)
        .map_err(FlameError::Transform)?;
    let uni_ast = transform::layer3_unicode::transform(heb_ast)
        .map_err(FlameError::Transform)?;
    let wave_ast = transform::layer4_wave::transform(uni_ast)
        .map_err(FlameError::Transform)?;
    let dna_ast = transform::layer5_dna_llvm::transform(wave_ast)
        .map_err(FlameError::Transform)?;
    let cmb_ast = transform::layer6_cmb::cmb_transform(dna_ast)
        .map_err(FlameError::Transform)?;
    let llvm_ir = transform::layer7_llvm::llvm_opt_transform(cmb_ast)
        .map_err(FlameError::Transform)?;

    let mut file = File::create(&args[2])?;
    file.write_all(llvm_ir.as_bytes())?;

    println!("Successfully compiled {} to {}", args[1], args[2]);
    Ok(())
}
