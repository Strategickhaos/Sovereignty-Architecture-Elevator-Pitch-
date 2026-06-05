# CHAPTER 17: Dynamic Loading

## Static vs. Dynamic Forces

Everything we've covered so far assumes static loads—constant, predictable forces like a hanging technician or steady haul. But rope access isn't always static. Drops, swings, falls, or sudden stops introduce dynamics: forces that change rapidly in magnitude and direction.

**Static force**: Constant, like your 200 lbs (0.9 kN) body weight at rest.

**Dynamic force**: Variable, amplified by acceleration. A 200 lb load dropping 2 feet can generate thousands of pounds on the system.

**Why care?** Dynamics can multiply tensions 2-10× or more, snapping ropes, shearing anchors, or turning a minor slip into a catastrophe. TRIG6 helps here too—angles modify dynamic impacts just like static ones.

## Fall Factor Explained

The fall factor (FF) measures how bad a fall is: **FF = Fall Distance / Rope Available to Absorb It**.

FF ranges 0-2 (above 2 is rare in access; you'd hit ground first).

- **FF 0**: No fall, just static hang.
- **FF 1**: Fall equal to rope length (e.g., 10 ft fall on 10 ft rope).
- **FF 2**: Worst case—fall twice the rope length (e.g., 20 ft on 10 ft, climber above anchor).

### Diagram:

```
Anchor ●  
       │ Rope length L  
       │  
       │ Fall distance 2L → FF=2  
       │  
       ● Climber starts here  
```

**Why FF matters**: Higher FF = higher impact force, because less rope to stretch and absorb energy.

## Impact Force Calculations

The basic impact formula (simplified for field use):

**Impact Force ≈ Weight × (1 + √(2 × FF))**

Where:
- Weight = static load (e.g., 200 lbs)
- FF = fall factor

This assumes ideal dynamic rope (10-15% stretch). Static ropes (low stretch) multiply impacts further—avoid for fall arrest.

### Example Table (200 lb Load, Dynamic Rope):

| FF  | √(2×FF) | Impact Multiplier | Peak Force (lbs) | Peak Force (kN) |
|-----|---------|-------------------|------------------|-----------------|
| 0   | 0       | 1×                | 200              | 0.9             |
| 0.5 | 1.41    | 2.41×             | 482              | 2.1             |
| 1   | 2       | 3×                | 600              | 2.7             |
| 1.5 | 2.45    | 3.45×             | 690              | 3.1             |
| 2   | 2.83    | 3.83×             | 766              | 3.4             |

**Note**: For exact work, use 1 kN = 224.81 lbf. These are theoretical; real impacts add friction, angles.

## TRIG6 Modification for Angles

Falls aren't always straight down. Angles introduce horizontal components, increasing effective FF.

If fall angle θ (from vertical):

**Effective Impact = Impact Force × sec(θ)**  [sec = 1/cos, your tension multiplier]

**Why?** The rope must provide more tension to counter the sideways vector.

### Example: FF1 fall at 30° from vertical:

- **Base Impact**: 600 lbs
- **Modified**: 600 × sec(30°) = 600 × 1.155 ≈ 693 lbs

### At 60°: 
600 × sec(60°) = 600 × 2 = 1,200 lbs (doubles!)

**Tie-in**: Same as your highline/deviation—reciprocals amplify.

## Why Dynamics Change Everything

- **Rope Stretch**: Dynamic ropes absorb ~30-40% energy via elongation; static ropes <5%, so impacts spike.
- **System Effects**: Pulleys add mass/inertia; friction reduces some peaks but unevenly.
- **Human Factor**: Shock loads can injure even if gear holds (e.g., >12 kN on body = severe risk).
- **Integration**: Dynamics multiply static issues—e.g., a FF1 fall through a 120° deviation: base 600 lbs × 2× multiplier = 1,200 lbs rope tension.

### Field Rule: 
Design for worst-case FF2, apply 10:1 safety factor for dynamics (vs. 5:1 static).

**Disclaimer**: Always verify with rated equipment, manufacturer data, and applicable standards (SPRAT/IRATA); this text is educational.

## FIELD PATTERN — "FF Cliff at 1"

- **FF <0.5**: Manageable, like lead climbing falls.
- **FF 1+**: Gear-tested territory—double-check anchors.
- **FF 2**: Avoid at all costs; rig belays to keep FF <1.

**Rule**: Shorten exposed rope lengths to minimize FF.
