# moi-bid-defense

根据已完成的投标技术响应文件生成讲标答辩幻灯片。

## 快速开始

```bash
# Step 1: 解析响应文件
python3 scripts/parse_response.py 技术响应方案.md

# Step 2: 提取黄金线索
python3 scripts/extract_threads.py 技术响应方案.md --top 20

# Step 3+: 在 Claude Code 中调用 skill
/moi-bid-defense
```

## 与 moi-bid-response 的关系

```
moi-bid-response                    moi-bid-defense
   招标文件(.docx)                     响应文件(.md/.docx)
        |                                  |
        v                                  v
   技术响应文件 ------------------> 讲标答辩幻灯片
   (50,000+ 字)                    (15-20 页)
```

## 文件结构

```
moi-bid-defense/
├── SKILL.md                         # 主指令文件
├── README.md                        # 本文件
├── scripts/
│   ├── parse_response.py            # 响应文件解析器
│   └── extract_threads.py           # 黄金线索提取评分引擎
└── references/
    └── defense-strategy.md          # 讲标策略指南
```

## 核心算法

`extract_threads.py` 采用三维评分模型从数万字响应中提取讲标线索：

| 维度 | 权重 | 检测内容 |
|------|:---:|------|
| 痛点回应 | 1-3 分 | 一期不足、核心挑战、差异化需求、安全风险、监管合规 |
| 差异化亮点 | 2-4 分 | 独有技术、硬承诺、交付亮点、数据安全、架构前瞻 |
| 量化冲击力 | 1-2 分 | 段落中的数字指标密度 |

仅 >=3 分的段落入选黄金线索清单。

## 依赖

- Python 3.8+
- 可选：python-docx（如需解析 .docx 格式的响应文件）
- guizang-ppt skill（如需输出瑞士风/杂志风 HTML 幻灯片）
