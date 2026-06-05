/// Transform Layer 1: Linguistic
/// Maps English/Hebrew intents to AST with semantic meaning
/// Adds 'ראה' for observation, collapsing wave functions in simulations

use crate::parser::grammar::AstNode;

#[derive(Debug, Clone)]
pub struct LinguisticAst {
    pub nodes: Vec<SemanticNode>,
}

#[derive(Debug, Clone)]
pub enum SemanticNode {
    Intent { operation: String, semantic: String, params: Vec<SemanticNode> },
    HebrewOp { root: String, semantic: String, args: Vec<SemanticNode> },
    Literal(String),
    Identifier(String),
    Block(Vec<SemanticNode>),
}

pub fn transform(ast: Vec<AstNode>) -> Result<LinguisticAst, String> {
    let nodes = ast.into_iter()
        .map(|node| transform_node(node))
        .collect::<Result<Vec<_>, String>>()?;
    
    Ok(LinguisticAst { nodes })
}

fn transform_node(node: AstNode) -> Result<SemanticNode, String> {
    match node {
        AstNode::Intent { operation, params } => {
            let semantic = match operation.as_str() {
                "bounce" => "LQC_bounce_suppression",
                "suppress" => "mode_suppression",
                "observe" => "wavefunction_collapse",
                "unify" => "theory_unification",
                "fluctuate" => "quantum_fluctuation",
                _ => &operation,
            }.to_string();
            
            let transformed_params = params.into_iter()
                .map(transform_node)
                .collect::<Result<Vec<_>, String>>()?;
            
            Ok(SemanticNode::Intent { 
                operation, 
                semantic, 
                params: transformed_params 
            })
        }
        AstNode::HebrewOp { root, args } => {
            let semantic = match root.as_str() {
                "דחה" => "bounce_operator",      // Push away/bounce
                "כבש" => "suppress_operator",    // Suppress/subdue
                "ראה" => "observe_operator",     // See/observe
                "נוע" => "fluctuate_operator",   // Move/fluctuate
                "אחד" => "unify_operator",       // One/unify
                "פלא" => "anomaly_operator",     // Wonder/anomaly
                _ => "unknown_hebrew_op",
            }.to_string();
            
            let transformed_args = args.into_iter()
                .map(transform_node)
                .collect::<Result<Vec<_>, String>>()?;
            
            Ok(SemanticNode::HebrewOp { 
                root, 
                semantic, 
                args: transformed_args 
            })
        }
        AstNode::Literal(lit) => {
            let str_val = match lit {
                crate::parser::grammar::LiteralValue::Number(n) => n.to_string(),
                crate::parser::grammar::LiteralValue::String(s) => s,
            };
            Ok(SemanticNode::Literal(str_val))
        }
        AstNode::Identifier(id) => Ok(SemanticNode::Identifier(id)),
        AstNode::Block(statements) => {
            let transformed = statements.into_iter()
                .map(transform_node)
                .collect::<Result<Vec<_>, String>>()?;
            Ok(SemanticNode::Block(transformed))
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lexer::scanner::scan;
    use crate::parser::grammar::parse;

    #[test]
    fn test_linguistic_transform() {
        let source = "intent bounce";
        let tokens = scan(source).unwrap();
        let ast = parse(&tokens).unwrap();
        let ling_ast = transform(ast).unwrap();
        
        assert_eq!(ling_ast.nodes.len(), 1);
        match &ling_ast.nodes[0] {
            SemanticNode::Intent { semantic, .. } => {
                assert_eq!(semantic, "LQC_bounce_suppression");
            }
            _ => panic!("Expected Intent node"),
        }
    }
}
