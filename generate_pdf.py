#!/usr/bin/env python3
"""
Builds a publication-ready PDF for Eigenmode Orbital Dynamics.
Converts Markdown -> HTML (with KaTeX rendering & Mermaid handling) -> PDF via Brave Headless.
"""

import os
import re
import subprocess
import sys
import shutil
import markdown

PAPER_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(PAPER_DIR, "EIGENMODE-ORBITAL-DYNAMICS.md")
HTML_STAGE1 = "/tmp/eigenmode_stage1.html"
HTML_STAGE2 = "/tmp/eigenmode_stage2.html"
PDF_OUT = os.path.join(PAPER_DIR, "EIGENMODE-ORBITAL-DYNAMICS.pdf")

def build_pdf():
    print(f"Reading markdown from: {MD_PATH}")
    with open(MD_PATH, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Strip top navigation links from the print document
    md_text = re.sub(r'^\[←.*?\]\(.*?\)\s*(\|.*?)?\n+', '', md_text, flags=re.MULTILINE)

    # Pre-process mermaid diagrams to an attractive block or diagram
    mermaid_pattern = re.compile(r'```mermaid\s*\n(.*?)\n```', re.DOTALL)
    def replace_mermaid(match):
        code = match.group(1)
        # Format the flowchart nicely for print
        lines = [line.strip() for line in code.split('\n') if line.strip() and not line.strip().startswith('flowchart')]
        flow_steps = []
        for l in lines:
            if '-->' in l:
                parts = l.split('-->')
                left = parts[0].strip()
                right = parts[1].strip()
                label = ""
                if '|' in right:
                    label_parts = right.split('|')
                    if len(label_parts) >= 3:
                        label = label_parts[1]
                        right = label_parts[2]
                flow_steps.append((left, label, right))
        
        # Build clean HTML flowchart
        html_box = '<div class="flowchart-box"><div class="flowchart-title">System Architecture Flow</div>'
        html_box += '<pre class="mermaid-code">' + code + '</pre></div>'
        return html_box

    processed_md = mermaid_pattern.sub(replace_mermaid, md_text)

    # Protect formulas from markdown mangling
    # We will temporarily replace $$...$$ and $...$ with placeholders
    math_blocks = []
    math_inlines = []

    def save_block_math(match):
        math_blocks.append(match.group(0))
        return f"%%MATHBLOCK{len(math_blocks)-1}%%"

    def save_inline_math(match):
        math_inlines.append(match.group(0))
        return f"%%MATHINLINE{len(math_inlines)-1}%%"

    # Replace block math first ($$...$$)
    processed_md = re.sub(r'\$\$(.*?)\$\$', save_block_math, processed_md, flags=re.DOTALL)
    # Replace inline math ($...$) - ensure not empty and not multiple $$
    processed_md = re.sub(r'(?<!\$)\$([^\$\n]+?)\$(?!\$)', save_inline_math, processed_md)

    # Convert markdown to HTML
    body_html = markdown.markdown(
        processed_md,
        extensions=['extra', 'tables', 'codehilite', 'toc']
    )

    # Restore math placeholders
    for i, m in enumerate(math_blocks):
        body_html = body_html.replace(f"%%MATHBLOCK{i}%%", m)
    for i, m in enumerate(math_inlines):
        body_html = body_html.replace(f"%%MATHINLINE{i}%%", m)

    # HTML template with KaTeX and professional publication styling
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Eigenmode Orbital Dynamics</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {{
        delimiters: [
            {{left: '$$', right: '$$', display: true}},
            {{left: '$', right: '$', display: false}}
        ],
        throwOnError: false
    }});"></script>
<style>
@page {{
    size: A4 portrait;
    margin: 20mm 18mm 22mm 18mm;
    @bottom-center {{
        content: counter(page);
        font-family: "Liberation Serif", "Times New Roman", serif;
        font-size: 9pt;
        color: #666;
    }}
}}

body {{
    font-family: "Liberation Serif", "Times New Roman", Times, Georgia, serif;
    font-size: 10.5pt;
    line-height: 1.5;
    color: #1a1a1a;
    background-color: #ffffff;
    max-width: 100%;
    margin: 0;
    padding: 0;
}}

/* Typography */
h1 {{
    font-size: 20pt;
    font-weight: bold;
    text-align: center;
    margin-top: 0;
    margin-bottom: 8pt;
    line-height: 1.25;
    color: #0b1d3a;
}}

