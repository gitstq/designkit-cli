<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/🎨_DesignKit-CLI-6366f1?style=for-the-badge&logo=python&logoColor=white&labelColor=1e1b4b">
    <img alt="DesignKit-CLI" src="https://img.shields.io/badge/🎨_DesignKit-CLI-6366f1?style=for-the-badge&logo=python&logoColor=white&labelColor=e0e7ff">
  </picture>
</p>

<p align="center">
  <b>轻量级设计令牌生成器 & AI UI 风格引擎</b><br>
  <i>一键生成、预览、导出完整设计系统 —— 零依赖，最大化创意。</i>
</p>

<p align="center">
  <a href="./README.md"><img src="https://img.shields.io/badge/EN-🇬🇧-blue?style=flat-square" alt="English"></a>
  <a href="./README.zh-CN.md"><img src="https://img.shields.io/badge/简体中文-🇨🇳-red?style=flat-square" alt="简体中文"></a>
  <a href="./README.zh-TW.md"><img src="https://img.shields.io/badge/繁體中文-🇭🇰-red?style=flat-square" alt="繁體中文"></a>
</p>

<p align="center">
  <a href="#-核心特性">核心特性</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-详细使用指南">使用指南</a> •
  <a href="#-导出格式">导出格式</a> •
  <a href="#-ai提示词集成">AI 提示词</a> •
  <a href="#-设计思路与迭代规划">设计思路</a>
</p>

<br>

> **💡 DesignKit-CLI 是什么？** 一个零依赖的 Python 命令行工具，让你从简单的主题预设中生成精美的设计系统。从 7 个精心设计的设计主题中选择，自定义每一个参数，在终端中实时预览，然后导出为 CSS/JSON/Tailwind/SCSS/DTCG 格式。更厉害的是——它能为 **GLM-5.1**、GPT 和 Claude 生成优化的 **AI 系统提示词**，让你的 AI 编码工具每次都生成一致且专业的前端界面。

---

## ✨ 核心特性

<table>
<tr>
<td width="300">

### 🎨 **7 套主题预设**
从极简到粗野主义，从温暖到霓虹——每套都拥有完美平衡的色彩、排版和间距。

</td>
<td width="300">

### 🖌️ **色彩智能引擎**
自动生成色阶调色板（50–950 级），互补色/近似色/三分色配色方案，WCAG 对比度检测。

</td>
<td width="300">

### 🔤 **排版生成器**
模块化字体比例系统，5 种字体搭配，自动推荐行高和字重。

</td>
</tr>
<tr>
<td>

### 🖥️ **交互式终端界面**
基于 Rich 的炫酷终端界面，支持实时主题预览和设计探索。

</td>
<td>

### 📦 **多格式导出**
CSS 自定义属性、JSON、Tailwind 配置、SCSS 变量、DTCG（设计令牌标准格式）——一条命令，所有格式一次搞定。

</td>
<td>

### 🤖 **AI 提示词生成器**
生成针对 **GLM-5.1**、GPT-4o 和 Claude 优化的系统提示词——你的 AI 将完美遵循你的设计系统。

</td>
</tr>
</table>

---

## 🚀 快速开始

```bash
# 安装（核心模块零依赖）
pip install designkit-cli

# 或直接克隆运行
git clone https://github.com/gitstq/designkit-cli.git
cd designkit-cli
pip install -e .

# 如需 TUI 预览（可选）：
pip install rich

# 👇 现在就试试这些命令：
designkit list                          # 查看全部 7 套主题
designkit preview --theme minimal       # 预览主题
designkit export --theme minimal --format css   # 导出令牌
designkit palette "#6366f1"             # 生成配色方案
designkit prompt --theme neon --model glm      # 生成 AI 提示词

# 更多示例
designkit preview --theme brutalist     # 预览粗野主义主题
designkit export --theme warm --format json --output ./warm-theme.json
designkit prompt --theme minimal --model glm --component "导航栏" --framework React
```

**环境要求**：Python 3.8+（核心：零依赖；TUI 预览：可选 Rich 库）

---

## 📖 详细使用指南

### `designkit list` — 浏览主题

```bash
designkit list
```

列出所有 7 套内置设计主题及其描述：

| 主题 ID | 名称 | 风格描述 |
|---------|------|----------|
| `minimal` | 极简 Minimal | 干净、留白驱动的设计，适合内容型应用 |
| `brutalist` | 粗野主义 Brutalist | 大胆、高对比、粗犷的设计语言 |
| `warm` | 温暖 Warm | 柔和、亲近、人性化的设计 |
| `neon` | 霓虹 Neon | 充满活力的暗色模式数字美学 |
| `corporate` | 商务 Corporate | 专业、可信、数据密集的设计 |
| `playful` | 活泼 Playful | 有趣、多彩、圆润的设计 |
| `nature` | 自然 Nature | 有机、平静、自然灵感的设计 |

### `designkit preview` — 终端预览

```bash
# 依次预览所有主题
designkit preview

# 预览特定主题
designkit preview --theme neon
```

> **💎 专业提示：** 安装 `rich` 库后可获得炫酷的彩色终端体验，包括实时色板、排版表格、间距柱状图和模拟组件预览。

### `designkit export` — 导出设计令牌

