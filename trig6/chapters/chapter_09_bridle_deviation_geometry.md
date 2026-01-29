# Chapter 9: Bridle and Deviation Geometry

## Introduction

This chapter covers the fundamental geometry of V-angle load sharing in bridle configurations and deviation systems. We cleanly separate cosine-based geometric load distribution from friction and capstan effects.

## V-Angle Load Sharing

When a load is supported by two anchor points forming a V-angle, the force on each leg depends on the angle between them. This is pure geometry—not friction.

### The Cosine Relationship

For a symmetric bridle with angle θ between the legs:

**Force per leg = Load / (2 × cos(θ/2))**

As the angle increases:
- 60° angle: Each leg carries 58% of the load (1.15× load sharing factor)
- 90° angle: Each leg carries 71% of the load (1.41× load sharing factor)
- 120° angle: Each leg carries 100% of the load (2.0× load sharing factor)
- 150° angle: Each leg carries 193% of the load (3.86× load sharing factor)

### Critical Angles

**FIELD PATTERN — V-Angle Warning**
- **What it is:** As V-angle exceeds 120°, force per leg exceeds the suspended load
- **What it does:** Creates dangerous loading that can fail anchor points
- **What to do:** Keep V-angles below 90° in rigging; never exceed 120°

## Deviation Systems

When rope deviates around an anchor point, the anchor sees the vector sum of tensions from both sides of the rope.

### Deviation Force Calculation

For rope under tension T deviating at angle θ:

**Deviation Force = 2T × sin(θ/2)**

Small angles result in small deviation forces:
- 10° deviation: Force = 0.17T (17% of rope tension)
- 30° deviation: Force = 0.52T (52% of rope tension)
- 60° deviation: Force = T (100% of rope tension)
- 90° deviation: Force = 1.41T (141% of rope tension)

## Friction vs. Geometry

**Important Distinction:** This chapter addresses geometric load distribution only. 

Friction effects (capstan equations, rope-on-rope friction) are separate phenomena that:
- Add resistance to rope movement
- Create holding power in descenders and progress capture devices
- Are covered in dedicated friction analysis chapters

The geometric principles here apply whether the system is static or in motion.

## Field Applications

### Anchor Rigging
- Use narrower V-angles to reduce per-leg loading
- Position anchors to minimize bridle angles
- Calculate actual forces, don't guess based on the suspended load

### Highlines and Traverses
- Deviation angles affect anchor loading at intermediate points
- Sag in the line influences deviation angles
- Tension amplification must be considered (see Chapter 17)

### Multi-Point Systems
- Each connection point sees geometry-based load distribution
- Complex systems require vector analysis of each junction
- Software tools can help visualize force vectors

## Summary

V-angle geometry and deviation angles determine how forces distribute in rope systems. Understanding these relationships allows technicians to:
- Predict anchor loading accurately
- Design safer rigging configurations
- Avoid dangerous geometric configurations
- Make informed decisions in the field

This geometric foundation is essential before considering dynamic loading, mechanical advantage, or system integration.

---

*Next: Chapter 17 — Dynamic Loading*
