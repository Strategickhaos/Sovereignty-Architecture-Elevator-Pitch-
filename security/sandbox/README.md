# Black Hole Sandbox - Process Isolation

## Purpose
Isolate suspicious processes in a vacuum to study their behavior before termination.

## The Black Hole Algorithm

1. Detect suspicious process
2. Create isolated namespace (no network, no filesystem)
3. Move process into black hole
4. Study behavior (syscalls, network attempts, file access)
5. Generate behavior report
6. Terminate process
7. Add signature to immunity ledger

Processes never "escape" the black hole.
