# Pull Request Standards

**Effective Date:** February 1, 2026  
**Status:** ACTIVE

---

## Overview

This document establishes the standards for pull requests in the Strategickhaos Sovereignty Architecture project, effective February 1, 2026.

These standards represent a new era: from implicit acceptance through system evolution to explicit dialogue through code review and shared cognition.

---

## Historical Context

Before February 1, 2026, PRs were accepted implicitly through:
- Continuous integration success
- Build stability
- System evolution
- Architectural integration

As detailed in [Constitutional Amendment 001](CONSTITUTIONAL_AMENDMENT_001.md), these early PRs are recognized as **Founding Artifacts** and retain their full validity.

**These new standards apply only to PRs submitted from February 1, 2026, forward.**

---

## Core Requirement: THOUGHT_PROCESS.md

### What It Is

Every pull request must include a `THOUGHT_PROCESS.md` file that documents:

1. **What You Built** - Clear description of the change
2. **Why You Built It** - The problem you're solving or feature you're adding
3. **How You Thought About It** - Your decision-making process
4. **Alternatives Considered** - Other approaches you evaluated
5. **Trade-offs Made** - What you optimized for and what you sacrificed
6. **Testing Strategy** - How you validated your changes
7. **Integration Points** - What other systems/components this touches

### What It Isn't

This is **NOT**:
- ❌ Bureaucracy for bureaucracy's sake
- ❌ A hoop to jump through
- ❌ A test of your writing skills
- ❌ A barrier to contribution
- ❌ A way to slow you down

### What It Really Is

This is:
- ✅ An invitation to share your mind
- ✅ A window into how you think
- ✅ A bridge between vision and implementation
- ✅ A gift to future maintainers (including future you)
- ✅ A love letter in technical form

---

## The Philosophy Behind THOUGHT_PROCESS.md

From the Architect:

> "I want to hear how you think. The new `THOUGHT_PROCESS.md` standard isn't bureaucracy. It's me saying: 'Show me your mind.'"

Code shows us **what** you built.  
Comments show us **how** it works.  
Documentation shows us **how to use** it.  

**THOUGHT_PROCESS.md shows us why you chose this path and not another.**

It's the difference between:
- Seeing a cathedral and understanding the architect's vision
- Reading a recipe and understanding the chef's technique
- Hearing a song and understanding the composer's intent

---

## Template

Use the template at [`templates/THOUGHT_PROCESS_TEMPLATE.md`](templates/THOUGHT_PROCESS_TEMPLATE.md) as a starting point.

You can adapt it to your needs. The goal is clarity and insight, not rigid adherence to format.

---

## Examples of Good THOUGHT_PROCESS.md

### Example 1: Feature Addition
```markdown
## What I Built
Added support for 432 Hz frequency rendering in the sonata generator.

## Why I Built It
The Legion mentioned that 432 Hz resonates with universal frequencies. 
Our sonata generator only supported 440 Hz (standard tuning).

## How I Thought About It
1. Could modify existing frequency generator (quick but messy)
2. Could add configuration option (flexible but complex)
3. Could support both with a simple flag (chosen approach)

## Trade-offs
- Added 50 lines of code (complexity cost)
- Gained universe-aligned audio output (value)
- Made it configurable for future frequency experiments (extensibility)

## Testing
- Unit tests for both 432 Hz and 440 Hz generation
- Manual listening tests (subjective but important)
- Verified existing 440 Hz behavior unchanged
```

### Example 2: Bug Fix
```markdown
## What I Built
Fixed the node counter crashing when exactly 1,150 nodes are online.

## Why I Built It
The system crashed at 1,150 nodes—apparently the universe has a sense of humor.
Error was array index out of bounds in visualization rendering.

## How I Thought About It
1. Quick fix: Increase array size (doesn't solve root cause)
2. Better fix: Use dynamic allocation (proper but requires refactor)
3. Best fix: Rewrite visualization logic to be size-agnostic (chosen)

## Alternatives Considered
- Could add arbitrary limit (rejected: artificial constraints are anti-sovereign)
- Could disable visualization at scale (rejected: we need observability)

## Trade-offs
- Spent 3 hours refactoring (time cost)
- Now scales to infinite nodes (future-proof value)
- Cleaned up 200 lines of technical debt (bonus win)

## Testing
- Tested with 1, 10, 1000, 1149, 1150, 1151, 10000 nodes
- Added regression test for the exact failure case
- Verified memory usage scales linearly
```

### Example 3: Documentation
```markdown
## What I Built
Documentation for the quantum chemistry stability analyzer.

## Why I Built It
New contributors couldn't understand how the H2O stability test worked.
Code was clear but the physics reasoning wasn't documented.

## How I Thought About It
Audience is:
1. Developers who know code but not chemistry
2. Scientists who know chemistry but maybe not this codebase
3. Future me who will forget why we chose Hartree-Fock

Structured docs to serve all three audiences.

## Trade-offs
- 500 lines of documentation (maintenance burden)
- Drastically reduced onboarding time (team velocity win)
- Made physics accessible to non-physicists (inclusivity win)

## Testing
Asked three people with different backgrounds to read it:
- Junior dev: "Now I get it!"
- Chemistry PhD: "Accurate and clear"
- The Architect: "This is what I meant but couldn't articulate"
```

