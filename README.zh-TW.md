<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/🎨_DesignKit-CLI-6366f1?style=for-the-badge&logo=python&logoColor=white&labelColor=1e1b4b">
    <img alt="DesignKit-CLI" src="https://img.shields.io/badge/🎨_DesignKit-CLI-6366f1?style=for-the-badge&logo=python&logoColor=white&labelColor=e0e7ff">
  </picture>
</p>

<p align="center">
  <b>輕量級設計令牌生成器 & AI UI 風格引擎</b><br>
  <i>一鍵生成、預覽、匯出完整設計系統 —— 零依賴，最大化創意。</i>
</p>

<p align="center">
  <a href="./README.md"><img src="https://img.shields.io/badge/EN-🇬🇧-blue?style=flat-square" alt="English"></a>
  <a href="./README.zh-CN.md"><img src="https://img.shields.io/badge/简体中文-🇨🇳-red?style=flat-square" alt="简体中文"></a>
  <a href="./README.zh-TW.md"><img src="https://img.shields.io/badge/繁體中文-🇭🇰-red?style=flat-square" alt="繁體中文"></a>
</p>

<p align="center">
  <a href="#-核心功能">核心功能</a> •
  <a href="#-快速開始">快速開始</a> •
  <a href="#-詳細使用指南">使用指南</a> •
  <a href="#-匯出格式">匯出格式</a> •
  <a href="#-ai提示詞整合">AI 提示詞</a> •
  <a href="#-設計理念與發展藍圖">設計理念</a>
</p>

<br>

> **💡 DesignKit-CLI 是什麼？** 一個零依賴的 Python 命令列工具，讓你能從簡單的主題預設中生成精美的設計系統。從 7 個精心設計的設計主題中選擇，自訂每一個參數，在終端機中即時預覽，然後匯出為 CSS/JSON/Tailwind/SCSS/DTCG 格式。更厲害的是——它能為 **GLM-5.1**、GPT 和 Claude 生成優化的 **AI 系統提示詞**，讓你的 AI 編碼工具每次都生成一致且專業的前端介面。

---

## ✨ 核心功能

<table>
<tr>
<td width="300">

### 🎨 **7 套主題預設**
從極簡到粗野主義，從溫暖到霓虹——每套都擁有完美平衡的色彩、排版和間距。

</td>
<td width="300">

### 🖌️ **色彩智慧引擎**
自動生成色階調色板（50–950 級），互補色/近似色/三分色配色方案，WCAG 對比度檢測。

</td>
<td width="300">

### 🔤 **排版產生器**
模組化字體比例系統，5 種字體搭配，自動推薦行高和字重。

</td>
</tr>
<tr>
<td>

### 🖥️ **互動式終端介面**
基於 Rich 的炫酷終端介面，支援即時主題預覽和設計探索。

</td>
<td>

### 📦 **多格式匯出**
CSS 自訂屬性、JSON、Tailwind 配置、SCSS 變數、DTCG（設計令牌標準格式）——一條命令，所有格式一次搞定。

</td>
<td>

### 🤖 **AI 提示詞產生器**
生成針對 **GLM-5.1**、GPT-4o 和 Claude 優化的系統提示詞——你的 AI 將完美遵循你的設計系統。

</td>
</tr>
</table>

---

## 🚀 快速開始

```bash
# 安裝（核心模組零依賴）
pip install designkit-cli

# 或直接克隆執行
git clone https://github.com/gitstq/designkit-cli.git
cd designkit-cli
pip install -e .

# 如需 TUI 預覽（可選）：
pip install rich

# 👇 現在就試試這些命令：
designkit list                          # 查看全部 7 套主題
designkit preview --theme minimal       # 預覽主題
designkit export --theme minimal --format css   # 匯出令牌
designkit palette "#6366f1"             # 生成配色方案
designkit prompt --theme neon --model glm      # 生成 AI 提示詞
```

**環境要求**：Python 3.8+（核心：零依賴；TUI 預覽：可選 Rich 函式庫）

---

## 📖 詳細使用指南

### `designkit list` — 瀏覽主題

```bash
designkit list
```

列出所有 7 套內建設計主題及其描述：

| 主題 ID | 名稱 | 風格描述 |
|---------|------|----------|
| `minimal` | 極簡 Minimal | 乾淨、留白驅動的設計，適合內容型應用 |
| `brutalist` | 粗野主義 Brutalist | 大膽、高對比、粗獷的設計語言 |
| `warm` | 溫暖 Warm | 柔和、親近、人性化的設計 |
| `neon` | 霓虹 Neon | 充滿活力的暗色模式數位美學 |
| `corporate` | 商務 Corporate | 專業、可信、資料密集的設計 |
| `playful` | 活潑 Playful | 有趣、多彩、圓潤的設計 |
| `nature` | 自然 Nature | 有機、平靜、自然靈感的設計 |

### `designkit preview` — 終端預覽

```bash
# 依次預覽所有主題
designkit preview

# 預覽特定主題
designkit preview --theme neon
```

> **💎 專業提示：** 安裝 `rich` 函式庫後可獲得炫酷的彩色終端體驗，包括即時色板、排版表格、間距柱狀圖和模擬元件預覽。

### `designkit export` — 匯出設計令牌

```bash
designkit export --theme minimal --format css        # CSS 自訂屬性
designkit export --theme minimal --format json       # 結構化 JSON
designkit export --theme minimal --format tailwind   # Tailwind 配置
designkit export --theme minimal --format scss       # SCSS 變數
designkit export --theme minimal --format dtcg       # W3C 設計令牌標準

# 一次匯出所有主題：
designkit export --format css

# 指定輸出路徑：
designkit export --theme playful --format css --output ./my-theme.css
```

