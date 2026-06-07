use crate::cell::{Cell, Value};
use crate::graph::DependencyGraph;
use crate::registry::FuncRegistry;
use std::collections::HashMap;

pub struct Sheet {
    pub cells: HashMap<String, Cell>,
}

impl Sheet {
    pub fn new() -> Self {
        Sheet {
            cells: HashMap::new(),
        }
    }

    pub fn set(&mut self, addr: &str, formula: &str) {
        let cell = Cell::new(addr, formula);
        self.cells.insert(addr.to_string(), cell);
    }

    pub fn get(&self, addr: &str) -> Option<Value> {
        self.cells.get(addr).map(|c| c.value.clone())
    }

    pub fn dirty_cells(&self) -> Vec<String> {
        self.cells
            .values()
            .filter(|c| c.dirty)
            .map(|c| c.addr.clone())
            .collect()
    }

    /// Extract dependencies from a formula (find cell refs in it)
    pub fn extract_deps(formula: &str) -> Vec<String> {
        use crate::lexer::tokenize;
        use crate::token::Token;
        let tokens = match tokenize(formula) {
            Ok(t) => t,
            Err(_) => return vec![],
        };
        let mut deps = Vec::new();
        for st in tokens {
            match st.token {
                Token::CellRef(addr) => deps.push(addr),
                Token::RangeRef(from, to) => {
                    deps.extend(crate::evaluator::expand_range_addrs(&from, &to));
                }
                _ => {}
            }
        }
        deps
    }

    /// Recalculate all cells in topological order
    pub fn recalc(&mut self, registry: &FuncRegistry) {
        // First pass: resolve literal values and compute deps
        let addrs: Vec<String> = self.cells.keys().cloned().collect();
        for addr in &addrs {
            let cell = self.cells.get_mut(addr).unwrap();
            if !cell.is_formula() {
                if let Some(val) = cell.literal_value() {
                    cell.value = val;
                    cell.dirty = false;
                }
            } else {
                let deps = Sheet::extract_deps(&cell.formula);
                cell.deps = deps;
            }
        }

        // Build dependency graph
        let mut graph = DependencyGraph::new();
        for (addr, cell) in &self.cells {
            graph.set_deps(addr, cell.deps.clone());
        }

        let order = match graph.topo_sort() {
            Ok(o) => o,
            Err(e) => {
                // Mark all formula cells as circular error
                for cell in self.cells.values_mut() {
                    if cell.is_formula() {
                        cell.value = Value::Error(e.clone());
                        cell.dirty = false;
                    }
                }
                return;
            }
        };

        // Evaluate in order
        for addr in &order {
            if let Some(cell) = self.cells.get(addr) {
                if !cell.is_formula() {
                    continue;
                }
                let formula = cell.formula.clone();
                // Build a temporary sheet snapshot for evaluation
                let value = self.eval_formula(&formula, registry);
                if let Some(cell) = self.cells.get_mut(addr) {
                    cell.value = value;
                    cell.dirty = false;
                }
            }
        }
    }

    fn eval_formula(&self, formula: &str, registry: &FuncRegistry) -> Value {
        use crate::evaluator::Evaluator;
        use crate::parser::parse;

        match parse(formula) {
            Ok(ast) => {
                let evaluator = Evaluator::new(registry, self);
                evaluator.eval(&ast).unwrap_or_else(|e| Value::Error(e.to_string()))
            }
            Err(e) => Value::Error(format!("#PARSE! {}", e)),
        }
    }

    /// Parse a .sagco file format into a Sheet
    pub fn from_sagco(content: &str) -> Self {
        let mut sheet = Sheet::new();
        for line in content.lines() {
            let line = line.trim();
            if line.is_empty() || line.starts_with('#') {
                continue;
            }
            // Format: ADDR = VALUE
            if let Some(eq_pos) = line.find('=') {
                let addr = line[..eq_pos].trim().to_string();
                let value = line[eq_pos + 1..].trim().to_string();
                // If value starts with =, it's a formula
                let formula = if value.starts_with('=') {
                    value
                } else {
                    value
                };
                sheet.set(&addr, &formula);
            }
        }
        sheet
    }
}

impl Default for Sheet {
    fn default() -> Self {
        Self::new()
    }
}
