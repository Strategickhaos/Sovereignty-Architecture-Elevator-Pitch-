use crate::mathml::node::MathNode;

pub fn render(node: &MathNode) -> String {
    match node {
        MathNode::Math(ch) => format!(
            "<math xmlns=\"http://www.w3.org/1998/Math/MathML\">{}</math>",
            ch.iter().map(render).collect::<String>()
        ),
        MathNode::MRow(ch) => format!(
            "<mrow>{}</mrow>",
            ch.iter().map(render).collect::<String>()
        ),
        MathNode::MText(s) => format!("<mtext>{s}</mtext>"),
        MathNode::Mi(s)    => format!("<mi>{s}</mi>"),
        MathNode::Mo(s)    => format!("<mo>{s}</mo>"),
        MathNode::Mn(s)    => format!("<mn>{s}</mn>"),
        MathNode::MFrac { num, den } =>
            format!("<mfrac>{}{}</mfrac>", render(num), render(den)),
        MathNode::MSup { base, sup } =>
            format!("<msup>{}{}</msup>", render(base), render(sup)),
        MathNode::MSub { base, sub } =>
            format!("<msub>{}{}</msub>", render(base), render(sub)),
        MathNode::MUnder { base, under } =>
            format!("<munder>{}{}</munder>", render(base), render(under)),
        MathNode::MUnderOver { base, under, over } =>
            format!("<munderover>{}{}{}</munderover>", render(base), render(under), render(over)),
    }
}

pub fn render_pretty(node: &MathNode, indent: usize) -> String {
    let pad = " ".repeat(indent * 2);
    match node {
        MathNode::Math(ch) => format!(
            "{pad}<math xmlns=\"http://www.w3.org/1998/Math/MathML\">\n{}{pad}</math>",
            ch.iter().map(|c| render_pretty(c, indent + 1)).collect::<String>(),
        ),
        MathNode::MRow(ch) => format!(
            "{pad}<mrow>\n{}{pad}</mrow>\n",
            ch.iter().map(|c| render_pretty(c, indent + 1)).collect::<String>(),
        ),
        MathNode::MText(s) => format!("{pad}<mtext>{s}</mtext>\n"),
        MathNode::Mi(s)    => format!("{pad}<mi>{s}</mi>\n"),
        MathNode::Mo(s)    => format!("{pad}<mo>{s}</mo>\n"),
        MathNode::Mn(s)    => format!("{pad}<mn>{s}</mn>\n"),
        MathNode::MFrac { num, den } => format!(
            "{pad}<mfrac>\n{}{}{pad}</mfrac>\n",
            render_pretty(num, indent + 1),
            render_pretty(den, indent + 1),
        ),
        MathNode::MSup { base, sup } => format!(
            "{pad}<msup>\n{}{}{pad}</msup>\n",
            render_pretty(base, indent + 1),
            render_pretty(sup, indent + 1),
        ),
        MathNode::MSub { base, sub } => format!(
            "{pad}<msub>\n{}{}{pad}</msub>\n",
            render_pretty(base, indent + 1),
            render_pretty(sub, indent + 1),
        ),
        MathNode::MUnder { base, under } => format!(
            "{pad}<munder>\n{}{}{pad}</munder>\n",
            render_pretty(base, indent + 1),
            render_pretty(under, indent + 1),
        ),
        MathNode::MUnderOver { base, under, over } => format!(
            "{pad}<munderover>\n{}{}{}{pad}</munderover>\n",
            render_pretty(base, indent + 1),
            render_pretty(under, indent + 1),
            render_pretty(over, indent + 1),
        ),
    }
}
