"""
TRIG6 Citations & Provenance Module
Every constant has provenance
"""


class Citation:
    """Citation for a constant or model"""
    
    def __init__(self, key, value, sources, description=None):
        self.key = key
        self.value = value
        self.sources = sources if isinstance(sources, list) else [sources]
        self.description = description
    
    def format(self):
        """Format citation for display"""
        lines = []
        lines.append(f"\nCITATION: {self.key}")
        lines.append(f"VALUE: {self.value}")
        if self.description:
            lines.append(f"DESCRIPTION: {self.description}")
        lines.append("SOURCES:")
        for i, source in enumerate(self.sources, 1):
            lines.append(f"  [{i}] {source.get('title', 'Unknown')}")
            if 'publisher' in source:
                lines.append(f"      Publisher: {source['publisher']}")
            if 'section' in source:
                lines.append(f"      Section: {source['section']}")
            if 'url' in source:
                lines.append(f"      URL: {source['url']}")
            if 'year' in source:
                lines.append(f"      Year: {source['year']}")
        return '\n'.join(lines)


# Citation database
CITATIONS = {
    # Rope constants
    "rope.knot.figure_8_on_bight": Citation(
        key="rope.knot.figure_8_on_bight",
        value="0.75-0.80 (strength retention)",
        description="Figure 8 on a bight knot strength efficiency",
        sources=[
            {
                "title": "Sterling Rope Technical Manual",
                "publisher": "Sterling Rope Company",
                "section": "Knot Efficiency Charts",
                "url": "https://sterlingrope.com"
            },
            {
                "title": "Petzl Technical Information",
                "publisher": "Petzl",
                "section": "Knot Strength Data"
            }
        ]
    ),
    "rope.material.nylon.tensile_strength": Citation(
        key="rope.material.nylon.tensile_strength",
        value="9000 lbf (typical for 11mm rope)",
        description="Tensile strength of nylon rope",
        sources=[
            {
                "title": "SPRAT Safe Practices for Rope Access Work",
                "publisher": "Society of Professional Rope Access Technicians",
                "section": "Equipment Standards",
                "year": "2023",
                "url": "https://sprat.org"
            }
        ]
    ),
    "rope.safety_factor": Citation(
        key="rope.safety_factor",
        value="15:1 for life safety applications",
        description="Required safety factor for rope access work",
        sources=[
            {
                "title": "OSHA 1926 Subpart M",
                "publisher": "Occupational Safety and Health Administration",
                "section": "Fall Protection",
                "url": "https://www.osha.gov"
            },
            {
                "title": "SPRAT Safe Practices",
                "publisher": "SPRAT",
                "section": "3.4.2 Rope Specifications"
            }
        ]
    ),
    
    # Pipe constants
    "pipe.pressure.asme_b31.3": Citation(
        key="pipe.pressure.asme_b31.3",
        value="P = 2SEt / (D - 2Yt)",
        description="ASME B31.3 pipe pressure formula",
        sources=[
            {
                "title": "ASME B31.3 Process Piping",
                "publisher": "American Society of Mechanical Engineers",
                "section": "304.1.2 Straight Pipe Under Internal Pressure",
                "year": "2022"
            }
        ]
    ),
    "pipe.api_gravity": Citation(
        key="pipe.api_gravity",
        value="API Gravity = (141.5 / SG at 60°F) - 131.5",
        description="API gravity formula for petroleum products",
        sources=[
            {
                "title": "API Manual of Petroleum Measurement Standards",
                "publisher": "American Petroleum Institute",
                "section": "Chapter 11.1",
                "year": "2021"
            }
        ]
    ),
    
    # Rigging constants
    "rigging.design_factor": Citation(
        key="rigging.design_factor",
        value="5:1 minimum for overhead lifting",
        description="Design factor for rigging equipment",
        sources=[
            {
                "title": "ASME B30.9 Slings",
                "publisher": "American Society of Mechanical Engineers",
                "section": "9-1.2.2 Design Factor",
                "year": "2021"
            }
        ]
    ),
    "rigging.hoist.speed_limit": Citation(
        key="rigging.hoist.speed_limit",
        value="120 feet per minute (maximum)",
        description="Maximum hoisting speed for personnel",
        sources=[
            {
                "title": "ASME B30.23 Personnel Lifting Systems",
                "publisher": "ASME",
                "section": "23-2.2.3"
            }
        ]
    ),
    
    # Physics models
    "model.bridle_two_leg_equal_angle": Citation(
        key="model.bridle_two_leg_equal_angle",
        value="T = W / (2 * cos(θ))",
        description="Tension in two-leg bridle with equal angles",
        sources=[
            {
                "title": "Engineering Mechanics: Statics",
                "publisher": "J.L. Meriam & L.G. Kraige",
                "section": "Chapter 3: Equilibrium of Force Systems",
                "year": "2016"
            }
        ]
    ),
    "model.highline_tension": Citation(
        key="model.highline_tension",
        value="T = W * (L / (8 * sag))",
        description="Tension in highline based on sag",
        sources=[
            {
                "title": "CMC Rope Rescue Manual",
                "publisher": "CMC Rescue",
                "section": "Chapter 8: Highline Systems"
            }
        ]
    ),
    "model.fall_impact_force": Citation(
        key="model.fall_impact_force",
        value="F = W * (1 + √(1 + 2h/d))",
        description="Impact force calculation for fall arrest",
        sources=[
            {
                "title": "ANSI Z359.1 Fall Protection Code",
                "publisher": "American National Standards Institute",
                "section": "Appendix C: Fall Arrest Force Calculations",
                "year": "2016"
            }
        ]
    )
}


def get_citation(key):
    """Get citation by key"""
    return CITATIONS.get(key)


def list_citations():
    """List all available citations"""
    return list(CITATIONS.keys())


def search_citations(query):
    """Search citations by keyword"""
    query_lower = query.lower()
    results = []
    for key, citation in CITATIONS.items():
        if (query_lower in key.lower() or 
            query_lower in str(citation.value).lower() or
            (citation.description and query_lower in citation.description.lower())):
            results.append(key)
    return results


# Self-test
if __name__ == "__main__":
    print("TRIG6 Citations Module Self-Test")
    print("=" * 70)
    
    # Test getting a citation
    cite = get_citation("rope.knot.figure_8_on_bight")
    if cite:
        print(cite.format())
    
    print("\n" + "=" * 70)
    print(f"\nTotal citations: {len(CITATIONS)}")
    print("\nAvailable citation keys:")
    for key in sorted(list_citations()):
        print(f"  - {key}")
    
    print("\n" + "=" * 70)
    print("\nSearch for 'rope':")
    for key in search_citations("rope"):
        print(f"  - {key}")
