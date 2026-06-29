#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄金线索提取器 — moi-bid-defense 核心评分引擎

从投标技术响应文件（Markdown）中提取最具讲标价值的内容线索，
按"痛点回应 + 差异化亮点 + 量化冲击力"三维模型评分排序。

用法：
    python3 extract_threads.py <响应文件.md> [--top N] [--json]

输出：
    默认：按评分排序的黄金线索清单（含得分、标签、原文摘要）+ 主题分布统计
    --json：输出为 JSON 格式，供 LLM 进一步处理
    --top N：仅输出前 N 条线索（默认 25）
"""

import re
import sys
import json
import argparse


def score_paragraph(text):
    """
    对单个段落进行三维评分。
    返回 (score, tags)，其中 tags 是命中标签的列表。
    """
    score = 0
    tags = []

    # ============================================================
    # 维度 1 — 痛点回应 (Pain Point Response)
    # ============================================================
    pain_patterns = [
        # (正则, 加分, 标签)
        (r'一期.*(?:不足|局限|无法|难以|缺失|信息孤岛|数据孤)', 3, '一期痛点'),
        (r'(?:挑战|难点|关键.*在于|核心.*在于|本质)', 2, '核心挑战'),
        (r'(?:差异化|各分公司.*不同|各不相同|特殊|特有|专项)', 2, '差异化需求'),
        (r'(?:H[₂2]S|硫化氢|剧毒|爆炸|泄漏|事故|风险)', 2, '安全风险'),
        (r'(?:600公里|地理跨度|两地)', 1, '地域特征'),
        (r'政府.*(?:监管|平台|上报|对接|合规)', 1, '监管合规'),
        (r'(?:现有.*系统|老旧|异构|不同厂商|不同协议)', 1, '系统异构'),
    ]
    for pattern, pts, tag in pain_patterns:
        if re.search(pattern, text):
            score += pts
            if tag not in tags:
                tags.append(tag)

    # ============================================================
    # 维度 2 — 差异化亮点 (Differentiation)
    # ============================================================
    diff_patterns = [
        (r'(?:我方|我们).*(?:独有|自主.*研发|创新|首创|领先|率先)', 4, '独有优势'),
        (r'(?:郑重承诺|保证|确保).*(?:不收取|免费|终身|全部.*承担)', 3, '硬承诺'),
        (r'(?:训练平台.*交付|源代码.*交付|知识产权.*归.*甲方)', 3, '交付亮点'),
        (r'(?:私有化部署|不出.*内网|本地.*完成|不依赖.*外部)', 2, '数据安全'),
        (r'设计容量.*200%|不.*架构.*变更.*可支撑|线性扩展', 2, '架构前瞻'),
        (r'(?:五横两纵|云边协同|灰度迁移|滚动.*不中断)', 2, '架构创新'),
        (r'(?:零代码|低代码|拖拽|可视化.*配置|无需编码)', 2, '易用性'),
        (r'(?:推倒重建|严格.*GB\s*30871|LEC.*LS.*双引擎)', 2, '标准领先'),
        (r'(?:季度.*迭代|增量训练|自动.*优化|持续.*提升)', 2, '持续进化'),
    ]
    for pattern, pts, tag in diff_patterns:
        if re.search(pattern, text):
            score += pts
            if tag not in tags:
                tags.append(tag)

    # ============================================================
    # 维度 3 — 量化冲击力 (Quantitative Impact)
    # ============================================================
    metric_pattern = re.compile(
        r'\d+[%％]|[≥≤]\d+%?|\d+\s*(?:万|亿|路|套|种|类|个|层|级|张|次|秒|分钟|小时|天|月|年|ms|Mbps|Gbps|FPS|QPS|GB|TB|MB)'
    )
    metrics = metric_pattern.findall(text)
    if len(metrics) >= 4:
        score += 2
        tags.append(f'{len(metrics)}项指标')
    elif len(metrics) >= 2:
        score += 1
        tags.append(f'{len(metrics)}项指标')

    # ============================================================
    # 扣分项 — 模板套话
    # ============================================================
    boilerplate = re.findall(r'满足.*要求|符合.*规范|遵循.*标准|严格按|依照.*规定', text)
    has_high_value_tag = any(t in ['独有优势', '硬承诺', '交付亮点'] for t in tags)
    if boilerplate and len(metrics) == 0 and not has_high_value_tag:
        score -= 2

    return score, tags


def classify_theme(tags, text):
    """将线索归类到主题。优先级：越具体的主题越先匹配。"""
    combined = ' '.join(tags) + ' ' + text
    # 先匹配最具体的主题（避免被宽泛关键词误分类）
    if any(w in combined for w in ['数字孪生', '三维建模', '渲染', 'UE5', 'Pixel Streaming']):
        return '数字孪生'
    if any(w in combined for w in ['视频智能分析', '视频AI', '摄像机', 'NVR', 'IPC', '布控球', '抽帧']):
        return 'AI智能化'
    if any(w in combined for w in ['RAG', '大语言模型', 'LLM', '私有化部署', 'Embedding', '知识库']):
        return 'AI智能化'
    if any(w in combined for w in ['巡检', '操作卡', '作业票', '双重预防', '责任制', '承包商', '安全培训', '安全基础', '个人工作台']):
        return '安全生产业务'
    if any(w in combined for w in ['LEC', 'LS模型', '风险评价', '隐患PDCA', '履职', '督办', '提级', '闭环验证']):
        return '安全生产业务'
    if any(w in combined for w in ['物联网', 'DCS', 'GDS', '协议网关', '边缘计算', '云边协同', '3万点']):
        return '物联网数据底座'
    if any(w in combined for w in ['五横两纵', '数据资源层', '平台支撑层', 'Data Guard', '容灾', '异地', '主备']):
        return '架构与可靠性'
    if any(w in combined for w in ['性能', '并发', '在线用户', '读写分离', '多级缓存', '响应时间']):
        return '架构与可靠性'
    if any(w in combined for w in ['一期继承', '一期数据', '灰度迁移', '兼容适配', '数据迁移', '全量接管']):
        return '一期继承与升级'
    if any(w in combined for w in ['源代码', '知识产权', '版权', '软件著作权']):
        return '实施与交付'
    if any(w in combined for w in ['驻场', '项目经理', '团队配置', '1+5+N', '上线', '验收']):
        return '实施与交付'
    if any(w in combined for w in ['故障.*响应', 'SLA', '服务.*时效', '7.*24', '质保', '售后']):
        return '服务保障'
    if any(w in combined for w in ['Oracle', '数据库', 'TDE', 'AES-256', '加密', '渗透', '等保']):
        return '数据与安全'
    # 最后才匹配宽泛的"理解与定位"（避免误杀具体内容）
    if any(w in combined for w in ['建设背景', '建设目标', '项目范围', '对招标方', '业务理解', '差异化需求']):
        return '理解与定位'
    if '一期痛点' in tags and not any(w in combined for w in ['重建', '升级', '推倒', '灰度']):
        return '理解与定位'
    return '理解与定位'  # 默认归类为理解与定位（最安全的默认值）


def extract_threads(filepath, top_n=25):
    """从响应文件中提取黄金线索。"""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # 按段落拆分（跳过标题行和过短行）
    paragraphs = [
        p.strip() for p in text.split('\n')
        if len(p.strip()) > 30 and not p.startswith('#')
    ]

    # 评分
    scored = []
    for p in paragraphs:
        s, t = score_paragraph(p)
        if s >= 3:  # 阈值：至少 3 分才算黄金线索
            theme = classify_theme(t, p)
            scored.append({
                'score': s,
                'tags': t,
                'theme': theme,
                'preview': p[:200],
                'full_text': p
            })

    # 按得分降序
    scored.sort(key=lambda x: -x['score'])

    # 主题分布
    theme_dist = {}
    for item in scored:
        theme = item['theme']
        theme_dist[theme] = theme_dist.get(theme, 0) + 1

    return {
        'total_threads': len(scored),
        'theme_distribution': theme_dist,
        'threads': scored[:top_n],
        'all_threads': scored
    }


def format_output(result, top_n):
    """格式化输出为可读文本。"""
    lines = []
    lines.append("=" * 65)
    lines.append("  moi-bid-defense · 黄金线索提取报告")
    lines.append("=" * 65)
    lines.append(f"  提取线索总数: {result['total_threads']} 条")
    lines.append(f"  展示前 {top_n} 条")
    lines.append("")

    lines.append("--- 主题分布 ---")
    for theme, count in sorted(result['theme_distribution'].items(), key=lambda x: -x[1]):
        bar = '█' * max(1, count // 2)
        lines.append(f"  {theme}: {count} 条 {bar}")
    lines.append("")

    lines.append(f"--- 黄金线索 Top {top_n} ---")
    for i, item in enumerate(result['threads'], 1):
        tag_str = ' | '.join(item['tags'])
        lines.append(f"\n#{i:2d} [得分:{item['score']:2d}] [{tag_str}] → {item['theme']}")
        lines.append(f"    {item['preview'][:150]}...")
    lines.append("")

    # 按主题分组推荐幻灯片页数
    lines.append("--- 建议幻灯片分配 ---")
    slide_budget = {
        '封面与收尾': 2,
        '理解与定位': 2,
        '架构与可靠性': 2,
        'AI智能化': 2,
        '安全生产业务': 3,
        '物联网数据底座': 2,
        '数字孪生': 2,
        '一期继承与升级': 1,
        '实施与交付': 2,
        '服务保障': 2,
        '数据与安全': 1,
    }
    total_slides = 0
    for theme, count in result['theme_distribution'].items():
        budget = slide_budget.get(theme, 1)
        total_slides += budget
        bar = '█' * budget
        lines.append(f"  {theme}: ~{budget} 页 {bar} ({count} 条线索)")
    lines.append(f"\n  建议总页数: ~{total_slides} 页 (20 分钟讲标)")
    lines.append("=" * 65)

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='黄金线索提取器')
    parser.add_argument('filepath', help='响应文件路径 (.md)')
    parser.add_argument('--top', type=int, default=25, help='展示前 N 条线索（默认 25）')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    args = parser.parse_args()

    result = extract_threads(args.filepath, args.top)

    if args.json:
        # JSON 输出（供 LLM 消费）
        output = {
            'total_threads': result['total_threads'],
            'theme_distribution': result['theme_distribution'],
            'threads': [
                {
                    'rank': i + 1,
                    'score': t['score'],
                    'tags': t['tags'],
                    'theme': t['theme'],
                    'preview': t['preview']
                }
                for i, t in enumerate(result['threads'])
            ]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(format_output(result, args.top))


if __name__ == '__main__':
    main()
