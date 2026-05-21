#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量添加 nav-right-group 和 lang-switch 的 CSS 样式到所有博客文件
"""
import glob
import re
import sys

# 从 index.html 提取的完整 CSS 样式
CSS_TO_ADD = """    /* Language switcher in nav */
    .nav-right-group {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }
    .lang-switch { position: relative; }
    .lang-switch-btn {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 4px 10px;
      border-radius: 8px;
      border: 1px solid var(--gray-200);
      background: transparent;
      cursor: pointer;
      font-size: .9rem;
      color: var(--gray-600);
      transition: all var(--transition-base);
      line-height: 1;
    }
    .lang-switch-btn:hover {
      border-color: var(--blue);
      color: var(--blue);
    }
    .lang-switch-menu {
      position: absolute;
      top: calc(100% + 6px);
      right: 0;
      background: #fff;
      border: 1px solid var(--gray-200);
      border-radius: 8px;
      box-shadow: var(--shadow-md);
      min-width: 150px;
      opacity: 0;
      pointer-events: none;
      transform: translateY(-4px);
      transition: opacity .2s ease, transform .2s ease;
      z-index: 200;
    }
    .lang-switch-menu.open {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
    }
    .lang-switch-item {
      display: block;
      padding: 10px 16px;
      font-size: .9rem;
      color: var(--gray-700);
      transition: background .15s;
      white-space: nowrap;
    }
    .lang-switch-item:hover {
      background: var(--blue-light);
      color: var(--blue);
    }
    .lang-switch-item:first-child { border-radius: 7px 7px 0 0; }
    .lang-switch-item:last-child { border-radius: 0 0 7px 7px; }
    [data-theme="dark"] .lang-switch-btn {
      border-color: var(--gray-200);
      color: var(--gray-600);
    }
    [data-theme="dark"] .lang-switch-btn:hover {
      border-color: var(--blue);
      color: var(--blue);
    }
    [data-theme="dark"] .lang-switch-menu {
      background: #0B0F1A;
      border-color: var(--gray-200);
    }
    [data-theme="dark"] .lang-switch-item {
      color: var(--gray-700);
    }
    [data-theme="dark"] .lang-switch-item:hover {
      background: rgba(99,102,241,.12);
      color: var(--blue);
    }
"""

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 检查是否已经存在 .nav-right-group CSS
    if '.nav-right-group {' in html:
        print(f"  ⏭️  已存在CSS，跳过: {path}")
        return False

    # 找到 </style> 标签并在其前面插入 CSS
    style_end = html.find('</style>')
    if style_end == -1:
        print(f"  ⚠️  未找到 </style> 标签: {path}")
        return False

    # 在 </style> 之前插入 CSS
    new_html = html[:style_end] + CSS_TO_ADD + html[style_end:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"  ✅ 已添加CSS: {path}")
    return True

def main():
    files = sorted(glob.glob('blog/*.html'))
    print(f"共找到 {len(files)} 个博客文件")
    print("=" * 50)

    success = 0
    for path in files:
        if process_file(path):
            success += 1

    print()
    print(f"结果: 成功添加CSS {success}/{len(files)} 个文件")

if __name__ == '__main__':
    main()
