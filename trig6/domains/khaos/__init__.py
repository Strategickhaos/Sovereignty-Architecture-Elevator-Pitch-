"""
TRIG6 KHAOS Domain
64-glyph symbolic system for quantum-state representation
"""


# 64-glyph symbolic system (DNA codon-inspired)
KHAOS_GLYPHS = {
    # Base glyphs (16 primordial forms)
    0x00: {"glyph": "∅", "name": "void", "meaning": "null state"},
    0x01: {"glyph": "◬", "name": "genesis", "meaning": "creation point"},
    0x02: {"glyph": "◭", "name": "collapse", "meaning": "wave function collapse"},
    0x03: {"glyph": "◮", "name": "entangle", "meaning": "quantum entanglement"},
    0x04: {"glyph": "◯", "name": "orbit", "meaning": "stable state"},
    0x05: {"glyph": "◰", "name": "flux", "meaning": "state transition"},
    0x06: {"glyph": "◱", "name": "mirror", "meaning": "reflection/symmetry"},
    0x07: {"glyph": "◲", "name": "shield", "meaning": "protection/isolation"},
    0x08: {"glyph": "◳", "name": "gate", "meaning": "conditional branch"},
    0x09: {"glyph": "◴", "name": "spiral", "meaning": "recursive pattern"},
    0x0A: {"glyph": "◵", "name": "pulse", "meaning": "oscillation"},
    0x0B: {"glyph": "◶", "name": "split", "meaning": "superposition"},
    0x0C: {"glyph": "◷", "name": "merge", "meaning": "convergence"},
    0x0D: {"glyph": "◸", "name": "ascend", "meaning": "energy increase"},
    0x0E: {"glyph": "◹", "name": "descend", "meaning": "energy decrease"},
    0x0F: {"glyph": "◺", "name": "bridge", "meaning": "connection"},
    
    # Composite glyphs (48 more for total of 64)
    # DNA codon mappings for computational states
    0x10: {"glyph": "⚡", "name": "strike", "meaning": "rapid state change"},
    0x11: {"glyph": "⚛", "name": "atom", "meaning": "fundamental unit"},
    0x12: {"glyph": "⚝", "name": "star", "meaning": "attractor state"},
    0x13: {"glyph": "⚞", "name": "corner", "meaning": "boundary condition"},
    0x14: {"glyph": "⚟", "name": "anchor", "meaning": "fixed point"},
    0x15: {"glyph": "⚠", "name": "warning", "meaning": "unstable state"},
    0x16: {"glyph": "⚙", "name": "gear", "meaning": "mechanical process"},
    0x17: {"glyph": "⚢", "name": "union", "meaning": "combination"},
    0x18: {"glyph": "⚣", "name": "intersect", "meaning": "collision"},
    0x19: {"glyph": "⚤", "name": "balance", "meaning": "equilibrium"},
    0x1A: {"glyph": "⚥", "name": "duality", "meaning": "paired states"},
    0x1B: {"glyph": "⚦", "name": "triple", "meaning": "three-way interaction"},
    0x1C: {"glyph": "⚧", "name": "transform", "meaning": "metamorphosis"},
    0x1D: {"glyph": "⚨", "name": "cross", "meaning": "interference"},
    0x1E: {"glyph": "⚩", "name": "flag", "meaning": "marker/signal"},
    0x1F: {"glyph": "⚪", "name": "circle", "meaning": "completion"},
    
    # Extended set for computational primitives
    0x20: {"glyph": "⚫", "name": "black", "meaning": "absorb all"},
    0x21: {"glyph": "⚬", "name": "medium", "meaning": "partial state"},
    0x22: {"glyph": "⚭", "name": "bond", "meaning": "strong coupling"},
    0x23: {"glyph": "⚮", "name": "divorce", "meaning": "decoupling"},
    0x24: {"glyph": "⚯", "name": "unmarried", "meaning": "independent"},
    0x25: {"glyph": "⚰", "name": "coffin", "meaning": "end state"},
    0x26: {"glyph": "⚱", "name": "urn", "meaning": "storage/memory"},
    0x27: {"glyph": "⚲", "name": "neuter", "meaning": "neutral state"},
    0x28: {"glyph": "⚳", "name": "earth", "meaning": "ground state"},
    0x29: {"glyph": "⚴", "name": "jupiter", "meaning": "expansion"},
    0x2A: {"glyph": "⚵", "name": "saturn", "meaning": "contraction"},
    0x2B: {"glyph": "⚶", "name": "uranus", "meaning": "revolution"},
    0x2C: {"glyph": "⚷", "name": "neptune", "meaning": "dissolution"},
    0x2D: {"glyph": "⚸", "name": "pluto", "meaning": "transformation"},
    0x2E: {"glyph": "⚹", "name": "star_mult", "meaning": "multiplication"},
    0x2F: {"glyph": "⚺", "name": "sextile", "meaning": "60° phase"},
    
    # Operational glyphs
    0x30: {"glyph": "⚻", "name": "chiron", "meaning": "healing/bridge"},
    0x31: {"glyph": "⚼", "name": "ceres", "meaning": "nurture/growth"},
    0x32: {"glyph": "⚽", "name": "ball", "meaning": "dynamic object"},
    0x33: {"glyph": "⚾", "name": "baseball", "meaning": "trajectory"},
    0x34: {"glyph": "⚿", "name": "wheeled", "meaning": "rotation"},
    0x35: {"glyph": "⛀", "name": "die_1", "meaning": "quantum state 1"},
    0x36: {"glyph": "⛁", "name": "die_2", "meaning": "quantum state 2"},
    0x37: {"glyph": "⛂", "name": "die_3", "meaning": "quantum state 3"},
    0x38: {"glyph": "⛃", "name": "die_4", "meaning": "quantum state 4"},
    0x39: {"glyph": "⛄", "name": "snowman", "meaning": "cold state"},
    0x3A: {"glyph": "⛅", "name": "cloud", "meaning": "distributed"},
    0x3B: {"glyph": "⛆", "name": "rain", "meaning": "cascade"},
    0x3C: {"glyph": "⛇", "name": "snow", "meaning": "crystallize"},
    0x3D: {"glyph": "⛈", "name": "storm", "meaning": "chaos"},
    0x3E: {"glyph": "⛉", "name": "fog", "meaning": "uncertainty"},
    0x3F: {"glyph": "⛊", "name": "ice", "meaning": "frozen state"},
}


