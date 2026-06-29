# Moi Bid Defense Skill · 讲标答辩幻灯片生成

![License](https://img.shields.io/badge/License-AGPL--3.0-blue?style=flat-square)
![Skill](https://img.shields.io/badge/Skill-Agent-111111?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Supported-6B5B95?style=flat-square)

一个适配 Claude Code 等 Agent 环境的讲标技能，用于从已完成的投标技术响应文件（md/docx）**自动生成讲标答辩幻灯片**（Markdown 大纲 + HTML 网页 PPT）。

核心流程：解析响应文件 → 黄金线索三维评分提取 → 按叙事策略编排幻灯片大纲 → 逐页编写（含讲标备注 + 预判 Q&A）→ 投喂版编辑（画面与备注分离）→ guizang-ppt 渲染为单文件 HTML。

> 由 [MoiTempete](https://github.com/MoiTempete) 基于真实化工安全生产信息化项目的中标讲标实践沉淀而成。
> HTML 渲染引擎由 [歸藏](https://github.com/op7418) 的 [guizang-ppt](https://github.com/op7418/guizang-ppt-skill) 提供（360 安全龙虾金牌赞助 / 真格 Token Grant 支持）。

## 30 秒开始

```bash
git clone https://github.com/MoiTempete/moi-bid-defense ~/.claude/skills/moi-bid-defense
```

也可以直接把这段话发给有 shell 权限的 AI Agent：

```text
帮我安装 moi-bid-defense skill。请把 https://github.com/MoiTempete/moi-bid-defense 克隆到 ~/.claude/skills/moi-bid-defense，安装完成后检查 SKILL.md、references/、scripts/ 是否存在。
```

已经安装过的话，用这段话更新：

```text
帮我更新 moi-bid-defense skill。请进入 ~/.claude/skills/moi-bid-defense 执行 git pull，然后告诉我当前最新 commit。
```

安装后直接对 Agent 说：

```text
帮我根据这份技术响应文件生成讲标幻灯片。
```

也可以试这些请求：

```text
分析这份响应文件，提取差异化亮点和量化指标。
生成 20 分钟讲标用的幻灯片大纲，确认结构后再逐页写。
把这些幻灯片渲染成瑞士风 HTML，投屏用。
```

## 效果

- 🔬 **黄金线索自动提取**：三维评分模型（痛点回应 + 差异化亮点 + 量化冲击力），从数万字响应中自动识别最具讲标价值的内容
- 🎬 **三种叙事策略**：技术纵深型 / 价值引领型 / 攻防兼备型，适配不同评委构成
- 📐 **幻灯片五元素模型**：每页 = 标题（判断句）+ 3-5 条要点 + 数据大字报 + 讲标备注 + 预判 Q&A
- 🎤 **讲标备注是灵魂**：语速提示、停顿点、眼神交流、备用素材——不是 PPT 大纲，是完整的演讲脚本
- ⚡ **Q&A 预判**：从响应文件中识别可能被追问的点，准备诚实具体的应答
- 🎨 **瑞士国际主义风 HTML**：无衬线、IKB 克莱因蓝、网格点阵、Data Hero 大字报——单文件 HTML，浏览器即开即用
- 📱 **横向翻页交互**：键盘 ← →、滚轮、触屏滑动、ESC 缩略图索引、B 键低功耗模式

## 适合 / 不适合

**✅ 合适**：投标讲标答辩、技术方案汇报、产品发布会、行业分享——需要从长篇技术文档中提炼亮点做口头演讲的场景

**❌ 不合适**：培训课件（信息密度需要更高）、大段数据表格展示（用常规 PPT 更合适）、多人协作编辑（这是静态 HTML）、纯设计排版型演示

## 常见使用场景

| 任务 | 推荐方式 |
|------|---------|
| 投标讲标，评委以技术专家为主 | 选策略 1（技术纵深型），架构→核心技术→性能举证 |
| 投标讲标，评委以商务领导为主 | 选策略 2（价值引领型），共鸣→价值→场景→承诺 |
| 不确定评委构成（默认） | 选策略 3（攻防兼备型），需求→架构→亮点深讲→信任建立 |
| 15 分钟短讲 | 12-15 页，数据大字报每页一个 |
| 20 分钟标准 | 15-20 页，3-4 个亮点模块深讲 |
| 30 分钟详细 | 20-28 页，可加入现场演示环节 |
| 想要杂志感 / 人文风 | 输出风格选"电子杂志风"（guizang-ppt 风格 A） |
| 想要科技感 / 数据驱动 | 输出风格选"瑞士国际主义"（guizang-ppt 风格 B，默认） |
| 只想要 Markdown 大纲 | 运行到 Step 4 即可，不进入 HTML 渲染 |
| 用 PowerPoint 编辑 | 选标准 PPTX 输出，后续在 PowerPoint/WPS 中手工调整 |

## 为什么是 Agent Skill

- **数万字→十几页的压缩需要判断力**：不是简单的摘要，需要识别"评委最想听什么"，Agent 的上下文理解比脚本规则更灵活
- **讲标备注是人力密集型工作**：停顿点、眼神交流、备用素材——这些传统上需要讲标人反复排练才能写出来，Agent 可以自动生成高质量初稿
- **Q&A 预判需要"反向思维"**：从响应中识别薄弱点和争议点，模拟评委视角追问——这是 Agent 的强项
- **逐页确认更安全**：讲标内容容错率低，人机协作逐页确认保障质量
- **HTML 渲染完全自动化**：从 Markdown 到可播放的网页 PPT，不需要打开任何设计工具

## 安装

### 方式一：命令行安装（推荐）

```bash
git clone https://github.com/MoiTempete/moi-bid-defense ~/.claude/skills/moi-bid-defense
```

### 方式二：把下面这段话直接发给 AI

> 帮我安装 `moi-bid-defense` 这个 Claude Code skill。请按下面步骤做：
>
> 1. 确保 `~/.claude/skills/` 目录存在（不存在就创建）
> 2. 执行 `git clone https://github.com/MoiTempete/moi-bid-defense.git ~/.claude/skills/moi-bid-defense`
> 3. 验证：`ls ~/.claude/skills/moi-bid-defense/` 应该看到 `SKILL.md`、`references/`、`scripts/` 三项
> 4. 告诉我安装好了，之后我说"生成讲标 PPT"之类的话就会触发这个 skill

把这段话复制粘贴给 Claude Code / Cursor / 任何有 shell 权限的 AI Agent，它会自动完成安装。

### 方式三：通过 moi-bid-response 自动引导

如果已安装 `moi-bid-response`，技术响应文件生成完毕后会自动询问是否需要生成述标 PPT，并引导安装 `moi-bid-defense`。

### HTML 渲染引擎安装

`moi-bid-defense` 首次生成 HTML 幻灯片时会自动引导安装 guizang-ppt：

```bash
npx skills add https://github.com/op7418/guizang-ppt-skill --skill guizang-ppt-skill
```

### 触发方式

装好后，Claude Code 会在对话里自动发现并调用这个 skill。触发关键词：

- "帮我生成讲标幻灯片"
- "根据响应文件做述标 PPT"
- "技术方案汇报 PPT"
- "投标答辩演示"
- "defense presentation"
- "bid defense slides"

## 使用流程

Skill 本身是结构化工作流，Agent 会逐步引导：

1. **解析响应文件** — 运行 `parse_response.py` 提取章节结构、★ 引用、量化指标分布
2. **风格配置** — 确认叙事策略（1/2/3）、讲标时长（15/20/30 min）、输出风格（瑞士/杂志/PPTX）
3. **黄金线索提取 + 大纲生成** — 运行 `extract_threads.py` → 按叙事策略编排 15-20 页幻灯片结构，等用户确认
4. **逐页编写幻灯片** — 每页包含标题（判断句）、要点、数据大字报、讲标备注、预判 Q&A，逐页确认
5. **输出幻灯片** — Markdown 大纲 → 投喂版编辑（画面与备注分离）→ guizang-ppt 渲染 HTML → 逐页检查修复

详细说明见 [`SKILL.md`](./SKILL.md)。

## 三种叙事策略

| 策略 | 适用场景 | 叙事节奏 |
|------|---------|---------|
| **1. 技术纵深型** | 评委以技术专家为主 | 痛点切入→架构总览→核心技术逐层展开→性能举证→实施保障 |
| **2. 价值引领型** | 评委以商务领导为主 | 需求共鸣→核心价值→关键场景演示→服务承诺→案例佐证 |
| **3. 攻防兼备型**（默认） | 混合评委 / 不确定 | 需求→架构一览→3-4 亮点深讲→一期继承→实施→服务→Q&A |

## 幻灯片五元素模型

每页幻灯片由五个元素构成：

| 元素 | 说明 | 示例 |
|------|------|------|
| **标题** | 完整的判断句或核心主张 | "AI 三大能力中枢——全私有化部署，甲方可自主训练" |
| **要点** | 3-5 条，每条不超过两行，用数字和动词驱动 | "12 类视频 AI 算法：明火 ≥98%、烟雾 ≥95%、安全帽 ≥97%" |
| **数据大字报** | 1 个最核心的数字，Data Hero 布局放大展示 | **0 条数据出内网** — 全部推理在本地 GPU 上完成 |
| **讲标备注** | 给演讲者的提示：语速、停顿、眼神、备用素材 | "此处停顿 2 秒，目光扫过评委席，然后说——" |
| **预判 Q&A** | 1-2 个评委可能追问的问题及应答要点 | "Q: GPU 成本多少？A: 训练用一张 A100-80G 即可起步，约 8-10 万" |

## 黄金线索三维评分模型

`extract_threads.py` 的核心算法，从数万字响应中提取最具讲标价值的内容：

| 维度 | 分值 | 检测内容 |
|------|:---:|------|
| **痛点回应** | 1-4 分 | 一期不足 +3、核心挑战 +2、差异化需求 +2、H₂S/爆炸等安全风险 +2、监管合规 +1、系统异构 +1 |
| **差异化亮点** | 2-4 分 | 独有技术 +4、硬承诺（费用全包/知识产权归甲方）+3、训练平台/源代码交付 +3、私有化部署 +2、架构前瞻 +2、标准领先 +2 |
| **量化冲击力** | 1-2 分 | 段落含 4+ 个量化指标 +2、含 2-3 个 +1 |
| **扣分** | -2 分 | 纯模板套话且无差异化标签 |

仅 ≥3 分的段落入选"黄金线索"清单，按得分降序排列供幻灯片编排。

## 目录结构

```
moi-bid-defense/
├── SKILL.md                         ← Skill 主文件：工作流、原则、常见错误
├── README.md                        ← 本文件
├── CONTRIBUTING.md                  ← 贡献指南
├── LICENSE                          ← AGPL-3.0
├── .github/
│   ├── pull_request_template.md
│   └── ISSUE_TEMPLATE/
│       ├── config.yml
│       ├── bug_report.yml
│       └── feature_request.yml
├── scripts/
│   ├── parse_response.py            ← 响应文件解析脚本（md/docx → 结构 + 指标）
│   └── extract_threads.py           ← 黄金线索提取评分引擎（三维评分 + 主题分类）
└── references/
    └── defense-strategy.md          ← 讲标策略指南（叙事策略/时间分配/评委心理/Q&A预判）
```

## 核心编写原则

1. **标题即主张**：每页标题必须是完整的判断句，听众只读标题也能把握要点
2. **黄金线索驱动**：幻灯片内容必须以提取脚本的评分排序结果为素材基础，不凭空编造
3. **口语化**：书面语转口语——"我方郑重承诺"→"我们承诺"，"本项目"→"这个项目"
4. **一页一个核心数字**：每页只放大一个最核心的量化指标，用 Data Hero 布局展示
5. **讲标备注必写**：这是区别于普通 PPT 大纲的核心差异化——停顿点、语速、眼神、备用素材
6. **Q&A 预判要诚实**：不确定的就说需要书面补充，不强行编造答案
7. **幻灯片与备注严格分离**：生成 HTML 前编辑投喂版 Markdown——画面内容进幻灯片，备注和 Q&A 不渲染
8. **生成后逐页检查**：内容稀疏的补、字号过小的放大、颜色不可读的修复

## Roadmap

- 支持更多 HTML 幻灯片风格（暗色主题、赛博朋克等）
- PPTX 格式直接输出（跳过 HTML 步骤）
- 讲标排练模式（计时器 + 自动提词）
- 基于真实讲标录音的多模态反馈优化
- 行业讲标模板库（信息化 / 安全 / 设备采购 / 工程服务）

## FAQ

**和 moi-bid-response 是什么关系？**
`moi-bid-response` 生成技术响应文件（docx），`moi-bid-defense` 把响应文件转化为讲标幻灯片（HTML）。两者是投标工作流的前后环节。`moi-bid-response` 完成后会自动建议启动 `moi-bid-defense`。

**生成的 HTML 能在 PowerPoint 里编辑吗？**
不能直接编辑。HTML 是网页格式，适合投屏播放。如果需要 PowerPoint 编辑，在 Step 2 选"标准 PPTX"输出格式。

**讲标备注是谁写的？**
Agent 基于响应文件内容和讲标策略指南自动生成。包括语速提示、停顿点、眼神交流时机、备用素材建议——相当于一个有经验的讲标教练帮你标注的脚本。

**Q&A 预判准确吗？**
预判基于响应文件中"可能引起质疑"的技术选型、性能指标、交付承诺等信号点识别。你可以人工审核和调整。

**怎么更新到最新版？**
在本地 skill 目录执行 `git pull`。

## 贡献

Bug、提取质量问题、新叙事策略需求——欢迎开 Issue 或 PR。改动请优先：

- 在 `scripts/extract_threads.py` 中优化评分规则和主题分类逻辑
- 在 `references/defense-strategy.md` 中补充新的讲标策略和 Q&A 模板
- 脚本改动需保持 JSON 输入输出接口兼容
- 工作流改动不能移除用户确认闸门（Step 2 / Step 3 / 逐页确认）

详见 [`CONTRIBUTING.md`](./CONTRIBUTING.md)。

## 关联 Skills

### 上游 — 技术响应文件生成

**[`moi-bid-response`](https://github.com/MoiTempete/moi-bid-response)** — 从招标技术规格书自动编写投标技术响应文件。完成响应文件输出后会自动建议启动 `moi-bid-defense`。

```bash
npx skills add https://github.com/MoiTempete/moi-bid-response --skill moi-bid-response
```

### 渲染引擎 — HTML 幻灯片

**[`guizang-ppt`](https://github.com/op7418/guizang-ppt-skill)** — 单文件 HTML 横向翻页 PPT，提供瑞士国际主义和电子杂志两套视觉系统。`moi-bid-defense` 首次渲染时会自动引导安装。

```bash
npx skills add https://github.com/op7418/guizang-ppt-skill --skill guizang-ppt-skill
```

**完整链路**：招标文件 (.docx) → `moi-bid-response` → 技术响应 (.docx/.md) → `moi-bid-defense` → 讲标幻灯片 (.html)

## 更新日志

### 2026-06-29

**SKILL.md 工作流完善**

- Step 5 从 12 行扩充到 ~90 行，新增投喂版 Markdown 编辑（5b）、guizang-ppt 自动安装与调用（5c）、输出文件清单（5d）
- 新增 5 条关键规则（11-15）：主动建议 HTML 生成、guizang-ppt 自动安装、画面与备注分离、生成后逐页检查、支持用户指定工具
- Step 2 输出风格选项新增 guizang-ppt 推荐说明

**extract_threads.py 评分算法 V2**

- 评分模型从"量化密度优先"重构为"痛点回应 + 差异化亮点 + 量化冲击力"三维模型
- 新增 16 条痛点检测规则（一期不足 +3、安全风险 +2、监管合规 +1 等）
- 新增 9 条差异化检测规则（独有技术 +4、硬承诺 +3、交付亮点 +3 等）
- 扣分机制：纯模板套话且无差异化标签 -2 分
- 主题分类函数重构为优先级匹配（具体主题先于宽泛主题），避免安全业务内容被误分为"理解与定位"

**guizang-ppt 集成实战验证**

- 使用广汇能源安全生产信息化二期响应文件（53,066 字）完整跑通全流程
- 生成 18 页瑞士国际主义风 HTML 幻灯片，经多轮修复（深色底改白底、稀疏页补内容、字号放大）
- 沉淀实战经验写入 SKILL.md 关键规则 14

**README.md 重构**

- 从 59 行扩充到 220+ 行，对齐 moi-bid-response README 的结构和深度
- 新增：badges、适合/不适合、常见使用场景表、三种叙事策略表、五元素模型、安装三种方式、FAQ、Roadmap、关联 Skills

**项目基建对齐**

- 新增 CONTRIBUTING.md（bug 报告/PR 指南/设计决策说明）
- 新增 .github/ISSUE_TEMPLATE/（bug_report.yml + feature_request.yml + config.yml）
- 新增 .github/pull_request_template.md
- LICENSE 采用 AGPL-3.0（与 moi-bid-response 一致）

**moi-bid-response 联动更新**

- 新增 Step 6：完成后主动询问是否生成述标 PPT，自动检查/安装 moi-bid-defense
- README 新增「关联 Skills」章节，标注完整链路
- 新增关键规则 12：完成后主动建议述标 PPT

## License

AGPL-3.0 © 2026 [MoiTempete](https://github.com/MoiTempete)

---

> HTML 渲染引擎 [guizang-ppt](https://github.com/op7418/guizang-ppt-skill) 由 [歸藏](https://x.com/op7418) 创建维护。本项目仅集成调用，不包含 guizang-ppt 代码。
