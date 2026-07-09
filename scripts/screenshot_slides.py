#!/usr/bin/env python3
"""Automated screenshot capture for HTML slide decks using Playwright + system Chrome.

Usage:
    python3 screenshot_slides.py <index.html路径> [输出目录] [页数]

    页数参数可选，省略时自动从 HTML 中检测 <section class="slide"> 数量。

Output:
    在输出目录下生成 P01.png ~ PNN.png，每页一张 1920x1080 截图。
"""

import os, sys, time
from playwright.sync_api import sync_playwright


def _detect_page_count(html_path: str) -> int:
    """从 HTML 文件中自动检测幻灯片页数。"""
    with open(html_path) as f:
        content = f.read()
    count = content.count('class="slide')
    if count == 0:
        raise ValueError(f"未在 {html_path} 中检测到任何 slide 页面，请检查文件内容")
    return count


def capture_slides(html_path: str, out_dir: str, page_count: int = 0) -> list[str]:
    """Capture screenshots of all slides in an HTML deck.

    Args:
        html_path: Absolute path to the index.html file
        out_dir: Directory to save PNG screenshots
        page_count: Number of slides (0 = auto-detect from HTML)

    Returns:
        List of saved file paths
    """
    os.makedirs(out_dir, exist_ok=True)
    file_url = "file://" + os.path.abspath(html_path)

    if page_count <= 0:
        page_count = _detect_page_count(html_path)
        print(f"自动检测到 {page_count} 页幻灯片")

    screenshots = []

    with sync_playwright() as p:
        # Use system Chrome (no extra download needed)
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(5000)  # Wait for WebGL + animations
        page.evaluate("document.body.style.zoom = '100%'")
        page.wait_for_timeout(500)   # Let layout reflow after zoom

        for i in range(page_count):
            if i > 0:
                page.keyboard.press("ArrowRight")
                page.wait_for_timeout(2500)  # Wait for slide transition

            path = os.path.join(out_dir, f"P{i + 1:02d}.png")
            page.screenshot(path=path, full_page=False)
            screenshots.append(path)
            print(f"  P{i + 1:02d}/{page_count:02d} saved")

        browser.close()

    print(f"Done: {len(screenshots)} screenshots → {out_dir}")
    return screenshots


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 screenshot_slides.py <index.html> [out_dir] [page_count]")
        print("  page_count 可选，省略时自动从 HTML 检测")
        sys.exit(1)

    html = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(html), "screenshots")
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    capture_slides(html, out, count)