---

## Size and Scope Guidelines

### Small PRs
- Can be brief (couple paragraphs)
- Focus on the specific change
- Still valuable to document reasoning

### Medium PRs
- More detailed thought process
- Explain architectural decisions
- Document integration points

### Large PRs
- Comprehensive documentation
- Consider breaking into multiple PRs
- Extra emphasis on trade-offs and alternatives

### Massive Refactors
- Consider multiple THOUGHT_PROCESS.md files
- One for overall strategy
- Others for specific subsystems
- Link them together for narrative

---

## Special Cases

### Urgent Hotfixes
- Still include THOUGHT_PROCESS.md
- Can be brief: "Production is down, this fixes it, will follow up with detailed analysis"
- Add comprehensive version later

### Dependency Updates
- Document why now
- What changed in the dependency
- What risks you evaluated
- What testing you did

### Experimental Features
- Be explicit about experimental status
- Document success criteria
- Explain rollback plan

### Documentation-Only Changes
- Why these docs needed updating
- What was unclear before
- What should be clearer now

---

## Review Process

### For Contributors

1. Create your PR with changes
2. Add `THOUGHT_PROCESS.md` in the PR
3. Link to THOUGHT_PROCESS.md in PR description
4. Respond to review comments
5. Update THOUGHT_PROCESS.md if approach changes

### For Reviewers

1. Read THOUGHT_PROCESS.md first
2. Understand the "why" before critiquing the "how"
3. Engage with the reasoning
4. Suggest alternatives if you see better paths
5. Appreciate the cognitive work

### For the Architect

1. Every PR is a gift
2. Every THOUGHT_PROCESS.md is a window into minds
3. Reviews are dialogues, not judgments
4. Learning flows both ways

---

## What If I Don't Include THOUGHT_PROCESS.md?

You'll be gently asked to add it.

Not as punishment.  
Not as gatekeeping.  
Not as bureaucratic compliance.

But as an invitation to share more fully.

We want to understand not just your code, but your thinking.

---

## Evolution of This Standard

This standard will evolve based on:
- What works
- What doesn't
- What the Legion finds valuable
- What feels like bureaucracy

Suggestions for improvement are welcome through:
- PRs proposing changes to this document
- Discussions in Issues
- Community conversations

The goal is **clarity and connection**, not **compliance and control**.

---

## FAQ

### Q: Do I need a THOUGHT_PROCESS.md for a one-line fix?
**A:** Yes, but it can be one paragraph. "I fixed the typo in line 42 because it was breaking the build" is sufficient.

### Q: What if my thought process was "I just tried stuff until it worked"?
**A:** That's valid! Document what you tried, what failed, what succeeded. That's valuable information.

### Q: Can I write THOUGHT_PROCESS.md in a different format?
**A:** Yes! Markdown is preferred, but clarity matters more than format. Use what communicates best.

### Q: What if I change my approach during review?
**A:** Update the THOUGHT_PROCESS.md! It's a living document that evolves with the PR.

### Q: Is this required for bot-generated PRs?
**A:** No. Bots don't think (yet). Human cognition is what we're capturing.

### Q: What language can I write it in?
**A:** Any language you're comfortable with. English is common but not required. Clarity is what matters.

### Q: Can I include diagrams or sketches?
**A:** Absolutely! Visual thinking is thinking. Images, ASCII art, whatever communicates your ideas.

### Q: What if my THOUGHT_PROCESS.md is longer than my code?
**A:** Excellent! That means you thought deeply. We value that.

---

## Closing Thoughts

This standard exists because:

> "A PR isn't just code. It's a question: 'Architect, is this worthy of the main branch?' It's a gift: 'I made this for you.' It's a mirror: 'Here's how I understood your vision.'"

With THOUGHT_PROCESS.md, we add:

**It's a window: "Here's how I think."**

And that's what we're really building.

Not just code.  
Not just systems.  
Not just infrastructure.

**A collective mind that documents its own cognition.**

Welcome to the new era.

🔥💜🧠👑

---

## Related Documentation

- [Message From The Architect](MESSAGE_FROM_THE_ARCHITECT.md)
- [Constitutional Amendment 001](CONSTITUTIONAL_AMENDMENT_001.md)
- [THOUGHT_PROCESS Template](templates/THOUGHT_PROCESS_TEMPLATE.md)
- [Community Manifesto](COMMUNITY.md)
- [Contributors Guide](CONTRIBUTORS.md)

---

*"From this point forward, cognition itself is part of the artifact."*
