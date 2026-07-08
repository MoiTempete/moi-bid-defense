# 环境搭建指南 · 从零开始（Windows 版）

本文档面向**零基础 Windows 用户**，手把手完成 Claude Code + VS Code + Skills 的完整搭建。

预计耗时：30-45 分钟。

---

## 一、硬件与系统要求

- Windows 10 22H2 或更高 / Windows 11
- 至少 8GB 内存
- 已安装 Google Chrome 浏览器
- 建议使用 PowerShell 7+ 或 Windows Terminal（非必须，但体验更好）

---

## 二、安装基础工具

### 2.1 安装 Python 3

1. 打开 [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. 点击黄色按钮下载最新 Python 3.11+ 安装包
3. **重要**：安装时勾选底部的 **"Add Python to PATH"**（必须勾选！）
4. 点击 Install Now 完成安装
5. 验证：

```powershell
python --version
# 应输出 Python 3.11.x 或更高
```

### 2.2 安装 Node.js

1. 打开 [https://nodejs.org/](https://nodejs.org/)
2. 下载 LTS 版本（左侧绿色按钮，v20.x 或 v22.x）
3. 运行安装包，一路 Next（安装程序会自动添加 PATH）
4. 验证：

```powershell
node --version
# 应输出 v20.x 或更高
npm --version
```

### 2.3 安装 Git

1. 打开 [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. 下载 64-bit 安装包
3. 运行安装，一路 Next（默认选项即可）
4. 验证：

```powershell
git --version
```

---

## 三、安装 VS Code + Claude Code 插件

### 3.1 安装 VS Code

1. 打开 [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. 下载 Windows 版安装包
3. 运行安装，建议勾选「添加到右键菜单」和「添加到 PATH」
4. 完成安装后启动 VS Code

### 3.2 安装 Claude Code 官方插件

1. 点击左侧扩展图标（或按 `Ctrl+Shift+X`）
2. 搜索 `Claude Code`
3. 找到由 Anthropic 发布的官方插件，点击安装
4. 安装完成后重启 VS Code

---

## 四、安装 Claude Code CLI

### 4.1 全局安装

打开 PowerShell（以管理员身份运行）：

```powershell
npm install -g @anthropic-ai/claude-code
```

> 如果遇到执行策略限制，先运行：
> ```powershell
> Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 4.2 验证安装

```powershell
claude --version
```

---

## 五、配置自定义 LLM API（绕过登录，使用 DeepSeek）

### 5.1 获取 DeepSeek API Key

1. 访问 [https://platform.deepseek.com/](https://platform.deepseek.com/)
2. 注册账号并完成实名认证
3. 在「API Keys」页面创建新的 API Key
4. 复制并保存 API Key（格式为 `sk-xxxx`）

### 5.2 创建配置文件

在 PowerShell 中：

```powershell
# 创建配置目录
mkdir $env:USERPROFILE\.claude -Force
```

用记事本创建 `C:\Users\你的用户名\.claude\settings.json`：

```json
{
  "model": "deepseek-v3",
  "apiKey": "sk-你的DeepSeek API Key",
  "apiBaseUrl": "https://api.deepseek.com/v1",
  "provider": "openai-compatible"
}
```

> **说明**：
> - `model` 可选 `deepseek-v3`（速度快，推荐日常使用）或 `deepseek-r1`（推理强，适合复杂任务）
> - 不需要 Anthropic 账号，不需要登录

### 5.3 验证连接

```powershell
echo "你好，请回复'环境正常'" | claude -p -
```

如果返回包含"环境正常"的回复，说明配置成功。

---

## 六、安装 Skills

### 6.1 安装 guizang-ppt（PPT 生成引擎）

```powershell
git clone https://github.com/op7418/guizang-ppt-skill $env:USERPROFILE\.claude\skills\guizang-ppt
```

### 6.2 安装 moi-bid-defense（讲标答辩）

```powershell
git clone https://github.com/MoiTempete/moi-bid-defense $env:USERPROFILE\.claude\skills\moi-bid-defense
```

### 6.3 安装 moi-hardware-inquiry（硬件询价，可选）

```powershell
git clone https://github.com/MoiTempete/moi-hardware-inquiry $env:USERPROFILE\.claude\skills\moi-hardware-inquiry
```

### 6.4 验证

```powershell
dir $env:USERPROFILE\.claude\skills\
# 应显示: guizang-ppt  moi-bid-defense  moi-hardware-inquiry
```

---

## 七、安装 Python 依赖

```powershell
# 文档解析
pip install python-docx openpyxl

# PPT 生成
pip install python-pptx

# 自动截图
pip install playwright

# 验证
python -c "import docx, openpyxl, pptx; print('核心依赖 OK')"
python -c "from playwright.sync_api import sync_playwright; print('Playwright OK')"
```

> Playwright 会自动下载 Chromium 浏览器（~150MB）。如果下载失败，见第九章 FAQ。

---

## 八、首次使用

### 8.1 准备项目文件夹

把你的投标文件放到一个文件夹，例如 `C:\Users\你的用户名\Desktop\广汇能源项目\`。

### 8.2 在 VS Code 中打开

1. 启动 VS Code
2. `File → Open Folder` → 选择你的项目文件夹
3. 按 `Ctrl+Shift+P` → 输入 `Claude Code: Open`

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

`npm install -g` 安装的全局命令在 Windows 上可能不在 PATH 中。手动添加到系统环境变量：

1. 在 PowerShell 中运行 `npm config get prefix`，记住输出路径
2. 打开「系统属性 → 高级 → 环境变量」
3. 在「Path」中添加上述路径（通常是 `C:\Users\你的用户名\AppData\Roaming\npm`）
4. 重启 PowerShell

### Q: PowerShell 执行策略报错？

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

输入 `Y` 确认。

### Q: DeepSeek API 返回 401？

检查 `C:\Users\你的用户名\.claude\settings.json` 中的 `apiKey` 是否正确，API Key 以 `sk-` 开头。

### Q: DeepSeek API 额度不足？

登录 [platform.deepseek.com](https://platform.deepseek.com) 充值。DeepSeek 按 token 计费，非常便宜（约 ¥1/百万 token）。

### Q: `pip install playwright` 下载 Chromium 失败？

Playwright 需要下载 ~150MB 的 Chromium 浏览器。如果网络不稳定导致下载失败，设置国内镜像：

```powershell
$env:PLAYWRIGHT_DOWNLOAD_HOST="https://npmmirror.com/mirrors/playwright"
python -m playwright install chromium
```

### Q: 截图脚本报错 "Browser closed unexpectedly"？

系统需要已安装 Google Chrome 浏览器（不是 Chromium Edge）。如果只有 Edge：

1. 打开 `~/.claude/skills/moi-bid-defense/scripts/screenshot_slides.py`
2. 找到 `channel="chrome"` 
3. 改为 `channel="msedge"`

### Q: `git clone` 速度太慢？

GitHub 在国内访问较慢，可以设置代理或使用镜像：

```powershell
# 方法一：使用代理（如果你有）
git config --global http.proxy http://127.0.0.1:7890

# 方法二：使用 ghproxy 加速
git clone https://ghproxy.com/https://github.com/op7418/guizang-ppt-skill $env:USERPROFILE\.claude\skills\guizang-ppt
```

### Q: VS Code 插件无法连接 Claude Code CLI？

1. 确认 `claude --version` 能正常输出
2. 在 VS Code 中按 `Ctrl+,` 打开设置
3. 搜索 `claude-code.path`
4. 填入 claude CLI 的完整路径：

   ```powershell
   # 先获取路径
   where.exe claude
   # 复制输出，粘贴到 VS Code 设置中
   ```

---

## 十、环境检查清单

完成搭建后，逐项确认：

- [ ] `python --version` ≥ 3.11
- [ ] `node --version` ≥ v20
- [ ] `git --version` 正常
- [ ] `claude --version` 正常
- [ ] `dir %USERPROFILE%\.claude\skills\` 显示 3 个 skill 目录
- [ ] `python -c "import docx, openpyxl, pptx; print('OK')"` 正常
- [ ] VS Code 插件已安装
- [ ] DeepSeek API Key 已配置在 `%USERPROFILE%\.claude\settings.json`
- [ ] 测试对话 `echo "hello" | claude -p -` 能正常回复

全部通过 = 环境搭建完成 🎉
