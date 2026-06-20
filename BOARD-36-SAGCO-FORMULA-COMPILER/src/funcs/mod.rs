pub mod builtin;
pub mod custom;
pub mod sagco_guard;

use crate::registry::FuncRegistry;

/// Wire all functions into the registry
pub fn register_all(registry: &mut FuncRegistry) {
    // Builtin functions
    registry.register("IF", builtin::func_if);
    registry.register("SUM", builtin::func_sum);
    registry.register("AVERAGE", builtin::func_average);
    registry.register("MIN", builtin::func_min);
    registry.register("MAX", builtin::func_max);
    registry.register("LEN", builtin::func_len);
    registry.register("CONCAT", builtin::func_concat);
    registry.register("AND", builtin::func_and);
    registry.register("OR", builtin::func_or);
    registry.register("NOT", builtin::func_not);
    registry.register("ABS", builtin::func_abs);
    registry.register("SQRT", builtin::func_sqrt);
    registry.register("ROUND", builtin::func_round);

    // Custom functions
    registry.register("MORSE", custom::func_morse);

    // SAGCO functions
    registry.register("SAGCO_SANITY", sagco_guard::func_sagco_sanity);
    registry.register("SAGCO_ERU", sagco_guard::func_sagco_eru);
    registry.register("SAGCO_GUARD", sagco_guard::func_sagco_guard);
    registry.register("SAGCO_UNITS", sagco_guard::func_sagco_units);
}
