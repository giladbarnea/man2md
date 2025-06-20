#!/usr/bin/env python3
"""
man2md - Convert raw man pages to markdown
"""

import sys
import re
from pathlib import Path
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional

# --- State Management ---


class ParserState(Enum):
    """Defines the current state of the parser."""

    NORMAL = auto()
    TP_BLOCK_TERM = auto()  # Expecting the term for a .TP block
    SYNOPSIS = auto()


@dataclass
class ParseContext:
    """Holds the parser's state and output buffers."""

    state: ParserState = ParserState.NORMAL
    markdown_lines: List[str] = field(default_factory=list)
    synopsis_buffer: List[str] = field(default_factory=list)
    command_name: Optional[str] = None


# --- Text and Synopsis Formatting ---


def process_text_formatting(line: str) -> str:
    """Process text formatting in a line"""
    # Convert \fI...\fP to **bold** (italic in man pages often means emphasis)
    line = re.sub(r"\\fI([^\\]+)\\fP", r"**\1**", line)

    # Convert \fB...\fP to `code` (bold in man pages often means literal text)
    line = re.sub(r"\\fB([^\\]+)\\fP", r"`\1`", line)

    # Handle special characters that need escaping
    line = line.replace("\\&", "")
    line = line.replace("\\-", "-")
    line = line.replace("\\.", ".")
    line = line.replace("\\\\", "\\")

    # Handle quotes - fix unprocessed formatting
    line = re.sub(r"\\fB([^\\]*?)\\fP", r"`\1`", line)
    line = re.sub(r"\\fI([^\\]*?)\\fP", r"**\1**", line)

    # Clean up any remaining backslash sequences
    line = re.sub(r"\\f[BIRP]", "", line)

    return line


def _flush_synopsis_buffer(context: ParseContext):
    """Format and flush the synopsis buffer"""
    if not context.synopsis_buffer:
        return

    result = []
    current_command = []

    for line in context.synopsis_buffer:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('.Nm'):
            # Start of a new command - flush previous one
            if current_command:
                cmd_text = _format_single_command(current_command)
                if cmd_text:
                    result.append(f"`{cmd_text}`")
                current_command = []
            
            # Add the command name
            if len(line) > 3:
                current_command.append(line[4:].strip())
            else:
                current_command.append(context.command_name or "command")
        else:
            # Add to current command
            current_command.append(line)
    
    # Don't forget the last command
    if current_command:
        cmd_text = _format_single_command(current_command)
        if cmd_text:
            result.append(f"`{cmd_text}`")

    # Add the formatted commands to the output
    context.markdown_lines.extend(result)
    context.synopsis_buffer = []

def _format_single_command(command_parts):
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

def process_bsd_macros(line: str, context: ParseContext) -> str:
    """Process BSD-style man page macros"""
    # Handle .Nm (command name) - if it's a bare .Nm, it references the command name
    if line.startswith(".Nm"):
        if len(line.strip()) == 3:  # Just .Nm with no arguments
            return f"`{context.command_name or 'command'}`"
        elif len(line) > 3:
            return f"`{line[4:].strip()}`"
        return ""

    # Handle synopsis lines - collect multiple elements on one line
    if any(macro in line for macro in [".Fl", ".Op", ".Ar"]):
        # Start with the full line and process all macros
        result = line

        # .Fl flag -> -flag
        result = re.sub(r"\.Fl\s+(\w+)", r"-\1", result)

        # .Op content -> [content] (but process inner content first)
        while ".Op " in result:
            # Find .Op and process its content
            match = re.search(r"\.Op\s+(.+?)(?=\s+\.|$)", result)
            if match:
                op_content = match.group(1).strip()
                # Process inner macros in the optional content
                op_content = re.sub(r"\.Fl\s+(\w+)", r"-\1", op_content)
                op_content = re.sub(r"\.Ar\s+(\w+)", r"\1", op_content)
                result = result.replace(match.group(0), f"[{op_content}]")
            else:
                break

        # .Ar argument -> argument (for remaining ones)
        result = re.sub(r"\.Ar\s+(\w+)", r"\1", result)

        # Clean up any remaining dots and extra whitespace
        result = re.sub(r"^\.*\s*", "", result)
        result = re.sub(r"\s+", " ", result).strip()

        if result:
            return f"`{result}`"

    return ""


# --- Directive Handlers ---


def _handle_title(line: str, context: ParseContext):
    """Handle title headers (.TH, .Dt)"""
    if line.startswith(".TH "):
        parts = line.split('"')
        if len(parts) >= 2:
            title = parts[1]
            section = parts[3] if len(parts) >= 4 else "1"
            context.markdown_lines.append(f"# {title}({section})")
            context.markdown_lines.append("")
            context.command_name = title.lower()
    elif line.startswith(".Dt "):
        parts = line.split()
        if len(parts) >= 3:
            title = parts[1]
            section = parts[2]
            context.markdown_lines.append(f"# {title}({section})")
            context.markdown_lines.append("")
            context.command_name = title.lower()


