/**
 * Caveman Logic System
 *
 * A clean, safe decision-making framework based on fundamental physics constraints
 * and multi-angle testing methodology.
 *
 * Core principle: "Does this shit compute?"
 * - If no → discard/sandbox
 * - If maybe → TRIG6 it (test from more angles)
 * - If yes → keep building
 */
/**
 * Decision outcomes for the main gate
 */
export var Decision;
(function (Decision) {
    Decision["REJECT"] = "reject";
    Decision["INVESTIGATE"] = "investigate";
    Decision["ACCEPT"] = "accept"; // Keep building
})(Decision || (Decision = {}));
/**
 * Caveman Physics Gate
 *
 * 5 fundamental validation checks based on physics constraints:
 * 1. Energy - Does it require free energy? (If yes → nope)
 * 2. Causality - Does effect come after cause? (If no → nope)
 * 3. Constraints - Can I bound it? (If no → sandbox)
 * 4. Reproducibility - Can I make it happen again? (If no → log + ignore)
 * 5. Failure mode - Does it fail loud and safe? (If no → fix or toss)
 */
export class PhysicsGate {
    /**
     * Validate a concept against physics constraints
     */
    static validate(concept) {
        const details = [];
        // 1. Energy check
        const energyOk = !concept.requiresFreeEnergy;
        if (!energyOk) {
            details.push("❌ Energy: Requires free energy → REJECT");
        }
        else {
            details.push("✅ Energy: No free energy required");
        }
        // 2. Causality check
        const causalityOk = concept.effectAfterCause;
        if (!causalityOk) {
            details.push("❌ Causality: Effect before cause → REJECT");
        }
        else {
            details.push("✅ Causality: Effect follows cause");
        }
        // 3. Constraints check
        const constraintsOk = concept.canBeBounded;
        if (!constraintsOk) {
            details.push("⚠️  Constraints: Cannot be bounded → SANDBOX");
        }
        else {
            details.push("✅ Constraints: Can be bounded with limits");
        }
        // 4. Reproducibility check
        const reproducibilityOk = concept.isReproducible;
        if (!reproducibilityOk) {
            details.push("⚠️  Reproducibility: Cannot reproduce → LOG + IGNORE");
        }
        else {
            details.push("✅ Reproducibility: Can be reproduced");
        }
        // 5. Failure mode check
        const failureModeOk = concept.failsSafely;
        if (!failureModeOk) {
            details.push("❌ Failure Mode: Does not fail safely → FIX OR TOSS");
        }
        else {
            details.push("✅ Failure Mode: Fails loud and safe");
        }
        // Overall pass requires all critical checks
        const passed = energyOk && causalityOk && constraintsOk && reproducibilityOk && failureModeOk;
        return {
            energy: energyOk,
            causality: causalityOk,
            constraints: constraintsOk,
            reproducibility: reproducibilityOk,
            failureMode: failureModeOk,
            passed,
            details
        };
    }
}
/**
 * TRIG6 - Multi-angle testing methodology
 *
 * When something is fuzzy but interesting:
 * 1. Look at it from 6 angles (change assumptions)
 * 2. If it blows up at any angle → reject with love
 * 3. If it stays bounded across angles → keep
 * 4. If it resonates (works only in narrow band) → handle gently
 */
