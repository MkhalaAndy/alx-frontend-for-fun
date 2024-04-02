#!/usr/bin/python3
"""
Markdown to HTML Converters
"""

import sys
import re

def parse_heading(line):
    """
    Parse heading Markdown syntax and generate HTML
    """
    heading_level = line.count('#')
    heading_text = line.strip('#').strip()
    return f"<h{heading_level}>{heading_text}</h{heading_level}>\n"

def parse_unordered_list(line):
    """
    Parse unordered listing Markdown syntax and generate HTML
    """
    items = line.strip('-').strip().split('\n')
    html = "<ul>\n"
    for item in items:
        html += f"<li>{item.strip()}</li>\n"
    html += "</ul>\n"
    return html

def parse_ordered_list(line):
    """
    Parse ordered listing Markdown syntax and generate HTML
    """
    items = line.strip('*').strip().split('\n')
    html = "<ol>\n"
    for item in items:
        html += f"<li>{item.strip()}</li>\n"
    html += "</ol>\n"
    return html

def parse_paragraph(line):
    """
    Parse paragraph Markdown syntax and generate HTML
    """
    paragraphs = line.split('\n\n')
    html = ""
    for paragraph in paragraphs:
        html += f"<p>\n{paragraph.strip().replace('\n', '<br />\n')}\n</p>\n"
    return html

def parse_bold_and_emphasis(line):
    """
    Parse bold and emphasis Markdown syntax and generate HTML
    """
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
    return line

def parse_custom_syntax(line):
    """
    Parse custom syntax and generate HTML
    """
    line = re.sub(r'\[\[(.*?)\]\]', lambda x: hashlib.md5(x.group(1).encode()).hexdigest(), line)
    line = re.sub(r'\(\((.*?)\)\)', lambda x: x.group(1).replace('c', '').replace('C', ''), line)
    return line

def convert_markdown_to_html(markdown_file, html_file):
    """
    Convert Markdown to HTML
    """
    with open(markdown_file, 'r') as md:
        markdown_content = md.readlines()

    with open(html_file, 'w') as html:
        for line in markdown_content:
            if line.startswith("#"):
                html.write(parse_heading(line))
            elif line.startswith("-"):
                html.write(parse_unordered_list(line))
            elif line.startswith("*"):
                html.write(parse_ordered_list(line))
            else:
                line = parse_bold_and_emphasis(line)
                line = parse_custom_syntax(line)
                html.write(parse_paragraph(line))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py <input_file.md> <output_file.html>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        convert_markdown_to_html(input_file, output_file)
    except FileNotFoundError:
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)
