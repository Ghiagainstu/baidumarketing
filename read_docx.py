#!/usr/bin/env python3
import zipfile
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

def extract_docx(docx_path, output_dir):
    """解压 DOCX 文件"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(docx_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    
    return output_dir

def read_document_xml(xml_path):
    """读取 document.xml 并提取文本"""
    try:
        # 注册命名空间
        namespaces = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
            'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
            'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
        }
        
        # 解析 XML
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # 提取所有文本
        text_parts = []
        
        # 查找所有 w:t 元素
        for t_elem in root.findall('.//w:t', namespaces):
            if t_elem.text:
                text_parts.append(t_elem.text)
        
        # 合并文本
        full_text = ' '.join(text_parts)
        
        # 尝试提取段落结构
        paragraphs = []
        for p_elem in root.findall('.//w:p', namespaces):
            para_texts = []
            for t_elem in p_elem.findall('.//w:t', namespaces):
                if t_elem.text:
                    para_texts.append(t_elem.text)
            if para_texts:
                paragraphs.append(' '.join(para_texts))
        
        return {
            'full_text': full_text,
            'paragraphs': paragraphs
        }
        
    except Exception as e:
        return {'error': str(e), 'full_text': '', 'paragraphs': []}

def main():
    if len(sys.argv) < 2:
        print("Usage: python read_docx.py <docx_file>")
        sys.exit(1)
    
    docx_path = sys.argv[1]
    if not os.path.exists(docx_path):
        print(f"File not found: {docx_path}")
        sys.exit(1)
    
    # 临时目录
    temp_dir = Path(docx_path).parent / "docx_extract"
    
    try:
        # 解压
        extract_dir = extract_docx(docx_path, temp_dir)
        
        # 查找 document.xml
        xml_path = extract_dir / "word" / "document.xml"
        if not xml_path.exists():
            # 可能在另一个位置
            xml_files = list(extract_dir.rglob("document.xml"))
            if xml_files:
                xml_path = xml_files[0]
            else:
                print("document.xml not found")
                sys.exit(1)
        
        # 读取内容
        result = read_document_xml(xml_path)
        
        if 'error' in result:
            print(f"Error reading XML: {result['error']}")
        else:
            # 写入文件避免编码问题
            output_file = Path(docx_path).parent / "extracted_content.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("DOCX CONTENT EXTRACTED\n")
                f.write("=" * 80 + "\n")
                f.write("\nFull text:\n")
                f.write("-" * 40 + "\n")
                f.write(result['full_text'])
                
                f.write("\n\nParagraphs:\n")
                f.write("-" * 40 + "\n")
                for i, para in enumerate(result['paragraphs']):
                    f.write(f"[{i+1}] {para}\n")
                
                f.write(f"\nTotal paragraphs: {len(result['paragraphs'])}\n")
                f.write(f"Total characters: {len(result['full_text'])}\n")
            
            # 在控制台输出摘要
            print(f"Content extracted and saved to: {output_file}")
            print(f"Total paragraphs: {len(result['paragraphs'])}")
            print(f"Total characters: {len(result['full_text'])}")
            
            # 显示前3段作为预览
            print("\nPreview (first 3 paragraphs):")
            print("-" * 40)
            for i, para in enumerate(result['paragraphs'][:3]):
                preview = para[:150] + "..." if len(para) > 150 else para
                print(f"[{i+1}] {preview}")
        
        # 清理（可选）
        # import shutil
        # shutil.rmtree(temp_dir)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()