export class TRIG6 {
    /**
     * Test a concept from 6 different angles
     * Each angle represents changing a different assumption
     */
    static test(concept, angleTester) {
        const angles = [
            angleTester(1, "Change scale assumptions (larger/smaller)"),
            angleTester(2, "Change time assumptions (faster/slower)"),
            angleTester(3, "Change resource assumptions (more/less)"),
            angleTester(4, "Change environmental assumptions (different context)"),
            angleTester(5, "Change interaction assumptions (isolated/connected)"),
            angleTester(6, "Change boundary assumptions (open/closed system)")
        ];
        const allPassed = angles.every(a => a.passed);
        const anyFailed = angles.some(a => !a.passed);
        const mostPassed = angles.filter(a => a.passed).length >= 4;
        let outcome;
        let resonance = false;
        let bounded = true;
        const details = [];
        if (anyFailed && !mostPassed) {
            // Blows up at multiple angles
            outcome = "reject";
            bounded = false;
            details.push("❌ Concept blows up at multiple angles → REJECT WITH LOVE");
        }
        else if (allPassed) {
            // Stays bounded across all angles
            outcome = "keep";
            bounded = true;
            details.push("✅ Concept stays bounded across all angles → KEEP");
        }
        else {
            // Works in some contexts but not others
            outcome = "handle_gently";
            resonance = true;
            bounded = true;
            details.push("⚠️  Concept resonates (narrow band) → HANDLE GENTLY");
        }
        // Add angle details
        angles.forEach(angle => {
            const status = angle.passed ? "✅" : "❌";
            details.push(`${status} Angle ${angle.angle}: ${angle.description}`);
            if (angle.notes) {
                details.push(`   → ${angle.notes}`);
            }
        });
        return {
            angles,
            outcome,
            resonance,
            bounded,
            details
        };
    }
}
/**
 * Main Caveman Logic Gate
 *
 * The complete decision-making system:
 * "Does this shit compute?"
 */
export class CavemanLogic {
    /**
     * Run a concept through the complete Caveman Logic system
     */
    static evaluate(concept, angleTester) {
        // Step 1: Physics Gate validation
        const physicsGate = PhysicsGate.validate(concept);
        // Step 2: Make initial decision
        let decision;
        let trig6;
        let recommendation;
        if (!physicsGate.passed) {
            // Failed physics gate - immediate rejection or sandbox
            if (!physicsGate.energy || !physicsGate.causality || !physicsGate.failureMode) {
                decision = Decision.REJECT;
                recommendation = "❌ REJECT: Violates fundamental physics constraints. Discard or sandbox.";
            }
            else if (!physicsGate.constraints) {
                decision = Decision.REJECT;
                recommendation = "⚠️  SANDBOX: Cannot be bounded. Isolate for safety.";
            }
            else {
                decision = Decision.INVESTIGATE;
                recommendation = "⚠️  INVESTIGATE: Not reproducible. Log and monitor before deciding.";
            }
        }
        else if (angleTester) {
            // Passed physics gate, but let's TRIG6 it for thoroughness
            trig6 = TRIG6.test(concept.name, angleTester);
            if (trig6.outcome === "reject") {
                decision = Decision.REJECT;
                recommendation = "❌ REJECT WITH LOVE: Passes physics but blows up under different assumptions.";
            }
            else if (trig6.outcome === "handle_gently") {
                decision = Decision.INVESTIGATE;
                recommendation = "⚠️  HANDLE GENTLY: Works in narrow band. Proceed with constraints and monitoring.";
            }
            else {
                decision = Decision.ACCEPT;
                recommendation = "✅ ACCEPT: Passes all tests. Keep building!";
            }
        }
        else {
            // Passed physics gate, no TRIG6 test provided
            decision = Decision.ACCEPT;
            recommendation = "✅ ACCEPT: Passes physics gate. Keep building!";
        }
        return {
            decision,
            physicsGate,
            trig6,
            recommendation
        };
    }
    /**
     * Quick sanity check - does it compute?
     */
    static doesItCompute(requiresFreeEnergy, effectAfterCause, canBeBounded, isReproducible, failsSafely) {
        return !requiresFreeEnergy &&
            effectAfterCause &&
            canBeBounded &&
            isReproducible &&
            failsSafely;
    }
}
/**
 * Utility function to create a simple angle tester
 * Useful for quick testing
 */
export function createSimpleAngleTester(testFunction) {
    return (angleNumber, description) => {
        const passed = testFunction(angleNumber);
        return {
            angle: angleNumber,
            description,
            passed,
            notes: passed ? "Stays bounded" : "Blows up"
        };
    };
}
