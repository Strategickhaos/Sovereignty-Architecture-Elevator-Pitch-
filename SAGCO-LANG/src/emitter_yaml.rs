use crate::ast::Program;

pub fn emit(prog: &Program) -> String {
    let mut out = String::from("bricks:\n");
    for brick in &prog.bricks {
        out.push_str(&format!("  - name: {}\n", brick.name));
        out.push_str(&format!("    from: {}\n", brick.route.from.path.join(".")));
        out.push_str(&format!("    to:   {}\n", brick.route.to.path.join(".")));
    }
    out
}
