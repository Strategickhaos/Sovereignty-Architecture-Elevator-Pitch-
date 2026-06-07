use crate::mathml::node::MathNode::{self, *};

pub fn mtext(s: &str) -> MathNode { MText(s.into()) }
pub fn mi(s: &str)    -> MathNode { Mi(s.into()) }
pub fn mo(s: &str)    -> MathNode { Mo(s.into()) }
pub fn mn(s: &str)    -> MathNode { Mn(s.into()) }

pub fn mrow(children: Vec<MathNode>) -> MathNode { MRow(children) }

pub fn mfrac(num: MathNode, den: MathNode) -> MathNode {
    MFrac { num: Box::new(num), den: Box::new(den) }
}
pub fn msup(base: MathNode, sup: MathNode) -> MathNode {
    MSup { base: Box::new(base), sup: Box::new(sup) }
}
pub fn msub(base: MathNode, sub: MathNode) -> MathNode {
    MSub { base: Box::new(base), sub: Box::new(sub) }
}
pub fn munder(base: MathNode, under: MathNode) -> MathNode {
    MUnder { base: Box::new(base), under: Box::new(under) }
}
pub fn munderover(base: MathNode, under: MathNode, over: MathNode) -> MathNode {
    MUnderOver { base: Box::new(base), under: Box::new(under), over: Box::new(over) }
}

// Layout helpers — read like the math story in your head
pub fn section(label: &str, body: Vec<MathNode>) -> MathNode {
    let mut children = vec![mtext(label)];
    children.extend(body);
    MRow(children)
}

pub fn inequality_chain(terms: Vec<MathNode>) -> MathNode {
    // interleave < between terms
    let mut children = vec![];
    for (i, t) in terms.into_iter().enumerate() {
        if i > 0 { children.push(mo("<")); }
        children.push(t);
    }
    MRow(children)
}

pub fn lim_under(var: &str, approach: MathNode) -> MathNode {
    munder(mo("lim"), mrow(vec![mi(var), mo("\u{2192}"), approach]))
}

pub fn prime(f: &str) -> MathNode {
    msup(mi(f), mo("\u{2032}"))
}
pub fn double_prime(f: &str) -> MathNode {
    msup(mi(f), mo("\u{2033}"))
}
pub fn nth_deriv(f: &str, n: &str) -> MathNode {
    msup(mi(f), mn(n))
}
