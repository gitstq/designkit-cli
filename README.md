<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/🎨_DesignKit-CLI-6366f1?style=for-the-badge&logo=python&logoColor=white&labelColor=1e1b4b">
    <img alt="DesignKit-CLI" src="https://img.shields.io/badge/🎨_DesignKit-CLI-6366f1?style=for-the-badge&logo=python&logoColor=white&labelColor=e0e7ff">
  </picture>
</p>

<p align="center">
  <b>Lightweight Design Token Generator & AI UI Style Engine</b><br>
  <i>Generate, preview, and export complete design systems — zero dependencies, maximum creativity.</i>
</p>

<p align="center">
  <a href="./README.md"><img src="https://img.shields.io/badge/EN-🇬🇧-blue?style=flat-square" alt="English"></a>
  <a href="./README.zh-CN.md"><img src="https://img.shields.io/badge/简体中文-🇨🇳-red?style=flat-square" alt="简体中文"></a>
  <a href="./README.zh-TW.md"><img src="https://img.shields.io/badge/繁體中文-🇭🇰-red?style=flat-square" alt="繁體中文"></a>
</p>

<p align="center">
  <a href="#-key-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-usage-guide">Usage</a> •
  <a href="#-export-formats">Export</a> •
  <a href="#-ai-prompt-integration">AI Prompts</a> •
  <a href="#-design-philosophy">Philosophy</a>
</p>

<br>

> **💡 What is DesignKit-CLI?** A zero-dependency Python CLI tool that lets you generate beautiful design systems from simple theme presets. Choose from 7 carefully crafted design themes, customize every parameter, preview in your terminal, and export to CSS/JSON/Tailwind/SCSS/DTCG format. Plus — it generates optimized **AI system prompts** for GLM-5.1, GPT, and Claude, so your AI coding tools produce consistent, professional UI code every time.

---

## ✨ Key Features

<table>
<tr>
<td width="300">

### 🎨 **7 Theme Presets**
From Minimal to Brutalist, Warm to Neon — each with perfectly balanced colors, typography, and spacing.

</td>
<td width="300">

### 🖌️ **Color Intelligence**
Automatic palette generation (50–950 scale), complementary/analogous/triadic schemes, WCAG contrast checking.

</td>
<td width="300">

### 🔤 **Typography Engine**
Modular type scales with 5 font pairings, line-height optimization, and weight recommendations.

</td>
</tr>
<tr>
<td>

### 🖥️ **Interactive TUI**
Beautiful Rich-powered terminal interface for live theme preview and design exploration.

</td>
<td>

### 📦 **Multi-Format Export**
CSS Custom Properties, JSON, Tailwind Config, SCSS Variables, DTCG (Design Tokens Format) — one command, all formats.

</td>
<td>

### 🤖 **AI Prompt Generator**
Generate system prompts optimized for **GLM-5.1**, GPT-4o, and Claude — your AI will follow your design system perfectly.

</td>
</tr>
</table>

---

## 🚀 Quick Start

```bash
# Install (no dependencies needed for core)
pip install designkit-cli

# Or run directly without install
git clone https://github.com/gitstq/designkit-cli.git
cd designkit-cli
pip install -e .

# For TUI preview (optional):
pip install rich

# 👇 Try these commands right now:
designkit list                          # See all 7 themes
designkit preview --theme minimal       # Preview a theme
designkit export --theme minimal --format css   # Export tokens
designkit palette "#6366f1"             # Generate color palette
designkit prompt --theme neon --model glm      # Generate AI prompt
```

**Requirements**: Python 3.8+ (core: zero dependencies; TUI: Rich library optional)

---

## 📖 Usage Guide

### `designkit list` — Browse themes

```bash
designkit list
```

Lists all 7 built-in design themes with descriptions:
- `minimal` — Clean, whitespace-driven
- `brutalist` — Bold, high-contrast
- `warm` — Soft, earthy, approachable
- `neon` — Vibrant, dark-mode-first
- `corporate` — Professional, data-dense
- `playful` — Fun, colorful, rounded
- `nature` — Organic, calm, green

### `designkit preview` — Preview in terminal

```bash
# Preview all themes sequentially
designkit preview

# Preview a specific theme
designkit preview --theme neon
```

> **💎 Pro Tip:** Install `rich` for a beautiful, color-rich TUI experience with live color swatches, typography tables, spacing bars, and simulated component previews.