def _handle_section(line: str, context: ParseContext):
    """Handle section headers (.SH, .Sh)"""
    # Flush any pending synopsis buffer
    if context.state == ParserState.SYNOPSIS and context.synopsis_buffer:
        _flush_synopsis_buffer(context)

    if line.startswith(".SH "):
        section_name = line[4:].strip().strip('"')
        context.markdown_lines.append(f"## {section_name}")
        context.markdown_lines.append("")
        context.state = ParserState.NORMAL
    elif line.startswith(".Sh "):
        section_name = line[4:].strip()
        context.markdown_lines.append(f"## {section_name}")
        context.markdown_lines.append("")
        context.state = (
            ParserState.SYNOPSIS if section_name == "SYNOPSIS" else ParserState.NORMAL
        )


def _handle_subsection(line: str, context: ParseContext):
    """Handle subsection header (.SS)"""
    subsection_name = line[4:].strip().strip('"')
    context.markdown_lines.append(f"### {subsection_name}")
    context.markdown_lines.append("")
    context.state = ParserState.NORMAL


def _handle_tp(line: str, context: ParseContext):
    """Handle term-paragraph block (.TP)"""
    context.state = ParserState.TP_BLOCK_TERM


def _handle_paragraph(line: str, context: ParseContext):
    """Handle paragraph directives (.PP, .Pp)"""
    if context.markdown_lines and context.markdown_lines[-1] != "":
        context.markdown_lines.append("")
    context.state = ParserState.NORMAL


def _handle_name_section(line: str, next_line: str, context: ParseContext) -> bool:
    """Handle NAME section with .Nm and .Nd"""
    if next_line.startswith(".Nd "):
        name = line[4:].strip()
        description = next_line[4:].strip()
        context.markdown_lines.append(f"{name} – {description}")
        context.markdown_lines.append("")
        return True
    return False


def _handle_text_line(line: str, context: ParseContext):
    """Handle regular text lines based on current state"""
    if not line.strip():
        return

    # Process text formatting
    processed_line = process_text_formatting(line)

    # Handle TP blocks specially
    if context.state == ParserState.TP_BLOCK_TERM:
        # This is the term/header for the TP block
        context.markdown_lines.append("")
        # Remove existing formatting since we're adding our own
        clean_line = re.sub(r"\*\*([^*]+)\*\*", r"\1", processed_line)
        context.markdown_lines.append(f"**{clean_line}**")
        context.state = ParserState.NORMAL
    else:
        context.markdown_lines.append(processed_line)


# --- Main Parsing Function ---


def parse_man_page(content: str) -> str:
    """Convert raw man page content to markdown"""
    lines = content.split("\n")
    context = ParseContext()

    i = 0
    while i < len(lines):
        line = lines[i]

        # Skip empty lines at start
        if not line.strip() and not context.markdown_lines:
            i += 1
            continue

        # Handle .TH (title header) - traditional man format
        if line.startswith((".TH ", ".Dt ")):
            _handle_title(line, context)
            i += 1
            continue

        # Handle section headers
        if line.startswith((".SH ", ".Sh ")):
            _handle_section(line, context)
            i += 1
            continue

        # Handle subsection header
        if line.startswith(".SS "):
            _handle_subsection(line, context)
            i += 1
            continue

        # Handle term-paragraph blocks
        if line.startswith(".TP"):
            _handle_tp(line, context)
            i += 1
            continue

        # Handle paragraph breaks
        if line.startswith((".PP", ".Pp")):
            _handle_paragraph(line, context)
            i += 1
            continue

        # Skip certain directives
        if line.startswith((".PD", ".Os", ".Dd", '."')):
            i += 1
            continue

        # Handle NAME section with .Nm and .Nd
        if line.startswith(".Nm "):
            if i + 1 < len(lines) and _handle_name_section(line, lines[i + 1], context):
                i += 2  # Skip both .Nm and .Nd lines
                continue

        # Handle other directives and text
        if line.startswith("."):
            if context.state == ParserState.SYNOPSIS:
                # Buffer synopsis lines for special formatting
                context.synopsis_buffer.append(line)
            else:
                # Convert BSD macros to readable text
                processed_line = process_bsd_macros(line, context)
                if processed_line:
                    context.markdown_lines.append(processed_line)
        elif line.strip():
            # Regular text line
            if context.state == ParserState.SYNOPSIS:
                context.synopsis_buffer.append(line)
            else:
                _handle_text_line(line, context)

        i += 1

    # Flush any remaining synopsis buffer at the end
    if context.state == ParserState.SYNOPSIS and context.synopsis_buffer:
        _flush_synopsis_buffer(context)

    return "\n".join(context.markdown_lines)


def main():
    if len(sys.argv) != 2:
        print("Usage: man2md.py <man_page_file>", file=sys.stderr)
        sys.exit(1)
        
    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"Error: File {input_file} not found", file=sys.stderr)
        sys.exit(1)
        
    try:
        content = input_file.read_text(encoding="utf-8", errors="ignore")
        markdown = parse_man_page(content)
        print(markdown)
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
