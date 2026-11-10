# Stata Workbench Shared Session — operating skill

<img src="media/icon.png" alt="Operating skill icon: a guide page with a check mark" width="96">

English | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md)

Operating skill for agents that run Stata in the user's existing
[Stata Workbench Shared Session](https://github.com/lzhs1995/stata-workbench-shared-session),
so that the person and the agent share one visible Stata session.

This version describes runtime **v0.1.3-rc.7.45** (pre-release). Pins, platform
results and the agent route are in `runtime-compatibility.json`; CI checks the
skill against a checkout of that tag.

Start with [SKILL.md](skills/stata-workbench-shared-session/SKILL.md). It is
ordered for use: what the runtime is, who runs the code, a three-minute start on
macOS and Windows, the full client options, Stop, receipts and exit codes,
troubleshooting, known limitations and platform notes. The references cover
staged work, receipts, author DO preservation, storage, exports, replay and
desktop recovery.

Agents: [AGENTS.md](AGENTS.md) lists which file to read for which task.

<!-- portfolio-stata-navigation-20261110 -->
## Project family · 專案導覽

| Repository | Role · 角色 |
| --- | --- |
| [Shared Session](https://github.com/lzhs1995/stata-workbench-shared-session) | Current runtime line and versioned releases · 現役執行環境與版本發行 |
| [Operating skill](https://github.com/lzhs1995/stata-workbench-shared-session-skill) | Separately versioned agent guidance and runtime compatibility checks · 獨立版本的代理操作指南與執行環境相容檢查 |
| [Next](https://github.com/lzhs1995/stata-workbench-next) | Preview development line with isolated profiles and ports · 使用獨立設定與連接埠的開發預覽版 |

These repositories have different roles and release cycles. Use the runtime and
skill versions named by their compatibility records; Next remains a separate
preview and does not replace an existing research session.

三個倉庫各自維護版本。請依相容紀錄選用執行環境與操作技能；Next 為獨立預覽版，
不會取代現有的研究工作階段。
<!-- /portfolio-stata-navigation-20261110 -->

## Install the skill

Installation is separate from the runtime: it never updates Workbench, restarts
a backend or contacts another agent.

```sh
python3 -B scripts/install.py --prefix /absolute/skill-storage
# Inspect the proposed changes, then:
python3 -B scripts/install.py --prefix /absolute/skill-storage --apply
```

The installer copies the skill and its receipt checkers into
`<prefix>/<skillVersion>/`, then points the Claude, Codex and `.agents` skill
routes at it. Existing routes are kept as timestamped backups; an existing
version directory is never overwritten.

## Checks

```sh
python3 -B -m unittest discover -s tests
# With a runtime checkout at the pinned tag:
STATA_WORKBENCH_RUNTIME=/abs/runtime python3 -B -m unittest discover -s tests
python3 -B scripts/runtime_contract_check.py --runtime-root /abs/runtime
# Also compare the released VSIX with its pin:
python3 -B scripts/runtime_contract_check.py --runtime-root /abs/runtime --vsix /abs/stata-workbench-shared-session-0.1.3-rc.7.45.vsix
```

`runtime_contract_check.py` fails when SKILL.md, its references, a README or
AGENTS.md mentions a client option or a `stata-workbench.*` command that the
pinned runtime does not have, when a pin differs from the checkout (version,
tag, bundle, client constants, and the tag commit when the runtime root is a git
checkout), or when it checked nothing. `vsixSha256` is compared only with a
file passed by `--vsix`. Pins it could not compare are listed in `notChecked`.

This repository contains operating guidance, offline checkers and synthetic
tests only. Never add research data, receipts, private backups or credentials.
