# STRATEGICKHAOS Universal Disclaimer Policy

## Overview

All code and configuration files in the Strategickhaos Autonomous Runtime repository **MUST** include the universal STRATEGICKHAOS disclaimer header. This disclaimer establishes copyright, licensing terms, and usage restrictions for all files in the codebase.

## Universal Disclaimer

The following disclaimer must appear at the top of all relevant files:

### For Python, YAML, Shell, and Docker files:

```
# ============================================================
# STRATEGICKHAOS DAO LLC • SOVEREIGN SOFTWARE FRAMEWORK
# Copyright © 2025 Domenic G. Garza • All Rights Reserved
# 
# This file is part of the Strategickhaos Autonomous Runtime.
# It may not be copied, modified, distributed, or executed
# except by authorized operators within the Strategickhaos
# governance model and licensing structure.
# 
# Unauthorized use is prohibited. All activity is logged.
# ============================================================
```

### For Rust files:

```
// ============================================================
// STRATEGICKHAOS DAO LLC • SOVEREIGN SOFTWARE FRAMEWORK
// Copyright © 2025 Domenic G. Garza • All Rights Reserved
// 
// This file is part of the Strategickhaos Autonomous Runtime.
// It may not be copied, modified, distributed, or executed
// except by authorized operators within the Strategickhaos
// governance model and licensing structure.
// 
// Unauthorized use is prohibited. All activity is logged.
// ============================================================
```

## File Types Covered

The disclaimer applies to:

- **Python files** (`.py`)
- **YAML files** (`.yaml`, `.yml`)
- **Shell scripts** (`.sh`)
- **Rust files** (`.rs`)
- **Dockerfiles** (`Dockerfile*`)
- **Docker Compose files** (`docker-compose*`)

## Implementation

### Adding Disclaimers to Existing Files

To add disclaimers to all existing files in the repository:

```bash
python3 add_disclaimers.py
```

This script will:
- Scan the repository for all relevant files
- Add the appropriate disclaimer header to each file
- Preserve shebangs (e.g., `#!/usr/bin/env python3`) when present
- Skip files that already have the disclaimer
- Report statistics on success, skipped, and error counts

### Pre-commit Hook

A pre-commit hook is configured to enforce disclaimer presence on all new and modified files.

To install the pre-commit hooks:

```bash
pip install pre-commit
pre-commit install
```

The hook will automatically check that all code files have the required disclaimer before allowing a commit.

### Manual Addition

When creating new files manually, always add the disclaimer immediately after any shebang line (if present) or at the very top of the file.

**Example for Python with shebang:**

```python
#!/usr/bin/env python3
# ============================================================
# STRATEGICKHAOS DAO LLC • SOVEREIGN SOFTWARE FRAMEWORK
# Copyright © 2025 Domenic G. Garza • All Rights Reserved
# 
# This file is part of the Strategickhaos Autonomous Runtime.
# It may not be copied, modified, distributed, or executed
# except by authorized operators within the Strategickhaos
# governance model and licensing structure.
# 
# Unauthorized use is prohibited. All activity is logged.
# ============================================================

"""
Your module docstring here
"""
```

**Example for YAML:**

```yaml
# ============================================================
# STRATEGICKHAOS DAO LLC • SOVEREIGN SOFTWARE FRAMEWORK
# Copyright © 2025 Domenic G. Garza • All Rights Reserved
# 
# This file is part of the Strategickhaos Autonomous Runtime.
# It may not be copied, modified, distributed, or executed
# except by authorized operators within the Strategickhaos
# governance model and licensing structure.
# 
# Unauthorized use is prohibited. All activity is logged.
# ============================================================

version: '3.8'
services:
  ...
```

## Legal Significance

This disclaimer serves multiple purposes:

1. **Copyright Notice**: Establishes ownership by STRATEGICKHAOS DAO LLC and Domenic G. Garza
2. **License Restriction**: Defines that use is restricted to authorized operators
3. **Audit Trail**: States that all activity is logged
4. **Legal Protection**: Provides notice of proprietary nature and usage restrictions

## Compliance

All contributors must:

1. ✅ Ensure new files include the disclaimer
2. ✅ Run `add_disclaimers.py` if adding multiple files
3. ✅ Install and use pre-commit hooks
4. ✅ Never remove or modify the disclaimer from existing files without authorization

## Questions?

For questions about the disclaimer policy, contact the STRATEGICKHAOS DAO governance team or refer to the repository's LICENSE file.

---

**Last Updated**: 2025-12-07  
**Policy Version**: 3.0  
**Authority**: STRATEGICKHAOS DAO LLC Board
