use crate::ast::Program;

pub fn emit(prog: &Program) -> String {
    let mut out = String::from("SAGCO MACHINE v0.1\n");
    out.push_str("---\n");
    for (i, brick) in prog.bricks.iter().enumerate() {
        let from = brick.route.from.path.join(".");
        let to   = brick.route.to.path.join(".");
        out.push_str(&format!("{:04X}  ROUTE  {} -> {}\n", i, from, to));
    }
    out
}
