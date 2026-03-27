# failures.md

## Purpose
Track failed attempts so retries do not repeat the same bad reasoning.

## Template

### [DATE/TIME] <TASK-ID>
**What failed**
- 

**Root cause**
- 

**Do not retry**
- 

**Correct next action**
- 

---

## Example

### 2026-03-27 ST-002
**What failed**
- Checked free disk space on every cache write.

**Root cause**
- Added too much overhead to hot IO path.

**Do not retry**
- Per-write free-space checks in hot path.

**Correct next action**
- Use periodic disk polling + threshold-based enable/disable.
