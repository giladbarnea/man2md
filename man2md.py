#!/usr/bin/env python3
"""
man2md - Convert raw man pages to markdown
"""

import sys
import re
from pathlib import Path

def parse_man_page(content: str) -> str:
    """Convert raw man page content to markdown"""
    lines = content.split('\n')
    markdown_lines = []
    in_tp_block = False
    current_tp_term = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines at start
        if not line.strip() and not markdown_lines:
            i += 1
            continue
            
        # Handle .TH (title header)
        if line.startswith('.TH '):
            parts = line.split('"')
            if len(parts) >= 2:
                title = parts[1]
                section = parts[3] if len(parts) >= 4 else "1"
                markdown_lines.append(f"# {title}({section})")
                markdown_lines.append("")
            i += 1
            continue
            
        # Handle .SH (section header)
        if line.startswith('.SH '):
            section_name = line[4:].strip().strip('"')
            markdown_lines.append(f"## {section_name}")
            markdown_lines.append("")
            in_tp_block = False
            i += 1
            continue
            
        # Handle .SS (subsection header)
        if line.startswith('.SS '):
            subsection_name = line[4:].strip().strip('"')
            markdown_lines.append(f"### {subsection_name}")
            markdown_lines.append("")
            in_tp_block = False
            i += 1
            continue
            
        # Handle .TP (term-paragraph) blocks
        if line.startswith('.TP'):
            in_tp_block = True
            current_tp_term = None
            i += 1
            continue
            
        # Handle .PP (paragraph) blocks
        if line.startswith('.PP'):
            if markdown_lines and markdown_lines[-1] != "":
                markdown_lines.append("")
            in_tp_block = False
            i += 1
            continue
            
        # Handle .PD (paragraph distance) - just skip
        if line.startswith('.PD'):
            i += 1
            continue
            
        # Skip comments
        if line.startswith('.\"'):
            i += 1
            continue
            
        # Handle regular text lines
        if line.strip() and not line.startswith('.'):
            # Process text formatting
            processed_line = process_text_formatting(line)
            
            # Handle TP blocks specially
            if in_tp_block:
                # This is the term/header for the TP block
                markdown_lines.append("")
                # Remove existing formatting since we're adding our own
                clean_line = re.sub(r'\*\*([^*]+)\*\*', r'\1', processed_line)
                markdown_lines.append(f"**{clean_line}**")
                in_tp_block = False
                i += 1
                continue
            
            markdown_lines.append(processed_line)
            
        # Skip other man page directives for now
        i += 1
        
    return '\n'.join(markdown_lines)

def process_text_formatting(line: str) -> str:
    """Process text formatting in a line"""
    # Convert \fI...\fP to **bold** (italic in man pages often means emphasis)
    line = re.sub(r'\\fI([^\\]+)\\fP', r'**\1**', line)
    
    # Convert \fB...\fP to `code` (bold in man pages often means literal text)
    line = re.sub(r'\\fB([^\\]+)\\fP', r'`\1`', line)
    
    # Handle special characters that need escaping
    line = line.replace('\\&', '')
    line = line.replace('\\-', '-')
    line = line.replace('\\.', '.')
    line = line.replace('\\\\', '\\')
    
    # Handle quotes - fix unprocessed formatting
    line = re.sub(r'\\fB([^\\]*?)\\fP', r'`\1`', line)
    line = re.sub(r'\\fI([^\\]*?)\\fP', r'**\1**', line)
    
    # Clean up any remaining backslash sequences
    line = re.sub(r'\\f[BIRP]', '', line)
    
    return line

def main():
    if len(sys.argv) != 2:
        print("Usage: man2md.py <man_page_file>", file=sys.stderr)
        sys.exit(1)
        
    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"Error: File {input_file} not found", file=sys.stderr)
        sys.exit(1)
        
    try:
        content = input_file.read_text(encoding='utf-8')
        markdown = parse_man_page(content)
        print(markdown)
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
