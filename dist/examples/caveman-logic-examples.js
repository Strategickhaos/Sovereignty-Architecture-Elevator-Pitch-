/**
 * Examples demonstrating the Caveman Logic System
 */
import { CavemanLogic, PhysicsGate, TRIG6, Decision, createSimpleAngleTester } from '../caveman-logic.js';
console.log("🔥 Caveman Logic System - Examples\n");
console.log("=".repeat(60) + "\n");
// ============================================================================
// Example 1: Simple Physics Gate Check
// ============================================================================
console.log("Example 1: Evaluating a well-designed API endpoint");
console.log("-".repeat(60));
const apiEndpointResult = PhysicsGate.validate({
    requiresFreeEnergy: false, // Uses normal compute
    effectAfterCause: true, // Request → Response
    canBeBounded: true, // Rate limits possible
    isReproducible: true, // Deterministic
    failsSafely: true // Returns proper errors
});
console.log(`Passed: ${apiEndpointResult.passed}`);
apiEndpointResult.details.forEach(d => console.log(`  ${d}`));
console.log();
// ============================================================================
// Example 2: Concept that violates physics
// ============================================================================
console.log("Example 2: Evaluating a concept that violates causality");
console.log("-".repeat(60));
const timeTravelResult = PhysicsGate.validate({
    requiresFreeEnergy: false,
    effectAfterCause: false, // ❌ Effect before cause!
    canBeBounded: true,
    isReproducible: false, // ⚠️ Can't reproduce
    failsSafely: true
});
console.log(`Passed: ${timeTravelResult.passed}`);
timeTravelResult.details.forEach(d => console.log(`  ${d}`));
console.log();
// ============================================================================
// Example 3: Full evaluation with TRIG6
// ============================================================================
console.log("Example 3: Full evaluation - Feature that scales poorly");
console.log("-".repeat(60));
const scalingIssueEval = CavemanLogic.evaluate({
    name: "Real-time sync for all users",
    requiresFreeEnergy: false,
    effectAfterCause: true,
    canBeBounded: true,
    isReproducible: true,
    failsSafely: true
}, 
// Custom angle tester that fails at scale
(angleNumber, description) => {
    let passed = true;
    let notes = "Stays bounded";
    // Simulate testing under different assumptions
    if (angleNumber === 1) {
        // Angle 1: Scale
        passed = false;
        notes = "Blows up with 1M+ users - memory exhaustion";
    }
    else if (angleNumber === 3) {
        // Angle 3: Resources
        passed = false;
        notes = "Requires exponential bandwidth growth";
    }
    return { angle: angleNumber, description, passed, notes };
});
console.log(`Decision: ${scalingIssueEval.decision}`);
console.log(`Recommendation: ${scalingIssueEval.recommendation}`);
if (scalingIssueEval.trig6) {
    console.log(`\nTRIG6 Analysis:`);
    console.log(`  Outcome: ${scalingIssueEval.trig6.outcome}`);
    console.log(`  Bounded: ${scalingIssueEval.trig6.bounded}`);
    console.log(`  Resonance: ${scalingIssueEval.trig6.resonance}`);
    console.log(`\nAngle Tests:`);
    scalingIssueEval.trig6.details.forEach(d => console.log(`  ${d}`));
}
console.log();
// ============================================================================
// Example 4: Simple angle tester
// ============================================================================
console.log("Example 4: Using createSimpleAngleTester");
console.log("-".repeat(60));
const simpleTest = TRIG6.test("Caching strategy", createSimpleAngleTester((angle) => {
    // All angles pass - good caching is robust
    return true;
}));
console.log(`Outcome: ${simpleTest.outcome}`);
console.log(`Bounded: ${simpleTest.bounded}`);
console.log(`Resonance: ${simpleTest.resonance}`);
console.log();
// ============================================================================
// Example 5: Quick sanity check
// ============================================================================
console.log("Example 5: Quick sanity check - doesItCompute()");
console.log("-".repeat(60));
const goodConcept = CavemanLogic.doesItCompute(false, true, true, true, true);
console.log(`Good concept computes: ${goodConcept}`);
const badConcept = CavemanLogic.doesItCompute(true, // ❌ Requires free energy
true, true, true, true);
console.log(`Bad concept computes: ${badConcept}`);
console.log();
// ============================================================================
// Example 6: Narrow band resonance (handle gently)
// ============================================================================
console.log("Example 6: Concept that works in narrow band (resonance)");
console.log("-".repeat(60));
const narrowBandEval = CavemanLogic.evaluate({
    name: "ML model for edge cases",
    requiresFreeEnergy: false,
    effectAfterCause: true,
    canBeBounded: true,
    isReproducible: true,
    failsSafely: true
}, (angleNumber, description) => {
    // Works in most cases but not all
    const passed = angleNumber !== 2 && angleNumber !== 4;
    const notes = passed
        ? "Works well in this context"
        : "Accuracy degrades significantly";
    return { angle: angleNumber, description, passed, notes };
});
console.log(`Decision: ${narrowBandEval.decision}`);
console.log(`Recommendation: ${narrowBandEval.recommendation}`);
if (narrowBandEval.trig6) {
    console.log(`\nThis concept has ${narrowBandEval.trig6.resonance ? 'RESONANCE' : 'NO RESONANCE'}`);
    console.log(`Should be: ${narrowBandEval.trig6.outcome.toUpperCase()}`);
}
console.log();
// ============================================================================
// Example 7: Real-world scenarios
// ============================================================================
console.log("Example 7: Real-world scenario evaluations");
console.log("-".repeat(60));
const scenarios = [
    {
        name: "Database connection pooling",
        physics: {
            requiresFreeEnergy: false,
            effectAfterCause: true,
            canBeBounded: true,
            isReproducible: true,
            failsSafely: true
        }
    },
    {
        name: "Infinite scroll without pagination",
        physics: {
            requiresFreeEnergy: false,
            effectAfterCause: true,
            canBeBounded: false, // ❌ Unbounded memory growth
            isReproducible: true,
            failsSafely: false // ❌ OOM crashes
        }
    },
    {
        name: "Retry logic with exponential backoff",
        physics: {
            requiresFreeEnergy: false,
            effectAfterCause: true,
            canBeBounded: true,
            isReproducible: true,
            failsSafely: true
        }
    }
];
scenarios.forEach(scenario => {
    const result = CavemanLogic.evaluate(scenario.physics);
    const symbol = result.decision === Decision.ACCEPT ? "✅" :
        result.decision === Decision.INVESTIGATE ? "⚠️ " : "❌";
    console.log(`${symbol} ${scenario.name}: ${result.decision}`);
});
console.log("\n" + "=".repeat(60));
console.log("✅ Examples complete!");
console.log("\nKey Takeaway: 'Does it compute?'");
console.log("  - If not → fuck 'em (discard/sandbox)");
console.log("  - If maybe → TRIG6 it");
console.log("  - If yes → keep building");
console.log("\nThat's it. That's the whole operating system.");
