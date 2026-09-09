# Stata Workbench Shared Session — operating skill

Independent, versioned operating protocol for automatic visible human/AI Stata
work. Runtime: https://github.com/lzhs1995/stata-workbench-shared-session.

**Development candidate, not a new formal acceptance.** Requires the runtime
`visible-cowork/1` protocol. Old transport-only PASS cannot certify this workflow.

Start with [SKILL.md](skills/stata-workbench-shared-session/SKILL.md).
No per-stage approval prompts: user interventions are explicit controls.
The exact execution do-file and real Stata Terminal must be visible side by side.

Installation is separate from runtime deployment:

```sh
python3 -B scripts/install.py --prefix /absolute/skill-storage
# Inspect the proposed changes, then:
python3 -B scripts/install.py --prefix /absolute/skill-storage --apply
```

Installer preserves prior Claude/Codex/.agents routes in timestamped backups,
never updates Workbench, restarts a backend or contacts another agent.
Run `python3 -B -m unittest discover -s tests` for local harness tests.
Version and platform limits are in `runtime-compatibility.json`.

Repository contains operational code and synthetic tests only. Never add research
data, local receipts, private backup files or credentials to public commits.
