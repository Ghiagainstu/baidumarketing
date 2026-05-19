# 2026-05-18 工作日志

## 生产事故：整个网站 404

**现象**：用户报告"整个网站打不开了"，所有页面返回 404 NOT_FOUND。

**排查过程**：
1. 检查 `vercel.json` 配置
2. 添加 `"buildCommand": null` 和 `"installCommand": null`
3. 重命名 `package.json` 为 `package.json.bak`
4. 创建测试文件验证 Vercel 是否服务文件
5. **关键发现**：所有文件都 404，Vercel 根本没有服务任何文件
6. **根本原因**：添加 `"outputDirectory": "."` 到 `vercel.json`
7. 网站恢复（HTTP 200）

**根因**：Vercel 需要显式配置 `"outputDirectory": "."` 才能正确服务纯静态文件。

## 修复：why-baidu-ppc-pro 页面问题

**现象**：
1. 第三方图表（StatCounter）不见了
2. 格式似乎也不对
3. 少部分页面打不开语言切换

**修复过程**：
1. 发现 8 个页面没有加载 `main.js`（about.html, china-geo.html, clients.html, faq.html, features.html, privacy.html, terms.html, why-baidu-ppc-pro.html）
2. 创建脚本批量修复这些页面：移除内联 JS，添加 `<script src="/assets/js/main.js" defer></script>`
3. 更新 CSP 允许 StatCounter 域名（`https://www.statcounter.com` 和 `https://gs.statcounter.com`）

## 提交记录

1. `fix: add outputDirectory to vercel.json to prevent build attempts causing 404`
2. `fix: add installCommand null to prevent npm install on Vercel`
3. `test: rename package.json to diagnose Vercel 404 issue`
4. `test: add test-deploy.txt to verify Vercel deployment`
5. `fix: add outputDirectory to vercel.json + test file to trigger deploy`
6. `cleanup: remove test files after 404 fix`
7. `fix: add main.js and remove inline JS from 8 pages; allow StatCounter in CSP`

## 经验教训

### Vercel 纯静态网站部署（关键！）
- **必须**在 `vercel.json` 中设置：
  - `"buildCommand": null`
  - `"installCommand": null`
  - `"outputDirectory": "."` ← 关键！不写此项会导致 Vercel 部署空项目，全部 404
  - `"cleanUrls": true`

### 安全审核检查清单
- 所有 HTML 页面必须加载 `main.js`
- 内联 JS 必须外部化
- 第三方脚本必须在 CSP 中白名单

## 待办

- [ ] 验证 StatCounter 图表是否正常显示
- [ ] 验证所有页面的语言切换是否正常
- [ ] 完成安全审核剩余工作（消除 `style-src` 的 `'unsafe-inline'`、切换到强制 CSP 等）