### `designkit export` — Export design tokens

```bash
designkit export --theme minimal --format css        # CSS custom properties
designkit export --theme minimal --format json       # Structured JSON
designkit export --theme minimal --format tailwind   # Tailwind config
designkit export --theme minimal --format scss       # SCSS variables
designkit export --theme minimal --format dtcg       # W3C Design Tokens

# Export all themes at once:
designkit export --format css

# Specify output path:
designkit export --theme playful --format css --output ./my-theme.css
```

### `designkit palette` — Color wizardry

```bash
# Generate full palette from any hex color
designkit palette "#6366f1"

# Short form also works
designkit palette ff6b6b
```

Output includes: 11-step primary palette, neutral gray palette, complementary color, analogous colors, triadic scheme, and foreground text contrast analysis.

### `designkit prompt` — AI system prompt generation

```bash
# Generate GLM-5.1 optimized prompt (default)
designkit prompt --theme minimal --model glm

# Generate for GPT-4o
designkit prompt --theme neon --model openai

# Generate for Claude
designkit prompt --theme warm --model claude

# Generate a component-specific prompt
designkit prompt --theme minimal --model glm --component "Card" --framework React
```

The generated prompts include complete design system context (colors, typography, spacing, motion, visual density) — ensuring your AI always produces code that matches your chosen design language.

---

## 📦 Export Formats

| Format | File Ext | Description | Use Case |
|--------|----------|-------------|----------|
| **CSS** | `.css` | CSS Custom Properties (`--dk-*`) | Any web project |
| **JSON** | `.json` | Structured nested tokens | Programmatic use |
| **Tailwind** | `.config.js` | Tailwind CSS `extend` config | Tailwind projects |
| **SCSS** | `.scss` | SCSS variables & maps | Sass projects |
| **DTCG** | `.tokens.json` | W3C Design Tokens Format | Design tool interop |

---

## 💡 Design Philosophy & Roadmap

### Design Principles

DesignKit-CLI was born from a simple observation: **AI-generated interfaces all look the same**. Whether it's GPT-4o, GLM-5.1, or Claude — without explicit design guidance, AI outputs generic, cookie-cutter UIs.

Inspired by the vision behind [taste-skill](https://github.com/Leonxlnx/taste-skill) (37K+ stars on GitHub), DesignKit-CLI takes a more comprehensive approach:

1. **🎯 Tokens over Instructions** — Instead of just telling AI "make it look good," we provide precise numerical design tokens
2. **🔄 Live Preview** — See your design system come to life in the terminal before committing to code
3. **🌐 Multi-Format** — Export to the format your project actually uses (CSS, Tailwind, SCSS, etc.)
4. **🤖 AI-Native** — Purpose-built for the AI-assisted development era, with prompt templates for every major model
5. **🔧 Zero Dependencies** — Core functionality works with just Python standard library

### Roadmap

- [ ] **Custom Theme Builder** — Interactive CLI wizard for creating themes from scratch
- [ ] **Component Library** — Pre-built design system component CSS (buttons, cards, forms, nav)
- [ ] **Figma Plugin Support** — Import/export tokens from Figma
- [ ] **Web UI** — Simple web-based theme designer
- [ ] **Dark Mode Toggle** — Auto-generate both light and dark token sets
- [ ] **More AI Models** — DeepSeek, Qwen, Gemini prompt templates
- [ ] **i18n** — RTL language support tokens

---

## 🤝 Contributing

We welcome contributions! Here's how to get involved:

1. 🍴 **Fork** the repository
2. 🌿 **Create** a feature branch (`git checkout -b feature/amazing`)
3. 💻 **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
4. 📤 **Push** to the branch (`git push origin feature/amazing`)
5. 🔄 **Open** a Pull Request

Please follow [Angular Commit Convention](https://www.conventionalcommits.org/) for commit messages.

**Issues**: Found a bug? Have an idea? [Open an issue](https://github.com/gitstq/designkit-cli/issues)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.

---

<p align="center">
  <sub>Built with ❤️ by the DesignKit Team · Inspired by <a href="https://github.com/Leonxlnx/taste-skill">taste-skill</a></sub>
</p>
<p align="center">
  <sub>🇬🇧 English · <a href="./README.zh-CN.md">🇨🇳 简体中文</a> · <a href="./README.zh-TW.md">🇭🇰 繁體中文</a></sub>
</p>