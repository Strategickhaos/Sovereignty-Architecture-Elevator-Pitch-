/// Legion of Minds ratification stub.
/// v0: just structure; real implementation later (2/3 votes, traceable).
#[derive(Debug, Clone)]
pub struct Vote {
    pub claude: bool,
    pub grok: bool,
    pub gemini: bool,
}

impl Vote {
    pub fn passes_2_of_3(&self) -> bool {
        let yes = [self.claude, self.grok, self.gemini].iter().filter(|&&b| b).count();
        yes >= 2
    }
}
