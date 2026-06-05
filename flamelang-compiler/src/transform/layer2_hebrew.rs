/// Transform Layer 2: Hebrew
/// Applies Hebrew roots as operators for quantum/CMB operations
/// e.g., 'דחה' for bounce: multiply spectrum by exp(-l/τ_bounce)

use crate::transform::layer1_linguistic::{LinguisticAst, SemanticNode};

#[derive(Debug, Clone)]
pub struct HebrewAst {
    pub operations: Vec<HebrewOperation>,
}

#[derive(Debug, Clone)]
pub enum HebrewOperation {
    Bounce { tau: f64 },           // exp(-l/τ)
    Suppress { mode: String, factor: f64 },
    Observe { collapse: bool },
    Fluctuate { amplitude: f64 },
    Unify { theories: Vec<String> },
    Anomaly { asymmetry: f64 },
    Generic { op: String, params: Vec<String> },
}

pub fn transform(ling_ast: LinguisticAst) -> Result<HebrewAst, String> {
    let operations = ling_ast.nodes.into_iter()
        .map(|node| transform_semantic_node(node))
        .collect::<Result<Vec<_>, String>>()?;
    
    Ok(HebrewAst { operations })
}

fn transform_semantic_node(node: SemanticNode) -> Result<HebrewOperation, String> {
    match node {
        SemanticNode::Intent { semantic, params, .. } => {
            match semantic.as_str() {
                "LQC_bounce_suppression" => {
                    // Default tau for bounce suppression
                    let tau = extract_numeric_param(&params, 0.065);
                    Ok(HebrewOperation::Bounce { tau })
                }
                "mode_suppression" => {
                    let mode = extract_string_param(&params, "B-mode");
                    let factor = extract_numeric_param(&params, 0.15);
                    Ok(HebrewOperation::Suppress { mode, factor })
                }
                "wavefunction_collapse" => {
                    Ok(HebrewOperation::Observe { collapse: true })
                }
                "quantum_fluctuation" => {
                    let amplitude = extract_numeric_param(&params, 1e-5);
                    Ok(HebrewOperation::Fluctuate { amplitude })
                }
                "theory_unification" => {
                    let theories = vec!["LQC".to_string(), "String".to_string()];
                    Ok(HebrewOperation::Unify { theories })
                }
                _ => {
                    Ok(HebrewOperation::Generic { 
                        op: semantic, 
                        params: vec![] 
                    })
                }
            }
        }
        SemanticNode::HebrewOp { semantic, args, .. } => {
            match semantic.as_str() {
                "bounce_operator" => {
                    let tau = extract_numeric_from_args(&args, 0.065);
                    Ok(HebrewOperation::Bounce { tau })
                }
                "suppress_operator" => {
                    let mode = extract_string_from_args(&args, "B-mode");
                    let factor = extract_numeric_from_args(&args, 0.15);
                    Ok(HebrewOperation::Suppress { mode, factor })
                }
                "observe_operator" => {
                    Ok(HebrewOperation::Observe { collapse: true })
                }
                "fluctuate_operator" => {
                    let amplitude = extract_numeric_from_args(&args, 1e-5);
                    Ok(HebrewOperation::Fluctuate { amplitude })
                }
                "unify_operator" => {
                    let theories = vec!["LQC".to_string(), "String".to_string()];
                    Ok(HebrewOperation::Unify { theories })
                }
                "anomaly_operator" => {
                    let asymmetry = extract_numeric_from_args(&args, 0.1);
                    Ok(HebrewOperation::Anomaly { asymmetry })
                }
                _ => {
                    Ok(HebrewOperation::Generic { 
                        op: semantic, 
                        params: vec![] 
                    })
                }
            }
        }
        SemanticNode::Block(nodes) => {
            // Transform first node in block
            if let Some(first) = nodes.into_iter().next() {
                transform_semantic_node(first)
            } else {
                Ok(HebrewOperation::Generic { 
                    op: "empty_block".to_string(), 
                    params: vec![] 
                })
            }
        }
        _ => {
            Ok(HebrewOperation::Generic { 
                op: "literal".to_string(), 
                params: vec![] 
            })
        }
    }
}

fn extract_numeric_param(params: &[SemanticNode], default: f64) -> f64 {
    params.first()
        .and_then(|p| {
            if let SemanticNode::Literal(s) = p {
                s.parse::<f64>().ok()
            } else {
                None
            }
        })
        .unwrap_or(default)
}

fn extract_string_param(params: &[SemanticNode], default: &str) -> String {
    params.first()
        .and_then(|p| {
            if let SemanticNode::Literal(s) = p {
                Some(s.clone())
            } else if let SemanticNode::Identifier(s) = p {
                Some(s.clone())
            } else {
                None
            }
        })
        .unwrap_or_else(|| default.to_string())
}

fn extract_numeric_from_args(args: &[SemanticNode], default: f64) -> f64 {
    extract_numeric_param(args, default)
}

fn extract_string_from_args(args: &[SemanticNode], default: &str) -> String {
    extract_string_param(args, default)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bounce_operation() {
        let ling_ast = LinguisticAst {
            nodes: vec![SemanticNode::Intent {
                operation: "bounce".to_string(),
                semantic: "LQC_bounce_suppression".to_string(),
                params: vec![],
            }],
        };
        
        let heb_ast = transform(ling_ast).unwrap();
        assert_eq!(heb_ast.operations.len(), 1);
        match &heb_ast.operations[0] {
            HebrewOperation::Bounce { tau } => {
                assert!((tau - 0.065).abs() < 1e-6);
            }
            _ => panic!("Expected Bounce operation"),
        }
    }
}
