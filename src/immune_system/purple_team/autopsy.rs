/// Tool autopsy stub: intake -> isolate -> analyze -> rebuild plan.
pub fn autopsy_plan(tool_name: &str) -> String {
    format!("AUTOPSY_PLAN::{tool_name}::(quarantine->analysis->purify->organize)")
}
