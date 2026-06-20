use super::{PassResult, Pipeline};
use crate::sheet::Sheet;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EruEntry {
    pub cell: String,
    pub expected: String,
    pub actual: String,
    pub variance: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EruReport {
    pub entries: Vec<EruEntry>,
    pub total_cells: usize,
    pub evaluated: usize,
    pub errors: usize,
    pub open_variances: usize,
}

impl EruReport {
    pub fn new() -> Self {
        EruReport {
            entries: Vec::new(),
            total_cells: 0,
            evaluated: 0,
            errors: 0,
            open_variances: 0,
        }
    }

    pub fn to_yaml(&self) -> String {
        serde_yaml::to_string(self).unwrap_or_else(|_| "# ERU report serialization error".to_string())
    }
}

impl Default for EruReport {
    fn default() -> Self {
        Self::new()
    }
}

pub struct EruPass;

impl EruPass {
    pub fn build_report(sheet: &Sheet) -> EruReport {
        let mut report = EruReport::new();
        report.total_cells = sheet.cells.len();

        let mut addrs: Vec<String> = sheet.cells.keys().cloned().collect();
        addrs.sort();

        for addr in addrs {
            let cell = &sheet.cells[&addr];
            report.evaluated += 1;

            let expected = if cell.is_formula() {
                "evaluated".to_string()
            } else {
                "literal".to_string()
            };

            let actual = cell.value.as_str();
            let variance = if cell.value.is_error() {
                report.errors += 1;
                report.open_variances += 1;
                "OPEN_VARIANCE".to_string()
            } else {
                "VARIANCE_0".to_string()
            };

            report.entries.push(EruEntry {
                cell: addr.clone(),
                expected,
                actual,
                variance,
            });
        }

        report
    }
}

impl Pipeline for EruPass {
    fn run(&self, sheet: &mut Sheet) -> PassResult {
        let mut result = PassResult::new("EruPass");
        let report = EruPass::build_report(sheet);

        if report.errors > 0 {
            result.add_error(format!(
                "{} cell(s) evaluated with errors (OPEN_VARIANCE)",
                report.errors
            ));
        }

        result.add_warning(format!(
            "ERU Summary: {}/{} cells evaluated, {} errors, {} open variances",
            report.evaluated, report.total_cells, report.errors, report.open_variances
        ));

        result
    }
}