def get_glyph(index):
    """Get glyph by index (0-63)"""
    if not (0 <= index < 64):
        raise ValueError(f"Index must be 0-63, got {index}")
    return KHAOS_GLYPHS.get(index, KHAOS_GLYPHS[0x00])


def encode_state(state_value):
    """
    Encode a state value (0-63) as a glyph
    """
    return get_glyph(state_value % 64)


def decode_glyph_name(name):
    """
    Decode glyph name to index
    """
    for index, data in KHAOS_GLYPHS.items():
        if data['name'] == name:
            return index
    return None


def compose_sequence(indices):
    """
    Compose a sequence of glyphs from indices
    Returns string of glyphs
    """
    return ''.join([get_glyph(i)['glyph'] for i in indices])


def quantum_hash(input_string):
    """
    Generate a 64-state quantum hash from input string
    Returns index (0-63)
    """
    hash_value = 0
    for char in input_string:
        hash_value = (hash_value * 31 + ord(char)) % 64
    return hash_value


def state_tensor(state_a, state_b):
    """
    Compute tensor product of two quantum states
    Returns new state (0-63)
    """
    return (state_a * 8 + state_b) % 64


# Predefined symbolic sequences
SYMBOLIC_SEQUENCES = {
    "boot": [0x01, 0x04, 0x0F, 0x1F],  # genesis → orbit → bridge → circle
    "evolve": [0x05, 0x09, 0x0D, 0x12],  # flux → spiral → ascend → star
    "collapse": [0x0B, 0x02, 0x04, 0x00],  # split → collapse → orbit → void
    "entangle": [0x03, 0x1A, 0x22, 0x0C],  # entangle → duality → bond → merge
    "defend": [0x07, 0x15, 0x1D, 0x06],  # shield → warning → cross → mirror
}


def get_sequence(name):
    """Get predefined symbolic sequence"""
    return SYMBOLIC_SEQUENCES.get(name)


def format_sequence(name):
    """Format sequence with glyphs and meanings"""
    sequence = get_sequence(name)
    if not sequence:
        return f"Unknown sequence: {name}"
    
    lines = [f"\nSequence: {name}"]
    for i, idx in enumerate(sequence, 1):
        glyph_data = get_glyph(idx)
        lines.append(f"  {i}. {glyph_data['glyph']} {glyph_data['name']:<12} - {glyph_data['meaning']}")
    return '\n'.join(lines)


# Self-test
if __name__ == "__main__":
    print("TRIG6 KHAOS Domain Self-Test")
    print("=" * 70)
    
    print(f"\nTotal glyphs: {len(KHAOS_GLYPHS)}")
    print("\nFirst 16 primordial glyphs:")
    for i in range(16):
        data = get_glyph(i)
        print(f"  {i:02X}: {data['glyph']} {data['name']:<12} - {data['meaning']}")
    
    print("\n" + "=" * 70)
    print("\nSymbolic sequences:")
    for name in SYMBOLIC_SEQUENCES.keys():
        print(format_sequence(name))
    
    print("\n" + "=" * 70)
    print("\nQuantum hash examples:")
    for text in ["TRIG6", "KHAOS", "SAGCO"]:
        hash_val = quantum_hash(text)
        glyph = get_glyph(hash_val)
        print(f"  {text:<10} → {hash_val:02d} → {glyph['glyph']} ({glyph['name']})")
    
    print("\n" + "=" * 70)
    print("\nState tensor product:")
    a, b = 3, 5  # entangle, flux
    result = state_tensor(a, b)
    glyph_a = get_glyph(a)
    glyph_b = get_glyph(b)
    glyph_r = get_glyph(result)
    print(f"  {glyph_a['glyph']} ⊗ {glyph_b['glyph']} = {glyph_r['glyph']}")
    print(f"  {glyph_a['name']} ⊗ {glyph_b['name']} = {glyph_r['name']}")
