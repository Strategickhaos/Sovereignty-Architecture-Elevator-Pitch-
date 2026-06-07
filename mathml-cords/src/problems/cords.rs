use crate::mathml::builders::*;
use crate::mathml::node::MathNode;

pub fn cords_explanation() -> MathNode {
    MathNode::Math(vec![
        mtext("To determine the correct order of the cables, we compute the derivatives:"),

        section("Red Cord: ", vec![
            prime("f"),
            mrow(vec![mo("("), mi("c"), mo(")")]),
            mo("="),
            mfrac(mn("1"), mi("c")),
        ]),

        section("Blue Cord: ", vec![
            double_prime("f"),
            mrow(vec![mo("("), mi("c"), mo(")")]),
            mo("="),
            mo("\u{2212}"),
            mfrac(mn("1"), msup(mi("c"), mn("2"))),
        ]),

        section("Green Cord: ", vec![
            nth_deriv("g", "8"),
            mrow(vec![mo("("), mn("3"), mi("\u{03C0}"), mo(")")]),
            mo("="),
            mn("0"),
        ]),

        mrow(vec![
            mtext("Since "),
            inequality_chain(vec![
                mrow(vec![mo("\u{2212}"), mfrac(mn("1"), msup(mi("c"), mn("2")))]),
                mn("0"),
                mfrac(mn("1"), mi("c")),
            ]),
            mtext(", the order smallest\u{2192}largest is: Blue, Green, Red Cord."),
        ]),
    ])
}

// Gate 4 — degree comparison limits
pub fn gate4_limits() -> MathNode {
    MathNode::Math(vec![
        mrow(vec![
            lim_under("x", MathNode::Mo("\u{221E}".into())),
            mfrac(
                mrow(vec![mi("a"), msup(mi("x"), mn("99")), mo("+"), mo("\u{22EF}")]),
                mrow(vec![mi("c"), msup(mi("x"), mn("99")), mo("+"), mo("\u{22EF}")]),
            ),
            mo("="),
            mfrac(mi("a"), mi("c")),
        ]),
        mrow(vec![
            lim_under("x", MathNode::Mo("\u{221E}".into())),
            mfrac(
                mrow(vec![mi("a"), msup(mi("x"), mn("99")), mo("+"), mo("\u{22EF}")]),
                mrow(vec![mi("c"), msup(mi("x"), mn("96")), mo("+"), mo("\u{22EF}")]),
            ),
            mo("="),
            mo("+\u{221E}"),
        ]),
        mrow(vec![
            lim_under("x", MathNode::Mo("\u{221E}".into())),
            mfrac(
                mrow(vec![mi("a"), msup(mi("x"), mn("96")), mo("+"), mo("\u{22EF}")]),
                mrow(vec![mi("c"), msup(mi("x"), mn("99")), mo("+"), mo("\u{22EF}")]),
            ),
            mo("="),
            mn("0"),
        ]),
    ])
}
