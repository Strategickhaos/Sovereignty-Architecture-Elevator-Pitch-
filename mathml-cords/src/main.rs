mod mathml;
mod problems;

use mathml::render::{render, render_pretty};
use problems::cords::{cords_explanation, gate4_limits};

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let problem = args.get(1).map(|s| s.as_str()).unwrap_or("cords");
    let pretty  = args.contains(&"--pretty".into());

    let tree = match problem {
        "gate4"  => gate4_limits(),
        _        => cords_explanation(),
    };

    if pretty {
        println!("{}", render_pretty(&tree, 0));
    } else {
        println!("{}", render(&tree));
    }
}
