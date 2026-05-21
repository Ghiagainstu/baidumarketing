#!/usr/bin/env python3
"""
batch_fix_all_blog.py - 批量修复所有 EN 博客文件
运行 fix_blog_all_in_one.py 和 add_toggleLangMenu.py
"""
import os
import sys
import subprocess
import glob

def main():
    blog_dir = 'blog'
    files = sorted(glob.glob(os.path.join(blog_dir, '*.html')))
    
    print(f"找到 {len(files)} 个博客文件")
    print("=" * 50)
    
    success_count = 0
    failed_files = []
    
    for i, path in enumerate(files, 1):
        slug = os.path.basename(path)
        print(f"\n[{i}/{len(files)}] 处理: {slug}")
        
        # 修复1: fix_blog_all_in_one.py
        try:
            result = subprocess.run(
                ['python', 'fix_blog_all_in_one.py', path],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print(f"  ✅ fix_blog_all_in_one.py 成功")
                for line in result.stdout.strip().split('\n'):
                    if '✅' in line or '⚠️' in line:
                        print(f"    {line.strip()}")
            else:
                print(f"  ❌ fix_blog_all_in_one.py 失败:")
                print(f"    {result.stderr[:200]}")
                failed_files.append((slug, 'fix_blog_all_in_one.py', result.stderr[:200]))
                continue
        except Exception as e:
            print(f"  ❌ fix_blog_all_in_one.py 异常: {e}")
            failed_files.append((slug, 'fix_blog_all_in_one.py', str(e)))
            continue
        
        # 修复2: add_toggleLangMenu.py
        try:
            result = subprocess.run(
                ['python', 'add_toggleLangMenu.py', path],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print(f"  ✅ add_toggleLangMenu.py 成功")
                for line in result.stdout.strip().split('\n'):
                    if '✅' in line or '⚠️' in line:
                        print(f"    {line.strip()}")
            else:
                print(f"  ⚠️ add_toggleLangMenu.py 返回非零: {result.returncode}")
                # 不视为失败，可能文件已经修复
        except Exception as e:
            print(f"  ⚠️ add_toggleLangMenu.py 异常: {e}")
            # 不视为失败
        
        success_count += 1
    
    # 汇总
    print("\n" + "=" * 50)
    print(f"✅ 成功: {success_count}/{len(files)}")
    if failed_files:
        print(f"❌ 失败: {len(failed_files)}")
        for slug, script, error in failed_files[:10]:  # 只显示前10个
            print(f"  - {slug} ({script}): {error[:100]}")
    else:
        print("🎉 所有文件修复完成！")

if __name__ == '__main__':
    main()
