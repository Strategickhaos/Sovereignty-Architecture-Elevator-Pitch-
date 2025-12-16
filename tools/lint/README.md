# IAM Check Linter - Inheritance Trap Detector

## Purpose
Programmatically flag IAM permissions granted at Project level instead of Resource level.

## The IAM Inheritance Trap

**Bad (Project-level)**:
```
Project: my-project
  ├─ IAM: user@example.com = Editor  ❌ TOO BROAD!
  ├─ Resource: database
  └─ Resource: storage-bucket
```

**Good (Resource-level)**:
```
Project: my-project
  ├─ Resource: database
  │   └─ IAM: user@example.com = Editor ✅
  └─ Resource: storage-bucket
      └─ IAM: user@example.com = Viewer ✅
```

This linter enforces the good pattern.
