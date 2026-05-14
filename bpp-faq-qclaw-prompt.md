# BPP FAQ QClaw 工作流 — QClaw 撰写 → WorkBuddy 上传网站

> QClaw 产出结构化 Markdown → WorkBuddy 读取后自动更新 `faq.html` / `ja/faq.html`

---

## FAQ 页面结构（了解即可）

当前英文 FAQ 页有 **8 个分类、共 51 个问答**：

| 分类 | 现有问答数 |
|------|-----------|
| Account & Setup | 8 |
| Fees & Budget | 6 |
| Billing & CPC | 3 |
| Compliance & Review | 5 |
| Baidu Feed Ads | 6 |
| Brand Zone Ads | 10 |
| oCPC & Smart Bidding | 7 |
| SEM Optimization | 6 |

每个分类是一个 `<div class="faq-list">` 区块。

---

## 输出格式（QClaw 必须遵守）

QClaw 输出一个 **干净的 Markdown 文件**，包含 YAML frontmatter + 分类分组 + FAQ 列表。

### 场景 A：新增 FAQ（追加到现有英文 FAQ 页）

```markdown
---
title: Baidu Advertising FAQ — New Items
action: append
language: en
target: faq.html
category: Account & Setup
---

## FAQ Items

### 🏢 Can I open a Baidu account without a Chinese domestic company?
**Yes.** Baidu supports account opening for **foreign companies and entities**. You don't
need a Chinese domestic business license to get started — we handle the process for you.

回答内容可以包含 **加粗文本**、[链接](https://baidumarketing.com/contact) 和其他行内格式。

### 🔄 Is there a difference between foreign and Chinese domestic Baidu accounts?
No functional difference. The only distinction is in the ad display: the company name
shown at the bottom of your ads will be either your foreign company name or your Chinese
company name, depending on which entity the account is registered under.
```

**规则**：
- `category` 必须匹配现有分类名之一（如上表）
- 新增项目追加到该分类的 `<div class="faq-list">` 末尾
- 每项以 `### [Emoji] [问题]` 开头，回答在下一段
- Emoji 必须！每个 FAQ 都要有

### 场景 B：新增分类 + FAQ（创建新分类区块）

```markdown
---
title: Baidu Advertising FAQ — New Section
action: append
language: en
target: faq.html
category: New Category Name   ← 如果不在现有 8 个分类中，就创建新分类
category_icon: chart   ← 可选：chart / shield / dollar / search / feed / target / star / settings
---

## FAQ Items

### 📈 New FAQ question here?
**Answer** here...
```
---

## 命名规范

保存到 Obsidian 时使用以下命名：
- `E:/Obsidian/Baidu/08-Baidu-Basics/faq-{描述}-{语言}.md`
- 示例：`faq-international-brands-en.md` / `faq-international-brands-jp.md`

---

# WorkBuddy 处理指令

## 读取 FAQ Markdown 后，WorkBuddy 自动执行：

### Step 1：解析 frontmatter
- `action`: append（追加）/ translate（翻译替换）/ new（全新页面）
- `language`: en / ja / ko / zh / ...
- `target`: faq.html / ja/faq.html / tr/faq.html
- `source_language`: 翻译源语言（如果是 translate）

### Step 2：解析 FAQ 列表

两种格式都支持：
- `### 问题?` + 下一行回答（Markdown 标题格式）
- `- question: "..."` + `answer: "..."`（YAML 列表格式）

### Step 3：生成 HTML 内容

每个 FAQ 项目生成：
```html
<div class="faq-item">
  <button class="faq-question" onclick="toggleFaq(this)">
    [Emoji] [问题]
    <span class="faq-icon">+</span>
  </button>
  <div class="faq-answer">
    [回答（保留 HTML 标记如 <strong>、<a>、<br>）]
  </div>
</div>
```

和对应 JSON-LD 条目：
```json
{
  "@type": "Question",
  "name": "[Emoji] [问题]",
  "acceptedAnswer": {
    "@type": "Answer",
    "text": "[回答（纯文本，去掉 Markdown/HTML 标记）]"
  }
}
```

### Step 4：更新目标文件

**append** → 在目标 faq.html 的 `<div class="faq-section">` 末尾追加新条目，并在 JSON-LD 数组中追加条目

**translate** → 替换目标 faq.html 中对应条目的文本（保留 HTML 结构），如有 JSON-LD 也同步翻译

**new** → 从 `bpp-template-ultimate` 模板创建全新的 faq.html，填充所有 FAQ 条目

### Step 5：更新 sitemap + git push

如果创建了新页面（new / translate），更新 sitemap.xml 并 git push。
如果是追加已有页面（append），直接 git push 即可。

---

## FAQ 写作规则（给 QClaw）

1. **每个 FAQ 必须有 emoji 开头** — 视觉标识，让页面更生动
2. **回答要简洁** — 2-4 句话，不超过 100 字
3. **可加粗关键词** — 用 `**关键字**` 标记核心信息
4. **可加链接** — 需要时用 `[描述](链接)` 指向相关页面
5. **语气** — 专业、直接、有帮助，不用 AI 废话
6. **去 AI 味** — 禁用：additionally / leverage / it is important to note / please feel free to
7. **数据要准** — 涉及金额、百分比、天数时必须准确

---

**版本历史**
- v1.0 (2026-05-14)：初始版本，FAQ 双阶段工作流