### `designkit palette` — 色彩魔法

```bash
# 從任意十六進位顏色生成完整調色板
designkit palette "#6366f1"

# 簡寫格式同樣支援
designkit palette ff6b6b
```

輸出包含：11 級主色調色板、中性灰調色板、互補色、近似色、三分色配色方案，以及前景文字對比度分析。

### `designkit prompt` — AI 提示詞生成

```bash
# 生成 GLM-5.1 優化提示詞（預設）
designkit prompt --theme minimal --model glm

# 生成 GPT-4o 優化提示詞
designkit prompt --theme neon --model openai

# 生成 Claude 優化提示詞
designkit prompt --theme warm --model claude

# 生成元件專屬提示詞
designkit prompt --theme minimal --model glm --component "Card" --framework React
```

生成的提示詞包含完整的設計系統上下文（色彩、排版、間距、動效、視覺密度）——確保你的 AI 始終生成符合所選設計語言的程式碼。

---

## 📦 匯出格式

| 格式 | 檔案副檔名 | 描述 | 適用場景 |
|------|----------|------|----------|
| **CSS** | `.css` | CSS 自訂屬性（`--dk-*`） | 任意 Web 專案 |
| **JSON** | `.json` | 結構化巢狀令牌 | 程式化使用 |
| **Tailwind** | `.config.js` | Tailwind CSS `extend` 配置 | Tailwind 專案 |
| **SCSS** | `.scss` | SCSS 變數和對應表 | Sass 專案 |
| **DTCG** | `.tokens.json` | W3C 設計令牌標準格式 | 設計工具互通 |

---

## 🤖 AI 提示詞整合

DesignKit-CLI 專為 AI 輔助開發時代而生。它生成的結構化設計令牌可以直接注入到 AI 編碼助手的上下文中：

### 支援的 AI 模型

| 模型 | 提示詞特色 |
|------|-----------|
| **GLM-5.1** 🏆 | 中文優化，詳細設計參數說明，清晰的程式碼生成要求 |
| **GPT-4o** | 英文優化，精確數值驅動 |
| **Claude** | 簡潔指令風格，注重品質和可存取性 |

### 使用場景

1. **統一團隊設計語言** — 將匯出的 AI 提示詞放入專案 `.claude.md` 或 `.cursorrules`
2. **快速原型開發** — 用 `designkit prompt` 生成設計上下文，讓 AI 一鍵生成元件
3. **設計系統遷移** — 在不同專案間快速切換設計風格

---

## 💡 設計理念與發展藍圖

### 設計理念

DesignKit-CLI 誕生於一個簡單的觀察：**AI 生成的介面看起來都一個樣**。無論是 GPT-4o、GLM-5.1 還是 Claude——沒有明確的設計指引，AI 輸出的都是千篇一律的通用介面。

受 [taste-skill](https://github.com/Leonxlnx/taste-skill)（GitHub 37K+ Stars）的啟發，DesignKit-CLI 採取了更全面的方法：

1. **🎯 令牌勝於指令** — 不是單純告訴 AI"讓它好看"，而是提供精確的數值設計令牌
2. **🔄 即時預覽** — 在投入程式碼之前，先在終端機中看到設計系統變成現實
3. **🌐 多格式輸出** — 匯出到你專案實際使用的格式（CSS、Tailwind、SCSS 等）
4. **🤖 AI 原生** — 專為 AI 輔助開發時代設計，為每個主流模型提供提示詞模板
5. **🔧 零依賴** — 核心功能僅依賴 Python 標準函式庫

### 發展藍圖

- [ ] **自訂主題建構器** — 互動式 CLI 嚮導，從零建立主題
- [ ] **元件庫整合** — 預建設計系統元件 CSS（按鈕、卡片、表單、導航）
- [ ] **Figma 外掛支援** — 從 Figma 匯入/匯出令牌
- [ ] **Web UI** — 簡單的 Web 端主題設計器
- [ ] **暗色模式切換** — 自動生成淺色和深色兩套令牌
- [ ] **更多 AI 模型** — DeepSeek、Qwen、Gemini 提示詞模板
- [ ] **國際化** — RTL 語言支援令牌

---

## 🤝 貢獻指南

歡迎參與貢獻！以下是參與方式：

1. 🍴 **Fork** 本倉庫
2. 🌿 **建立** 功能分支（`git checkout -b feature/amazing`）
3. 💻 **提交** 變更（`git commit -m 'feat: 添加超棒功能'`）
4. 📤 **推送** 到分支（`git push origin feature/amazing`）
5. 🔄 **發起** Pull Request

提交訊息請遵循 [Angular 提交規範](https://www.conventionalcommits.org/)。

**回饋問題**：發現了 Bug？有好點子？[提交 Issue](https://github.com/gitstq/designkit-cli/issues)

---

## 📄 開源協議

本專案採用 **MIT 許可證**——詳見 [LICENSE](./LICENSE) 檔案。

---

<p align="center">
  <sub>用 ❤️ 構建 · DesignKit Team · 靈感來源於 <a href="https://github.com/Leonxlnx/taste-skill">taste-skill</a></sub>
</p>
<p align="center">
  <sub><a href="./README.md">🇬🇧 English</a> · <a href="./README.zh-CN.md">🇨🇳 简体中文</a> · 🇭🇰 繁體中文</sub>
</p>