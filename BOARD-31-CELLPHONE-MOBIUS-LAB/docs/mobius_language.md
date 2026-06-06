# Mobius DSL — Language Reference
## BOARD-31-CELLPHONE-MOBIUS-LAB

Each line in a `.mobius` file is one equation. Comments start with `#`.

### Equation Types

| Keyword  | Syntax                                      | ERU Role                    |
|----------|---------------------------------------------|-----------------------------|
| `LIMIT`  | `lim(f, var, approach_val) = expected`      | Expected boundary behavior  |
| `DERIV`  | `d/dt(f, var) = rate`                       | Rate of change / variance   |
| `PIECE`  | `piece(condition, val_true, val_false)`     | Branching / threshold logic |
| `ASSERT` | `if(cond) when(trigger) then(action name)` | Compiler gate / test        |
| `INTEGRAL`| `integral(f, a, b) = area`                | Cumulative drift over range |

### Example

```
LIMIT:   lim(cpu_load, t, steady_state) = 0.45
DERIV:   d/dt(citizen_count, t)         = 3449
PIECE:   piece(severity == CRITICAL, open_case, log_only)
ASSERT:  if(token_in_url) when(browser_nav) then(fire_antibody BROWSER_TOKEN_IN_REFERRER)
```

### ASSERT Gates (Compiler)

The compiler converts `ASSERT` lines into executable Python tests:

```
if(CONDITION) when(TRIGGER) then(ACTION ANTIBODY_NAME)
```

- `CONDITION` — evaluated against event dict fields
- `TRIGGER`   — event type gate (`browser_nav`, `always`, `severity == X`)
- `ACTION`    — `fire_antibody`, `open_case`, `log_only`

### ERU Mapping

Each equation type maps to an ERU record:

| Kind     | Expected         | Actual            | Variance             |
|----------|-----------------|-------------------|----------------------|
| LIMIT    | convergence val  | observed boundary | delta from limit     |
| DERIV    | expected rate    | measured rate     | slope divergence     |
| PIECE    | correct branch   | branch taken      | condition mismatch   |
| ASSERT   | assertion passes | assertion result  | failure mode         |