```bash
designkit export --theme minimal --format css        # CSS 自定义属性
designkit export --theme minimal --format json       # 结构化 JSON
designkit export --theme minimal --format tailwind   # Tailwind 配置
designkit export --theme minimal --format scss       # SCSS 变量
designkit export --theme minimal --format dtcg       # W3C 设计令牌标准

# 一次导出所有主题：
designkit export --format css

# 指定输出路径：
designkit export --theme playful --format css --output ./my-theme.css
```

### `designkit palette` — 色彩魔法

```bash
# 从任意十六进制颜色生成完整调色板
designkit palette "#6366f1"

# 简写格式同样支持
designkit palette ff6b6b
```

输出包含：11 级主色调色板、中性灰调色板、互补色、近似色、三分色配色方案，以及前景文本对比度分析。

### `designkit prompt` — AI 提示词生成

```bash
# 生成 GLM-5.1 优化提示词（默认）
designkit prompt --theme minimal --model glm

# 生成 GPT-4o 优化提示词
designkit prompt --theme neon --model openai

# 生成 Claude 优化提示词
designkit prompt --theme warm --model claude

# 生成组件专属提示词
designkit prompt --theme minimal --model glm --component "Card" --framework React
```

生成的提示词包含完整的设计系统上下文（色彩、排版、间距、动效、视觉密度）——确保你的 AI 始终生成符合所选设计语言的代码。

---

## 📦 导出格式

| 格式 | 文件后缀 | 描述 | 适用场景 |
|------|----------|------|----------|
| **CSS** | `.css` | CSS 自定义属性（`--dk-*`） | 任意 Web 项目 |
| **JSON** | `.json` | 结构化嵌套令牌 | 程序化使用 |
| **Tailwind** | `.config.js` | Tailwind CSS `extend` 配置 | Tailwind 项目 |
| **SCSS** | `.scss` | SCSS 变量和映射表 | Sass 项目 |
| **DTCG** | `.tokens.json` | W3C 设计令牌标准格式 | 设计工具互通 |

---

## 🤖 AI 提示词集成

DesignKit-CLI 专为 AI 辅助开发时代而生。它生成的结构化设计令牌可以直接注入到 AI 编码助手的上下文中：

### 支持的 AI 模型

| 模型 | 提示词特色 |
|------|-----------|
| **GLM-5.1** 🏆 | 中文优化，详细设计参数说明，清晰的代码生成要求 |
| **GPT-4o** | 英文优化，精确数值驱动 |
| **Claude** | 简洁指令风格，注重品质和可访问性 |

### 使用场景

1. **统一团队设计语言** — 将导出的 AI 提示词放入项目 `.claude.md` 或 `.cursorrules`
2. **快速原型开发** — 用 `designkit prompt` 生成设计上下文，让 AI 一键生成组件
3. **设计系统迁移** — 在不同项目间快速切换设计风格

---

## 💡 设计思路与迭代规划

### 设计理念

DesignKit-CLI 诞生于一个简单的观察：**AI 生成的界面看起来都一个样**。无论是 GPT-4o、GLM-5.1 还是 Claude——没有明确的设计指引，AI 输出的都是千篇一律的通用界面。

受 [taste-skill](https://github.com/Leonxlnx/taste-skill)（GitHub 37K+ Stars）的启发，DesignKit-CLI 采取了更全面的方法：

1. **🎯 令牌胜于指令** — 不是单纯告诉 AI"让它好看"，而是提供精确的数值设计令牌
2. **🔄 实时预览** — 在投入代码之前，先在终端中看到设计系统变成现实
3. **🌐 多格式输出** — 导出到你项目实际使用的格式（CSS、Tailwind、SCSS 等）
4. **🤖 AI 原生** — 专为 AI 辅助开发时代设计，为每个主流模型提供提示词模板
5. **🔧 零依赖** — 核心功能仅依赖 Python 标准库

### 迭代规划

- [ ] **自定义主题构建器** — 交互式 CLI 向导，从零创建主题
- [ ] **组件库集成** — 预建设计系统组件 CSS（按钮、卡片、表单、导航）
- [ ] **Figma 插件支持** — 从 Figma 导入/导出令牌
- [ ] **Web UI** — 简单的 Web 端主题设计器
- [ ] **暗色模式切换** — 自动生成浅色和深色两套令牌
- [ ] **更多 AI 模型** — DeepSeek、Qwen、Gemini 提示词模板
- [ ] **国际化** — RTL 语言支持令牌

---

## 🤝 贡献指南

欢迎参与贡献！以下是参与方式：

1. 🍴 **Fork** 本仓库
2. 🌿 **创建** 功能分支（`git checkout -b feature/amazing`）
3. 💻 **提交** 变更（`git commit -m 'feat: 添加超棒功能'`）
4. 📤 **推送** 到分支（`git push origin feature/amazing`）
5. 🔄 **发起** Pull Request

提交信息请遵循 [Angular 提交规范](https://www.conventionalcommits.org/)。

**反馈问题**：发现了 Bug？有好主意？[提交 Issue](https://github.com/gitstq/designkit-cli/issues)

---

## 📄 开源协议

本项目采用 **MIT 许可证**——详见 [LICENSE](./LICENSE) 文件。

---

<p align="center">
  <sub>用 ❤️ 构建 · DesignKit Team · 灵感来源于 <a href="https://github.com/Leonxlnx/taste-skill">taste-skill</a></sub>
</p>
<p align="center">
  <sub><a href="./README.md">🇬🇧 English</a> · 🇨🇳 简体中文 · <a href="./README.zh-TW.md">🇭🇰 繁體中文</a></sub>
</p>