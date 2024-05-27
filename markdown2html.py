#!/usr/bin/python3
"""
This is a script to convert a Markdown file to HTML.

Usage:
    ./markdown2html.py [input_file] [output_file]

Arguments:
    input_file: the name of the Markdown file to be converted
    output_file: the name of the output HTML file

Example:
    ./markdown2html.py README.md README.html
"""

import sys
import pathlib
import re
import hashlib

def convert_md_to_html(input_file, output_file):
    '''
    Converts markdown file to HTML file
    '''
    # Read the contents of the input file
    with open(input_file, encoding='utf-8') as f:
        md_content = f.readlines()

    html_content = []
    inside_ul = False
    inside_ol = False
    inside_p = False

    def close_list():
        nonlocal inside_ul, inside_ol
        if inside_ul:
            html_content.append('</ul>\n')
            inside_ul = False
        if inside_ol:
            html_content.append('</ol>\n')
            inside_ol = False

    def close_paragraph():
        nonlocal inside_p
        if inside_p:
            html_content.append('</p>\n')
            inside_p = False

    for line in md_content:
        line = line.rstrip()
        # Check if the line is a heading
        match = re.match(r'^(#{1,6}) (.+)', line)
        if match:
            close_list()
            close_paragraph()
            h_level = len(match.group(1))
            h_content = match.group(2)
            html_content.append(f'<h{h_level}>{h_content}</h{h_level}>\n')
        # Check if the line is an unordered list item
        elif re.match(r'^- (.+)', line):
            if not inside_ul:
                close_list()
                close_paragraph()
                html_content.append('<ul>\n')
                inside_ul = True
            item_content = re.sub(r'^- (.+)', r'\1', line)
            html_content.append(f'<li>{item_content}</li>\n')
        # Check if the line is an ordered list item
        elif re.match(r'^\* (.+)', line):
            if not inside_ol:
                close_list()
                close_paragraph()
                html_content.append('<ol>\n')
                inside_ol = True
            item_content = re.sub(r'^\* (.+)', r'\1', line)
            html_content.append(f'<li>{item_content}</li>\n')
        # Check if the line is a blank line
        elif line.strip() == '':
            close_list()
            close_paragraph()
        # Handle paragraph text
        else:
            if not inside_p:
                close_list()
                html_content.append('<p>\n')
                inside_p = True
            else:
                html_content.append('<br/>\n')
            paragraph_content = line.strip()
            # Replace bold syntax
            paragraph_content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', paragraph_content)
            # Replace italic syntax
            paragraph_content = re.sub(r'__(.+?)__', r'<em>\1</em>', paragraph_content)
            # Replace MD5 syntax
            paragraph_content = re.sub(r'\[\[(.+?)\]\]', lambda x: hashlib.md5(x.group(1).encode()).hexdigest(), paragraph_content)
            # Remove 'c' and 'C' from the content
            paragraph_content = re.sub(r'\(\((.+?)\)\)', lambda x: x.group(1).replace('c', '').replace('C', ''), paragraph_content)
            html_content.append(paragraph_content)

    close_paragraph()
    close_list()

    # Write the HTML content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(html_content)

if __name__ == '__main__':
    # Check the number of command-line arguments
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the input file exists
    input_path = pathlib.Path(input_file)
    if not input_path.is_file():
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    # Convert the markdown file to HTML
    convert_md_to_html(input_file, output_file)
    sys.exit(0)
