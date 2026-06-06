#[derive(Debug, Clone)]
pub struct PadRef {
    pub path: Vec<String>, // e.g. ["J8", "PIN_03"]
}

#[derive(Debug, Clone)]
pub struct Route {
    pub from: PadRef,
    pub to: PadRef,
}

#[derive(Debug, Clone)]
pub struct Brick {
    pub name: String,
    pub route: Route,
}

#[derive(Debug, Clone)]
pub struct Program {
    pub bricks: Vec<Brick>,
}
