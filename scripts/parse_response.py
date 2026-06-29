#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
响应文件解析器 — moi-bid-defense Step 1

解析投标技术响应文件（.md 或 .docx），提取结构化信息供黄金线索提取使用。

用法：
    python3 parse_response.py <响应文件.[md|docx]> [--json]

输出：
    章节结构树、★ 条款引用清单、量化指标分类统计、架构关键词分布
"""

import re
import sys
import json
import argparse
from pathlib import Path


def parse_markdown(filepath):
    """解析 Markdown 格式的响应文件。"""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    lines = text.split('\n')

    # 提取标题层级
    headings = []
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            level = len(re.match(r'^#+', line).group())
            title = line.lstrip('#').strip()
            headings.append({'level': level, 'title': title})

    # 提取 ★ 引用
    star_refs = re.findall(r'★[^。\n]{10,120}', text)

    # 量化指标分类
    pct_metrics = re.findall(r'\d+[%％]|[≥≤≥]\d+\s*%', text)
    time_metrics = re.findall(r'\d+\s*(?:秒|分钟|小时|天|月|年|ms)', text)
    scale_metrics = re.findall(r'\d+\s*(?:万|亿|路|套|种|类|个|层|级|张|次|点)', text)
    rate_metrics = re.findall(r'\d+\s*(?:Mbps|Gbps|FPS|QPS|GB|TB|MB|PB)', text)

    # 架构关键词
    arch_keywords = re.findall(
        r'(?:五横两纵|分层架构|模块化|可扩展|冗余部署|高可用|异地容灾|负载均衡|读写分离|多级缓存|'
        r'微服务|容器化|Kubernetes|云边协同|灰度发布|滚动更新)',
        text
    )

    # 总字数
    chinese_chars = len(re.findall(r'[一-鿿]', text))

    return {
        'file': filepath,
        'total_chars': len(text),
        'chinese_chars': chinese_chars,
        'headings': headings,
        'heading_count': len(headings),
        'star_refs': star_refs,
        'star_count': len(star_refs),
        'metrics': {
            'percentage': {'count': len(pct_metrics), 'samples': pct_metrics[:10]},
            'time': {'count': len(time_metrics), 'samples': time_metrics[:10]},
            'scale': {'count': len(scale_metrics), 'samples': scale_metrics[:10]},
            'rate': {'count': len(rate_metrics), 'samples': rate_metrics[:10]},
            'total': len(pct_metrics) + len(time_metrics) + len(scale_metrics) + len(rate_metrics)
        },
        'arch_keywords_count': len(arch_keywords),
        'line_count': len(lines)
    }


def parse_docx(filepath):
    """解析 docx 格式的响应文件。"""
    try:
        import docx
    except ImportError:
        print("错误：需要安装 python-docx 库。运行: pip install python-docx", file=sys.stderr)
        sys.exit(1)

    doc = docx.Document(filepath)
    paragraphs = [p.text for p in doc.paragraphs]
    text = '\n'.join(paragraphs)

    # 保存为临时 md 文件供后续处理
    md_path = Path(filepath).with_suffix('.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(text)

    result = parse_markdown(str(md_path))
    result['file'] = filepath
    result['converted_md'] = str(md_path)
    return result


def format_output(result):
    """格式化输出为可读文本。"""
    lines = []
    lines.append("=" * 60)
    lines.append(f"  文件：{result['file']}")
    lines.append(f"  总字符数：{result['total_chars']:,}")
    lines.append(f"  中文字数：{result['chinese_chars']:,}")
    lines.append(f"  章节数：{result['heading_count']} 个标题")
    lines.append(f"  ★ 引用：{result['star_count']} 处")
    lines.append("=" * 60)

    # 量化指标分类
    m = result['metrics']
    lines.append(f"\n📊 量化指标（共 {m['total']} 个）：")
    lines.append(f"  精度/百分比：{m['percentage']['count']} 个")
    lines.append(f"  时间指标：{m['time']['count']} 个")
    lines.append(f"  规模数量：{m['scale']['count']} 个")
    lines.append(f"  速率/容量：{m['rate']['count']} 个")

    # 架构关键词
    lines.append(f"\n🏗 架构关键词：{result['arch_keywords_count']} 处")

    # 章节结构（只显示 H2）
    lines.append("\n📑 一级章节：")
    for h in result['headings']:
        if h['level'] == 2:
            lines.append(f"  {h['title'][:60]}")

    # ★ 引用抽样
    lines.append(f"\n⭐ ★ 引用抽样（共 {result['star_count']} 处，展示前 5）：")
    for ref in result['star_refs'][:5]:
        lines.append(f"  • {ref[:100]}...")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='响应文件解析器')
    parser.add_argument('filepath', help='响应文件路径 (.md 或 .docx)')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    args = parser.parse_args()

    filepath = args.filepath
    ext = Path(filepath).suffix.lower()

    if ext == '.md':
        result = parse_markdown(filepath)
    elif ext == '.docx':
        result = parse_docx(filepath)
    else:
        print(f"错误：不支持的文件格式 '{ext}'。请使用 .md 或 .docx 文件。", file=sys.stderr)
        sys.exit(1)

    if args.json:
        # JSON 输出不包含完整标题列表（太大）
        output = {
            'file': result['file'],
            'total_chars': result['total_chars'],
            'chinese_chars': result['chinese_chars'],
            'heading_count': result['heading_count'],
            'star_count': result['star_count'],
            'metrics': {k: v['count'] for k, v in result['metrics'].items() if k != 'total'},
            'metrics_total': result['metrics']['total'],
            'arch_keywords_count': result['arch_keywords_count']
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(format_output(result))


if __name__ == '__main__':
    main()
