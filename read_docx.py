#!/usr/bin/env python3
"""
DOCX 文本提取工具
用法: python read_docx.py <path/to/file.docx>
输出: 文本内容 + 创建时间
"""
import sys
import os
import zipfile
import tempfile
import xml.etree.ElementTree as ET

def extract_docx(docx_path):
    if not os.path.exists(docx_path):
        print(f"ERROR: File not found: {docx_path}", file=sys.stderr)
        sys.exit(1)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(docx_path, 'r') as z:
            z.extractall(tmpdir)
        
        # 提取文本
        doc_path = os.path.join(tmpdir, 'word', 'document.xml')
        if not os.path.exists(doc_path):
            print("ERROR: word/document.xml not found in DOCX", file=sys.stderr)
            sys.exit(1)
        
        tree = ET.parse(doc_path)
        ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        texts = []
        for t in tree.iter(f'{{{ns}}}t'):
            if t.text:
                texts.append(t.text)
        
        content = '\n'.join(texts)
        
        # 提取创建时间
        created = "unknown"
        core_path = os.path.join(tmpdir, 'docProps', 'core.xml')
        if os.path.exists(core_path):
            ctree = ET.parse(core_path)
            for e in ctree.iter():
                tag_lower = e.tag.lower()
                if 'created' in tag_lower and e.text and e.text.strip():
                    created = e.text.strip()
                    break
        
        print("---CONTENT---")
        print(content)
        print("---DATE---")
        print(created)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python read_docx.py <path_to_docx>", file=sys.stderr)
        sys.exit(1)
    extract_docx(sys.argv[1])
