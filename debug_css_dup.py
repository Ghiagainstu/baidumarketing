#!/usr/bin/env python3
"""诊断：测试移除重复 CSS 后是否解决问题"""
import glob

# 只修一个文件做测试
path = 'blog/baidu-ad-billing-models-explained.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# 找到 Bug-specific styles 标记后的重复CSS并检查
# 实际上检查下原始 CSS 区是否有两个 .lang-switch-menu
import re
matches = [(m.start(), m.group()[:60]) for m in re.finditer(r'\.lang-switch-menu\s*\{', html)]
print(f'找到 {len(matches)} 个 .lang-switch-menu {{')
for start, snippet in matches:
    # 显示周围上下文
    ctx = html[max(0,start-50):start+30]
    print(f'  位置 {start}: ...{ctx}...')
