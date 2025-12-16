# Quarantine Zone

All 3rd party crates and libraries are isolated here until purified.

## Purpose

This directory enforces the **Axiom of Sovereignty**: No external code enters the system without审核 (audit).

## Process

1. **Intake**: New dependency arrives here
2. **Audit**: Security review and license check
3. **Purification**: Remove unnecessary code, verify integrity
4. **Integration**: Move to main dependency tree

## Status

Currently, we use Cargo's standard dependency management but maintain this directory for future manual auditing of critical dependencies.
