# Learnings

## [LRN-20260426-001] correction — blog footer container wrapper

**Logged**: 2026-04-26T11:00:00+08:00
**Priority**: high
**Status**: resolved
**Area**: frontend

### Summary
博客文件 footer 内不应包裹 `<div class="container">`，否则 800px max-width 会压缩四栏 footer-top 布局

### Details
给 blog/feed-landing-page-optimization.html 同步首页完整 footer 时，保留了原文件中 `<footer><div class="container"><div class="footer-top">...` 的结构。但首页 footer 的结构是 `<footer><div class="footer-top">...`（无 container wrapper），因为 footer-top CSS 自带 `max-width: 1140px; margin: 0 auto;`。而 .container 有 `max-width: 800px`（博客文章宽度），导致 footer 被压缩到 800px，四栏布局变形。

### Resolution
- **Resolved**: 2026-04-26T11:00:00+08:00
- **Commit**: ca38615
- **Notes**: 移除 `<div class="container">` wrapper，footer-top 直接作为 footer 的子元素

### Metadata
- Source: user_feedback
- Related Files: blog/*.html
- Tags: footer, container, blog, layout
- Recurrence-Count: 1
- First-Seen: 2026-04-26
- Last-Seen: 2026-04-26

---