h2 {{
    font-size: 13.5pt;
    font-weight: bold;
    margin-top: 18pt;
    margin-bottom: 6pt;
    border-bottom: 1px solid #1a365d;
    padding-bottom: 2pt;
    color: #1a365d;
    page-break-after: avoid;
}}

h3 {{
    font-size: 11.5pt;
    font-weight: bold;
    margin-top: 13pt;
    margin-bottom: 4pt;
    color: #2b4c7e;
    page-break-after: avoid;
}}

h4 {{
    font-size: 10.5pt;
    font-weight: bold;
    font-style: italic;
    margin-top: 10pt;
    margin-bottom: 3pt;
    color: #333333;
    page-break-after: avoid;
}}

p {{
    margin-top: 0;
    margin-bottom: 7pt;
    text-align: justify;
    text-justify: inter-word;
}}

/* Lists */
ul, ol {{
    margin-top: 0;
    margin-bottom: 8pt;
    padding-left: 20pt;
}}

li {{
    margin-bottom: 3pt;
    text-align: justify;
}}

/* Blockquotes */
blockquote {{
    margin: 10pt 0;
    padding: 6pt 14pt;
    border-left: 3px solid #2b4c7e;
    background-color: #f7f9fc;
    font-style: italic;
    font-size: 10pt;
}}

/* Tables */
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10pt 0 14pt 0;
    font-size: 8.8pt;
    page-break-inside: avoid;
}}

th, td {{
    border: 1px solid #cbd5e1;
    padding: 4.5pt 6pt;
    text-align: left;
}}

th {{
    background-color: #f1f5f9;
    font-weight: bold;
    color: #0f172a;
    border-bottom: 1.5px solid #64748b;
}}

tr:nth-child(even) td {{
    background-color: #f8fafc;
}}

/* Code & Pre */
pre, code {{
    font-family: "Liberation Mono", "DejaVu Sans Mono", Courier, monospace;
}}

pre {{
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 3px;
    padding: 8pt 10pt;
    font-size: 8pt;
    line-height: 1.35;
    overflow-x: auto;
    margin: 8pt 0 10pt 0;
    page-break-inside: avoid;
}}

p code, li code {{
    background-color: #f1f5f9;
    padding: 1pt 3pt;
    border-radius: 2px;
    font-size: 9pt;
    border: 1px solid #e2e8f0;
}}

/* Flowchart box */
.flowchart-box {{
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 8pt 12pt;
    margin: 10pt 0;
    page-break-inside: avoid;
}}
.flowchart-title {{
    font-weight: bold;
    font-size: 9.5pt;
    color: #1a365d;
    margin-bottom: 4pt;
}}
.mermaid-code {{
    margin: 0;
    background: transparent;
    border: none;
    font-size: 8.5pt;
}}

/* KaTeX formatting */
.katex-display {{
    margin: 8pt 0 !important;
    overflow-x: hidden;
    overflow-y: hidden;
    page-break-inside: avoid;
}}
.katex {{
    font-size: 1.05em !important;
}}

/* Horizontal rule */
hr {{
    border: none;
    border-top: 1px solid #cbd5e1;
    margin: 14pt 0;
}}
</style>
</head>
<body>
{body_html}
</body>
</html>
"""

    print(f"Writing Stage 1 HTML: {HTML_STAGE1}")
    with open(HTML_STAGE1, "w", encoding="utf-8") as f:
        f.write(full_html)

    # Render KaTeX via Brave headless dump-dom
    print("Executing KaTeX DOM expansion via Brave Headless...")
    dump_cmd = f"flatpak run --command=sh com.brave.Browser -c 'brave --headless --no-sandbox --dump-dom {HTML_STAGE1}' > {HTML_STAGE2}"
    subprocess.run(dump_cmd, shell=True, check=True)

    # Print fully-rendered HTML to PDF via Brave Headless (write to /tmp first because of flatpak sandbox)
    tmp_pdf = "/tmp/eigenmode_orbital_dynamics.pdf"
    print(f"Generating PDF via Brave Headless: {tmp_pdf}")
    pdf_cmd = f"flatpak run com.brave.Browser --headless --no-sandbox --print-to-pdf={tmp_pdf} {HTML_STAGE2}"
    subprocess.run(pdf_cmd, shell=True, check=True)

    shutil.copyfile(tmp_pdf, PDF_OUT)

    if os.path.exists(PDF_OUT):
        sz = os.path.getsize(PDF_OUT)
        print(f"SUCCESS: PDF generated ({sz:,} bytes) at {PDF_OUT}")
    else:
        print("ERROR: PDF file not found!")
        sys.exit(1)

if __name__ == "__main__":
    build_pdf()
