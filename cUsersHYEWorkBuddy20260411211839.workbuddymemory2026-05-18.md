# 2026-05-18 工作日志

## 生产事故：整个网站 404

**现象**：用户报告"整个网站打不开了"，所有页面返回 404 NOT_FOUND。

**排查过程**：
1. 检查 `vercel.json` 配置（发现 `frame-ancestors` 拼写错误，但其实是正确的）
2. 检查 `package.json` 是否存在（存在，但只有 `jsdom` 依赖，没有 build 脚本）
3. 添加 `"buildCommand": null` 和 `"installCommand": null` 到 `vercel.json`
4. 重命名 `package.json` 为 `package.json.bak`
5. 创建测试文件（`test-deploy.txt`）验证 Vercel 是否服务文件
6. 所有测试都 404，说明 Vercel 根本没有服务任何文件
7. 添加 `"outputDirectory": "."` 到 `vercel.json`
8. 网站恢复（HTTP 200）

**根因**：Vercel 需要显式配置 `"outputDirectory": "."` 才能正确服务纯静态文件。之前 Vercel 可能错误地配置了输出目录（例如 `build/` 或 `dist/`），导致部署空项目，从而 404。

**修复**：添加 `"outputDirectory": "."` 到 `vercel.json`。

**验证**：所有关键页面返回 200（`/`, `/about`, `/contact`, `/ja/`）。

## 提交记录

1. `fix: add buildCommand null to vercel.json to prevent build attempts causing 404`
2. `fix: add installCommand null to prevent npm install on Vercel`
3. `test: rename package.json to diagnose Vercel 404 issue`
4. `test: add test-deploy.txt to verify Vercel deployment`
5. `fix: add outputDirectory to vercel.json + test file to trigger deploy`
6. `cleanup: remove test files after 404 fix`

## 经验总结

- **Vercel 纯静态网站部署**：必须在 `vercel.json` 中显式设置：
  - `"buildCommand": null`
  - `"installCommand": null`
  - `"outputDirectory": "."`
- **诊断 404 问题**：创建测试文件（例如 `test.txt`）并推送到 GitHub，观察 Vercel 是否服务该文件
- **Vercel 项目存在性验证**：访问 `https://vercel.com/gh/<user>/<repo>` 确认项目存在

## 待办

- [ ] 恢复 `package.json`（本地使用，不推送）
- [ ] 更新 `MEMORY.md` 记录 Vercel 部署经验
- [ ] 检查 Vercel 控制台确认部署配置正确
