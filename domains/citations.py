"""
Regulatory citations database
All standards cited with full references
"""

CITATIONS = {
    "rope.knot.figure_8_on_bight": {
        "name": "Figure 8 on a Bight",
        "description": "Loop knot with approximately 70-75% rope strength retention",
        "standard": "NFPA 1983",
        "title": "Standard on Life Safety Rope and Equipment for Emergency Services",
        "section": "4.4.2",
        "year": "2017",
        "strength_retention": "70-75%",
        "applications": ["Rescue operations", "Climbing", "Fall protection"],
        "citation": "NFPA 1983:2017 Section 4.4.2 - Life Safety Rope Performance"
    },
    "rope.knot.bowline": {
        "name": "Bowline",
        "description": "Fixed loop knot with approximately 60% rope strength retention",
        "standard": "NFPA 1983",
        "section": "4.4.2",
        "year": "2017",
        "strength_retention": "60%",
        "applications": ["General purpose loop", "Rescue"],
        "citation": "NFPA 1983:2017 Section 4.4.2"
    },
    "rigging.safety_factor": {
        "name": "Rigging Safety Factor",
        "description": "Minimum 5:1 safety factor for rigging and slings",
        "standard": "ASME B30.9",
        "title": "Slings",
        "section": "9-1.2.1",
        "year": "2018",
        "value": "5:1",
        "citation": "ASME B30.9-2018 Section 9-1.2.1 - Design Factor"
    },
    "fall_protection.anchor_strength": {
        "name": "Anchor Point Strength",
        "description": "Anchor points must support 5,000 lbs per attached worker",
        "standard": "OSHA 1926.502",
        "title": "Fall Protection Systems Criteria and Practices",
        "section": "(d)(15)",
        "year": "2023",
        "value": "5000 lbs",
        "citation": "29 CFR 1926.502(d)(15) - Anchorages"
    },
    "rope.working_load": {
        "name": "Working Load Limit",
        "description": "Maximum load that should be applied to rope in normal service",
        "standard": "OSHA 1926.251",
        "section": "(a)(1)",
        "year": "2023",
        "formula": "Breaking Strength / Safety Factor",
        "citation": "29 CFR 1926.251(a)(1) - Rigging Equipment for Material Handling"
    },
    "physics.gravity": {
        "name": "Standard Gravity",
        "description": "Standard acceleration due to gravity on Earth",
        "standard": "NIST SP 811",
        "title": "Guide for the Use of the International System of Units (SI)",
        "year": "2008",
        "value": "9.80665 m/s²",
        "citation": "NIST SP 811:2008 - Standard Gravity"
    }
}


def get_citation(key):
    """
    Retrieve a citation by key.
    
    Args:
        key: Citation key (e.g., 'rope.knot.figure_8_on_bight')
        
    Returns:
        Citation dictionary or None if not found
    """
    return CITATIONS.get(key)


def list_citations():
    """List all available citation keys"""
    return sorted(CITATIONS.keys())


def search_citations(query):
    """
    Search citations by keyword.
    
    Args:
        query: Search term
        
    Returns:
        List of matching citation keys
    """
    query_lower = query.lower()
    matches = []
    
    for key, data in CITATIONS.items():
        searchable = f"{key} {data.get('name', '')} {data.get('description', '')}".lower()
        if query_lower in searchable:
            matches.append(key)
    
    return sorted(matches)
