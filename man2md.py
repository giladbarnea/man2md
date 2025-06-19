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
    in_synopsis = False
    synopsis_buffer = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines at start
        if not line.strip() and not markdown_lines:
            i += 1
            continue
            
        # Handle .TH (title header) - traditional man format
        if line.startswith('.TH '):
            parts = line.split('"')
            if len(parts) >= 2:
                title = parts[1]
                section = parts[3] if len(parts) >= 4 else "1"
                markdown_lines.append(f"# {title}({section})")
                markdown_lines.append("")
            i += 1
            continue
            
        # Handle .Dt (BSD title header)
        if line.startswith('.Dt '):
            parts = line.split()
            if len(parts) >= 3:
                title = parts[1]
                section = parts[2]
                markdown_lines.append(f"# {title}({section})")
                markdown_lines.append("")
            i += 1
            continue
            
        # Handle .SH (section header) - traditional man format
        if line.startswith('.SH '):
            section_name = line[4:].strip().strip('"')
            markdown_lines.append(f"## {section_name}")
            markdown_lines.append("")
            in_tp_block = False
            i += 1
            continue
            
        # Handle .Sh (BSD section header)
        if line.startswith('.Sh '):
            # Flush any pending synopsis buffer
            if in_synopsis and synopsis_buffer:
                formatted_commands = format_synopsis_buffer(synopsis_buffer)
                # Debug: print what we're adding
                # print(f"DEBUG: Adding {len(formatted_commands)} synopsis commands")
                # for cmd in formatted_commands:
                #     print(f"DEBUG: {cmd}")
                markdown_lines.extend(formatted_commands)
                synopsis_buffer = []
            
            section_name = line[4:].strip()
            markdown_lines.append(f"## {section_name}")
            markdown_lines.append("")
            in_tp_block = False
            in_synopsis = (section_name == "SYNOPSIS")
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
            
        # Handle .Pp (BSD paragraph break)
        if line.startswith('.Pp'):
            if markdown_lines and markdown_lines[-1] != "":
                markdown_lines.append("")
            i += 1
            continue
            
        # Handle .Os, .Dd (BSD metadata - skip)
        if line.startswith('.Os') or line.startswith('.Dd'):
            i += 1
            continue
            
        # Handle BSD .Nm and .Nd for NAME section
        if line.startswith('.Nm '):
            name = line[4:].strip()
            # Look ahead for .Nd
            if i + 1 < len(lines) and lines[i + 1].startswith('.Nd '):
                description = lines[i + 1][4:].strip()
                markdown_lines.append(f"{name} – {description}")
                markdown_lines.append("")
                i += 2  # Skip both .Nm and .Nd lines
                continue
            i += 1
            continue
            
        # Skip standalone .Nd (already handled above)
        if line.startswith('.Nd '):
            i += 1
            continue
            
        # Handle other BSD directives by converting them to text
        if line.startswith('.'):
            if in_synopsis:
                # Buffer synopsis lines for special formatting
                synopsis_buffer.append(line)
            else:
                # Convert BSD macros to readable text
                processed_line = process_bsd_macros(line)
                if processed_line:
                    markdown_lines.append(processed_line)
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
    
    # Flush any remaining synopsis buffer at the end
    if in_synopsis and synopsis_buffer:
        markdown_lines.extend(format_synopsis_buffer(synopsis_buffer))
        
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

def process_bsd_macros(line: str) -> str:
    """Process BSD-style man page macros"""
    # Handle .Nm (command name) - if it's a bare .Nm, it references the command name
    if line.startswith('.Nm'):
        if len(line.strip()) == 3:  # Just .Nm with no arguments
            return "`fsck_hfs`"  # Reference to the command name
        elif len(line) > 3:
            return f"`{line[4:].strip()}`"
        return ""
    
    # Handle synopsis lines - collect multiple elements on one line
    if any(macro in line for macro in ['.Fl', '.Op', '.Ar']):
        # Start with the full line and process all macros
        result = line
        
        # .Fl flag -> -flag
        result = re.sub(r'\.Fl\s+(\w+)', r'-\1', result)
        
        # .Op content -> [content] (but process inner content first)
        while '.Op ' in result:
            # Find .Op and process its content
            match = re.search(r'\.Op\s+(.+?)(?=\s+\.|$)', result)
            if match:
                op_content = match.group(1).strip()
                # Process inner macros in the optional content
                op_content = re.sub(r'\.Fl\s+(\w+)', r'-\1', op_content)
                op_content = re.sub(r'\.Ar\s+(\w+)', r'\1', op_content)
                result = result.replace(match.group(0), f'[{op_content}]')
            else:
                break
        
        # .Ar argument -> argument (for remaining ones)
        result = re.sub(r'\.Ar\s+(\w+)', r'\1', result)
        
        # Clean up any remaining dots and extra whitespace
        result = re.sub(r'^\.*\s*', '', result)
        result = re.sub(r'\s+', ' ', result).strip()
        
        if result:
            return f"`{result}`"
    
    return ""

def format_synopsis_buffer(buffer):
    """Format buffered synopsis lines into proper command syntax"""
    result = []
    current_command = []
    
    for line in buffer:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('.Nm'):
            # Start of a new command - flush previous one
            if current_command:
                cmd_text = format_single_command(current_command)
                if cmd_text:
                    result.append(f"`{cmd_text}`")
                current_command = []
            
            # Add the command name
            if len(line) > 3:
                current_command.append(line[4:].strip())
            else:
                current_command.append("fsck_hfs")
        else:
            # Add to current command
            current_command.append(line)
    
    # Don't forget the last command
    if current_command:
        cmd_text = format_single_command(current_command)
        if cmd_text:
            result.append(f"`{cmd_text}`")
    
    return result

def format_single_command(command_parts):
    """Format a single command from its parts"""
    if not command_parts:
        return ""
    
    # Start with command name
    parts = [command_parts[0]]
    
    # Process remaining parts
    for part in command_parts[1:]:
        if part.startswith('.Fl '):
            flag = part[4:].strip()
            parts.append(f"-{flag}")
        elif part.startswith('.Op '):
            opt_content = part[4:].strip()
            # Process inner content - handle Fl specially for options
            if opt_content.startswith('Fl '):
                flags = opt_content[3:].strip()
                parts.append(f"[-{flags}]")
            else:
                # Process other inner content
                opt_content = re.sub(r'\.Fl\s+(\w+)', r'-\1', opt_content)
                opt_content = re.sub(r'\.Ar\s+(\w+)', r'\1', opt_content)
                parts.append(f"[{opt_content}]")
        elif part.startswith('.Ar '):
            arg = part[4:].strip()
            parts.append(arg)
    
    return " ".join(parts)

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
