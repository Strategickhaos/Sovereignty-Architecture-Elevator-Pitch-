use crate::mathml::builders::*;
use crate::mathml::node::MathNode;

// Chain rule template: d/dt[u^n] = n*u^(n-1)*u'
pub fn chain_rule_power(u_label: &str, n: &str, _uprime_label: &str) -> MathNode {
    let exp = n.parse::<i32>()
        .map(|x| (x - 1).to_string())
        .unwrap_or_else(|_| "n-1".into());
    MathNode::Math(vec![
        mrow(vec![
            msup(mi(u_label), mn(n)),
            mo("\u{2192}"),
            mn(n),
            mo("\u{22C5}"),
            msup(mi(u_label), mn(&exp)),
            mo("\u{22C5}"),
            msup(mi(u_label), mo("\u{2032}")),
        ]),
    ])
}
