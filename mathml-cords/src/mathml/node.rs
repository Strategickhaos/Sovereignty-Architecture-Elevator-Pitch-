#[derive(Debug, Clone)]
pub enum MathNode {
    Math(Vec<MathNode>),
    MRow(Vec<MathNode>),
    MText(String),
    Mi(String),
    Mo(String),
    Mn(String),
    MFrac { num: Box<MathNode>, den: Box<MathNode> },
    MSup { base: Box<MathNode>, sup: Box<MathNode> },
    MSub { base: Box<MathNode>, sub: Box<MathNode> },
    MUnder { base: Box<MathNode>, under: Box<MathNode> },
    MUnderOver { base: Box<MathNode>, under: Box<MathNode>, over: Box<MathNode> },
}
