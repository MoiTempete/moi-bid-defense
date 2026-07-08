# 环境搭建指南 · 从零开始（Mac版）

本文档面向**零基础用户**，手把手完成 Claude Code + VS Code + Skills 的完整搭建。

预计耗时：30-45 分钟。

---

## 一、硬件与系统要求

- macOS 12+ / Windows 10+ / Ubuntu 20+
- 至少 8GB 内存
- 已安装 Google Chrome 浏览器

---

## 二、安装基础工具

### 2.1 安装 Homebrew（macOS）

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

安装完成后运行 `brew --version` 确认。

### 2.2 安装 Python 3

```bash
# macOS
brew install python@3.11

# 验证
python3 --version  # 应输出 3.11.x 或更高
```

### 2.3 安装 Node.js（Claude Code 依赖）

```bash
# macOS
brew install node@20

# 验证
node --version  # 应输出 v20.x 或更高
npm --version
```

### 2.4 安装 Git

```bash
# macOS（通常已预装）
brew install git

# 验证
git --version
```

---

## 三、安装 VS Code + Claude Code 插件

### 3.1 安装 VS Code

从 [https://code.visualstudio.com/](https://code.visualstudio.com/) 下载安装。

### 3.2 安装 Claude Code 官方插件

1. 打开 VS Code
2. 点击左侧扩展图标（或按 `Cmd+Shift+X`）
3. 搜索 `Claude Code`
4. 找到由 Anthropic 发布的官方插件，点击安装
5. 安装完成后重启 VS Code

---

## 四、安装 Claude Code CLI

### 4.1 全局安装

```bash
npm install -g @anthropic-ai/claude-code
```

### 4.2 验证安装

```bash
claude --version
```

---

## 五、配置自定义 LLM API（绕过登录，使用 DeepSeek）

Claude Code 支持通过配置文件使用第三方 LLM API，无需 Anthropic 账号。

### 5.1 获取 DeepSeek API Key

1. 访问 [https://platform.deepseek.com/](https://platform.deepseek.com/)
2. 注册账号并完成实名认证
3. 在「API Keys」页面创建新的 API Key
4. 复制并保存 API Key（格式为 `sk-xxxx`）

### 5.2 创建 Claude Code 配置文件

```bash
mkdir -p ~/.claude
```

创建 `~/.claude/settings.json`：

```json
{
  "model": "deepseek-v3",
  "apiKey": "sk-你的DeepSeek API Key",
  "apiBaseUrl": "https://api.deepseek.com/v1",
  "provider": "openai-compatible"
}
```

> **说明**：
>
> - `model` 可选 `deepseek-v3`（速度快）或 `deepseek-r1`（推理强，适合复杂任务）
> - `apiBaseUrl` 使用 DeepSeek 的 OpenAI 兼容端点
> - 不需要 Anthropic 账号，不需要登录

### 5.3 验证连接

```bash
echo "你好，请回复'环境正常'" | claude -p -
```

如果返回包含"环境正常"的回复，说明配置成功。

---

## 六、安装 Skills

Skills 是 Claude Code 的扩展能力包，存放在 `~/.claude/skills/` 目录下。

### 6.1 安装 guizang-ppt（PPT 生成引擎）

```bash
git clone https://github.com/op7418/guizang-ppt-skill ~/.claude/skills/guizang-ppt
```

### 6.2 安装 moi-bid-response（投标响应文件编写）

```bash
git clone https://github.com/MoiTempete/moi-bid-response ~/.claude/skills/moi-bid-response
```

### 6.3 安装 moi-bid-defense（讲标答辩幻灯片）

```bash
git clone https://github.com/MoiTempete/moi-bid-defense ~/.claude/skills/moi-bid-defense
```

### 6.4 安装 moi-hardware-inquiry（硬件询价，可选）

```bash
git clone https://github.com/MoiTempete/moi-hardware-inquiry ~/.claude/skills/moi-hardware-inquiry
```

### 6.5 验证 Skills 已安装

```bash
ls ~/.claude/skills/
# 应显示: guizang-ppt  moi-bid-response  moi-bid-defense  moi-hardware-inquiry
```

---

## 七、安装 Python 依赖

这些 Python 包是 Skills 运行所需的依赖。

```bash
# 文档解析
pip3 install python-docx openpyxl

# PPT 生成
pip3 install python-pptx

# 自动截图（仅 screenshot_slides.py 需要）
pip3 install playwright

# 验证
python3 -c "import docx, openpyxl, pptx; print('核心依赖 OK')"
python3 -c "from playwright.sync_api import sync_playwright; print('Playwright OK')"
```

---

## 八、首次使用

### 8.1 打开项目

```bash
# 假设你的投标文件在桌面的这个目录
cd ~/Desktop/广汇能源安全生产信息化（二期）
```

### 8.2 在 VS Code 中打开

1. 启动 VS Code
2. `File → Open Folder` → 选择你的项目目录
3. 按 `Cmd+Shift+P` → 输入 `Claude Code: Open`

### 8.3 调用 Skill

在 Claude Code 对话框中输入：

```
/moi-bid-defense

响应文件在：./投标文件/技术响应方案-完整稿.md
讲标时长 20 分钟，默认配置即可
```

Claude Code 会自动加载 skill 并按工作流逐步生成幻灯片。

---

## 九、常见问题

### Q: `claude` 命令找不到？

```bash
# 确认 npm 全局安装路径在 PATH 中
echo $PATH | grep npm
# 如果没有，添加到 ~/.zshrc:
echo 'export PATH="$PATH:$(npm config get prefix)/bin"' >> ~/.zshrc
source ~/.zshrc
```

### Q: DeepSeek API 返回 401？

检查 `~/.claude/settings.json` 中的 `apiKey` 是否正确。注意 API Key 格式为 `sk-` 开头。

### Q: DeepSeek API 返回额度不足？

登录 [platform.deepseek.com](https://platform.deepseek.com) 充值。DeepSeek API 按 token 计费，非常便宜（约 ¥1/百万 token）。

### Q: `pip3 install playwright` 安装很慢？

Playwright 需要下载 Chromium 浏览器（~150MB）。如果下载慢，可以使用国内镜像：

```bash
pip3 install playwright -i https://pypi.tuna.tsinghua.edu.cn/simple
PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright python3 -m playwright install chromium
```

### Q: 截图脚本报错 "Browser closed unexpectedly"？

系统需要已安装 Google Chrome 浏览器。如果用的是 Chromium，修改脚本中的 `channel="chrome"` 为 `channel="chromium"`。

### Q: VS Code 插件无法连接 Claude Code CLI？

1. 确认 `claude --version` 能正常输出
2. 在 VS Code 设置中搜索 `claude-code.path`，手动指定 CLI 路径：
   ```bash
   which claude  # 复制输出路径
   ```
3. 将路径粘贴到 VS Code 设置中

---

## 十、环境检查清单

完成搭建后，逐项确认：

- [ ] `python3 --version` ≥ 3.11
- [ ] `node --version` ≥ v20
- [ ] `git --version` 正常
- [ ] `claude --version` 正常
- [ ] `ls ~/.claude/skills/` 显示 3 个 skill 目录
- [ ] `python3 -c "import docx, openpyxl, pptx; print('OK')"` 正常
- [ ] VS Code 插件已安装
- [ ] DeepSeek API Key 已配置在 `~/.claude/settings.json`
- [ ] 测试对话 `echo "hello" | claude -p -` 能正常回复

全部通过 = 环境搭建完成 🎉
