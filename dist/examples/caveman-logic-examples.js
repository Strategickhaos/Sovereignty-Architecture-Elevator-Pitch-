// src/caveman-logic.ts
var PhysicsGate = class {
  /**
   * Validate a concept against physics constraints
   */
  static validate(concept) {
    const details = [];
    const energyOk = !concept.requiresFreeEnergy;
    if (!energyOk) {
      details.push("\u274C Energy: Requires free energy \u2192 REJECT");
    } else {
      details.push("\u2705 Energy: No free energy required");
    }
    const causalityOk = concept.effectAfterCause;
    if (!causalityOk) {
      details.push("\u274C Causality: Effect before cause \u2192 REJECT");
    } else {
      details.push("\u2705 Causality: Effect follows cause");
    }
    const constraintsOk = concept.canBeBounded;
    if (!constraintsOk) {
      details.push("\u26A0\uFE0F  Constraints: Cannot be bounded \u2192 SANDBOX");
    } else {
      details.push("\u2705 Constraints: Can be bounded with limits");
    }
    const reproducibilityOk = concept.isReproducible;
    if (!reproducibilityOk) {
      details.push("\u26A0\uFE0F  Reproducibility: Cannot reproduce \u2192 LOG + IGNORE");
    } else {
      details.push("\u2705 Reproducibility: Can be reproduced");
    }
    const failureModeOk = concept.failsSafely;
    if (!failureModeOk) {
      details.push("\u274C Failure Mode: Does not fail safely \u2192 FIX OR TOSS");
    } else {
      details.push("\u2705 Failure Mode: Fails loud and safe");
    }
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
};
var TRIG6 = class {
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
    const allPassed = angles.every((a) => a.passed);
    const anyFailed = angles.some((a) => !a.passed);
    const mostPassed = angles.filter((a) => a.passed).length >= 4;
    let outcome;
    let resonance = false;
    let bounded = true;
    const details = [];
    if (anyFailed && !mostPassed) {
      outcome = "reject";
      bounded = false;
      details.push("\u274C Concept blows up at multiple angles \u2192 REJECT WITH LOVE");
    } else if (allPassed) {
      outcome = "keep";
      bounded = true;
      details.push("\u2705 Concept stays bounded across all angles \u2192 KEEP");
    } else {
      outcome = "handle_gently";
      resonance = true;
      bounded = true;
      details.push("\u26A0\uFE0F  Concept resonates (narrow band) \u2192 HANDLE GENTLY");
    }
    angles.forEach((angle) => {
      const status = angle.passed ? "\u2705" : "\u274C";
      details.push(`${status} Angle ${angle.angle}: ${angle.description}`);
      if (angle.notes) {
        details.push(`   \u2192 ${angle.notes}`);
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
};
var CavemanLogic = class {
  /**
   * Run a concept through the complete Caveman Logic system
   */
  static evaluate(concept, angleTester) {
    const physicsGate = PhysicsGate.validate(concept);
    let decision;
    let trig6;
    let recommendation;
    if (!physicsGate.passed) {
      if (!physicsGate.energy || !physicsGate.causality || !physicsGate.failureMode) {
        decision = "reject" /* REJECT */;
        recommendation = "\u274C REJECT: Violates fundamental physics constraints. Discard or sandbox.";
      } else if (!physicsGate.constraints) {
        decision = "reject" /* REJECT */;
        recommendation = "\u26A0\uFE0F  SANDBOX: Cannot be bounded. Isolate for safety.";
      } else {
        decision = "investigate" /* INVESTIGATE */;
        recommendation = "\u26A0\uFE0F  INVESTIGATE: Not reproducible. Log and monitor before deciding.";
      }
    } else if (angleTester) {
      trig6 = TRIG6.test(concept.name, angleTester);
      if (trig6.outcome === "reject") {
        decision = "reject" /* REJECT */;
        recommendation = "\u274C REJECT WITH LOVE: Passes physics but blows up under different assumptions.";
      } else if (trig6.outcome === "handle_gently") {
        decision = "investigate" /* INVESTIGATE */;
        recommendation = "\u26A0\uFE0F  HANDLE GENTLY: Works in narrow band. Proceed with constraints and monitoring.";
      } else {
        decision = "accept" /* ACCEPT */;
        recommendation = "\u2705 ACCEPT: Passes all tests. Keep building!";
      }
    } else {
      decision = "accept" /* ACCEPT */;
      recommendation = "\u2705 ACCEPT: Passes physics gate. Keep building!";
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
    return !requiresFreeEnergy && effectAfterCause && canBeBounded && isReproducible && failsSafely;
  }
};
function createSimpleAngleTester(testFunction) {
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

// src/examples/caveman-logic-examples.ts
console.log("\u{1F525} Caveman Logic System - Examples\n");
console.log("=".repeat(60) + "\n");
console.log("Example 1: Evaluating a well-designed API endpoint");
console.log("-".repeat(60));
var apiEndpointResult = PhysicsGate.validate({
  requiresFreeEnergy: false,
  // Uses normal compute
  effectAfterCause: true,
  // Request → Response
  canBeBounded: true,
  // Rate limits possible
  isReproducible: true,
  // Deterministic
  failsSafely: true
  // Returns proper errors
});
console.log(`Passed: ${apiEndpointResult.passed}`);
apiEndpointResult.details.forEach((d) => console.log(`  ${d}`));
console.log();
console.log("Example 2: Evaluating a concept that violates causality");
console.log("-".repeat(60));
var timeTravelResult = PhysicsGate.validate({
  requiresFreeEnergy: false,
  effectAfterCause: false,
  // ❌ Effect before cause!
  canBeBounded: true,
  isReproducible: false,
  // ⚠️ Can't reproduce
  failsSafely: true
});
console.log(`Passed: ${timeTravelResult.passed}`);
timeTravelResult.details.forEach((d) => console.log(`  ${d}`));
console.log();
console.log("Example 3: Full evaluation - Feature that scales poorly");
console.log("-".repeat(60));
var scalingIssueEval = CavemanLogic.evaluate(
  {
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
    if (angleNumber === 1) {
      passed = false;
      notes = "Blows up with 1M+ users - memory exhaustion";
    } else if (angleNumber === 3) {
      passed = false;
      notes = "Requires exponential bandwidth growth";
    }
    return { angle: angleNumber, description, passed, notes };
  }
);
console.log(`Decision: ${scalingIssueEval.decision}`);
console.log(`Recommendation: ${scalingIssueEval.recommendation}`);
if (scalingIssueEval.trig6) {
  console.log(`
TRIG6 Analysis:`);
  console.log(`  Outcome: ${scalingIssueEval.trig6.outcome}`);
  console.log(`  Bounded: ${scalingIssueEval.trig6.bounded}`);
  console.log(`  Resonance: ${scalingIssueEval.trig6.resonance}`);
  console.log(`
Angle Tests:`);
  scalingIssueEval.trig6.details.forEach((d) => console.log(`  ${d}`));
}
console.log();
console.log("Example 4: Using createSimpleAngleTester");
console.log("-".repeat(60));
var simpleTest = TRIG6.test(
  "Caching strategy",
  createSimpleAngleTester((angle) => {
    return true;
  })
);
console.log(`Outcome: ${simpleTest.outcome}`);
console.log(`Bounded: ${simpleTest.bounded}`);
console.log(`Resonance: ${simpleTest.resonance}`);
console.log();
console.log("Example 5: Quick sanity check - doesItCompute()");
console.log("-".repeat(60));
var goodConcept = CavemanLogic.doesItCompute(
  false,
  true,
  true,
  true,
  true
);
console.log(`Good concept computes: ${goodConcept}`);
var badConcept = CavemanLogic.doesItCompute(
  true,
  // ❌ Requires free energy
  true,
  true,
  true,
  true
);
console.log(`Bad concept computes: ${badConcept}`);
console.log();
console.log("Example 6: Concept that works in narrow band (resonance)");
console.log("-".repeat(60));
var narrowBandEval = CavemanLogic.evaluate(
  {
    name: "ML model for edge cases",
    requiresFreeEnergy: false,
    effectAfterCause: true,
    canBeBounded: true,
    isReproducible: true,
    failsSafely: true
  },
  (angleNumber, description) => {
    const passed = angleNumber !== 2 && angleNumber !== 4;
    const notes = passed ? "Works well in this context" : "Accuracy degrades significantly";
    return { angle: angleNumber, description, passed, notes };
  }
);
console.log(`Decision: ${narrowBandEval.decision}`);
console.log(`Recommendation: ${narrowBandEval.recommendation}`);
if (narrowBandEval.trig6) {
  console.log(`
This concept has ${narrowBandEval.trig6.resonance ? "RESONANCE" : "NO RESONANCE"}`);
  console.log(`Should be: ${narrowBandEval.trig6.outcome.toUpperCase()}`);
}
console.log();
console.log("Example 7: Real-world scenario evaluations");
console.log("-".repeat(60));
var scenarios = [
  {
    name: "Database connection pooling",
    requiresFreeEnergy: false,
    effectAfterCause: true,
    canBeBounded: true,
    isReproducible: true,
    failsSafely: true
  },
  {
    name: "Infinite scroll without pagination",
    requiresFreeEnergy: false,
    effectAfterCause: true,
    canBeBounded: false,
    // ❌ Unbounded memory growth
    isReproducible: true,
    failsSafely: false
    // ❌ OOM crashes
  },
  {
    name: "Retry logic with exponential backoff",
    requiresFreeEnergy: false,
    effectAfterCause: true,
    canBeBounded: true,
    isReproducible: true,
    failsSafely: true
  }
];
scenarios.forEach((scenario) => {
  const result = CavemanLogic.evaluate(scenario);
  const symbol = result.decision === "accept" /* ACCEPT */ ? "\u2705" : result.decision === "investigate" /* INVESTIGATE */ ? "\u26A0\uFE0F " : "\u274C";
  console.log(`${symbol} ${scenario.name}: ${result.decision}`);
});
console.log("\n" + "=".repeat(60));
console.log("\u2705 Examples complete!");
console.log("\nKey Takeaway: 'Does it compute?'");
console.log("  - If not \u2192 fuck 'em (discard/sandbox)");
console.log("  - If maybe \u2192 TRIG6 it");
console.log("  - If yes \u2192 keep building");
console.log("\nThat's it. That's the whole operating system.");
