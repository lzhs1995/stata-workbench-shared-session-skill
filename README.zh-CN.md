# Stata Workbench Shared Session — 操作 skill

<img src="media/icon.png" alt="操作 skill 图标：带勾号的指南页" width="96">

[English](README.md) | 简体中文 | [繁體中文](README.zh-TW.md)

给 agent 用的操作 skill：agent 在用户已有的
[Stata Workbench Shared Session](https://github.com/lzhs1995/stata-workbench-shared-session)
里运行 Stata，人和 agent 共用同一个可见的 Stata 会话。

本版对应 runtime **v0.1.3-rc.7.45**（pre-release）。版本锁定值、平台结果和 agent 路线写在
`runtime-compatibility.json` 里；CI 用这个 tag 的 runtime checkout 检查 skill。

从 [SKILL.md](skills/stata-workbench-shared-session/SKILL.md) 开始读。它按使用顺序排列：
runtime 是什么、谁来运行代码、macOS 和 Windows 上的三分钟上手、客户端的全部选项、Stop、
回执和退出码、故障排查、已知限制和平台说明。references 讲分阶段工作、回执、保留作者的
`.do` 文件、存储、导出、重跑和桌面恢复。SKILL.md 只有英文版，内容以它为准。

agent 先看 [AGENTS.md](AGENTS.md)：哪类任务读哪个文件。

## 安装 skill

安装与 runtime 分开：它不会更新 Workbench、重启 backend，也不会联系别的 agent。

```sh
python3 -B scripts/install.py --prefix /absolute/skill-storage
# 先看它打算做的改动，再执行：
python3 -B scripts/install.py --prefix /absolute/skill-storage --apply
```

安装器把 skill 和回执检查脚本复制到 `<prefix>/<skillVersion>/`，再把 Claude、Codex 和
`.agents` 的 skill 路径指向它。原有路径保留为带时间戳的备份；已有的版本目录永远不会被覆盖。

## 检查

```sh
python3 -B -m unittest discover -s tests
# 有锁定 tag 的 runtime checkout 时：
STATA_WORKBENCH_RUNTIME=/abs/runtime python3 -B -m unittest discover -s tests
python3 -B scripts/runtime_contract_check.py --runtime-root /abs/runtime
# 再用发布的 VSIX 核对它的锁定值：
python3 -B scripts/runtime_contract_check.py --runtime-root /abs/runtime --vsix /abs/stata-workbench-shared-session-0.1.3-rc.7.45.vsix
```

以下情况 `runtime_contract_check.py` 判失败：SKILL.md、references、任一 README 或 AGENTS.md
提到了锁定 runtime 没有的客户端选项或 `stata-workbench.*` 命令；锁定值与 checkout 不一致（版本、
tag、bundle、客户端常量，runtime 目录是 git checkout 时还有 tag 对应的提交）；什么都没检查到。
`vsixSha256` 只和 `--vsix` 给出的文件比对。没能比对的锁定值列在 `notChecked` 里。

本仓库只有操作指南、离线检查器和合成测试。不要加入研究数据、回执、私人备份或凭据。
