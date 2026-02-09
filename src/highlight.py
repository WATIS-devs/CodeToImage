#!/usr/bin/env python3
"""
Script for converting Python files to HTML with Monokai syntax highlighting.
Usage: python highlight.py <path_to_file.py>
"""

import sys
import os
from pathlib import Path
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name

# Monokai color scheme
MONOKAI_CSS = """
/* Main style */
body {
    font-family: 'Fira Code', 'Consolas', 'Monaco', 'Courier New', monospace;
    background-color: #272822;
    color: #f8f8f2;
    margin: 0;
    padding: 20px;
    line-height: 1.6;
}

/* Code container */
.code-container {
    background-color: #272822;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    overflow: hidden;
    max-width: 100%;
    margin: 0 auto;
}

/* File header */
.file-header {
    background-color: #1e1f1c;
    padding: 10px 15px;
    border-bottom: 1px solid #3e3d32;
    color: #75715e;
    font-size: 14px;
    font-weight: bold;
}

/* Scroll */
.code-wrapper {
    overflow-x: auto;
    padding: 20px;
}

/* Table with line numbers */
.highlight table {
    border-spacing: 0;
    border-collapse: separate;
    width: 100%;
}

.highlight pre {
    margin: 0;
    padding: 0;
    background: none;
    font-size: 14px;
}

/* Line numbers */
.highlight td.linenos {
    padding-right: 15px;
    color: #90908a;
    text-align: right;
    user-select: none;
    border-right: 1px solid #3e3d32;
}

.highlight td.code {
    padding-left: 15px;
}

/* Code highlighting styles (Monokai) */
.highlight .c { color: #75715e } /* Comment */
.highlight .err { color: #960050; background-color: #1e0010 } /* Error */
.highlight .k { color: #66d9ef } /* Keyword */
.highlight .l { color: #ae81ff } /* Literal */
.highlight .n { color: #f8f8f2 } /* Name */
.highlight .o { color: #f92672 } /* Operator */
.highlight .p { color: #f8f8f2 } /* Punctuation */
.highlight .cm { color: #75715e } /* Comment.Multiline */
.highlight .cp { color: #75715e } /* Comment.Preproc */
.highlight .c1 { color: #75715e } /* Comment.Single */
.highlight .cs { color: #75715e } /* Comment.Special */
.highlight .ge { font-style: italic } /* Generic.Emph */
.highlight .gs { font-weight: bold } /* Generic.Strong */
.highlight .kc { color: #66d9ef } /* Keyword.Constant */
.highlight .kd { color: #66d9ef } /* Keyword.Declaration */
.highlight .kn { color: #f92672 } /* Keyword.Namespace */
.highlight .kp { color: #66d9ef } /* Keyword.Pseudo */
.highlight .kr { color: #66d9ef } /* Keyword.Reserved */
.highlight .kt { color: #66d9ef } /* Keyword.Type */
.highlight .ld { color: #e6db74 } /* Literal.Date */
.highlight .m { color: #ae81ff } /* Literal.Number */
.highlight .s { color: #e6db74 } /* Literal.String */
.highlight .na { color: #a6e22e } /* Name.Attribute */
.highlight .nb { color: #f8f8f2 } /* Name.Builtin */
.highlight .nc { color: #a6e22e } /* Name.Class */
.highlight .no { color: #66d9ef } /* Name.Constant */
.highlight .nd { color: #a6e22e } /* Name.Decorator */
.highlight .ni { color: #f8f8f2 } /* Name.Entity */
.highlight .ne { color: #a6e22e } /* Name.Exception */
.highlight .nf { color: #a6e22e } /* Name.Function */
.highlight .nl { color: #f8f8f2 } /* Name.Label */
.highlight .nn { color: #f8f8f2 } /* Name.Namespace */
.highlight .nx { color: #a6e22e } /* Name.Other */
.highlight .py { color: #f8f8f2 } /* Name.Property */
.highlight .nt { color: #f92672 } /* Name.Tag */
.highlight .nv { color: #f8f8f2 } /* Name.Variable */
.highlight .ow { color: #f92672 } /* Operator.Word */
.highlight .w { color: #f8f8f2 } /* Text.Whitespace */
.highlight .mf { color: #ae81ff } /* Literal.Number.Float */
.highlight .mh { color: #ae81ff } /* Literal.Number.Hex */
.highlight .mi { color: #ae81ff } /* Literal.Number.Integer */
.highlight .mo { color: #ae81ff } /* Literal.Number.Oct */
.highlight .sb { color: #e6db74 } /* Literal.String.Backtick */
.highlight .sc { color: #e6db74 } /* Literal.String.Char */
.highlight .sd { color: #e6db74 } /* Literal.String.Doc */
.highlight .s2 { color: #e6db74 } /* Literal.String.Double */
.highlight .se { color: #ae81ff } /* Literal.String.Escape */
.highlight .sh { color: #e6db74 } /* Literal.String.Heredoc */
.highlight .si { color: #e6db74 } /* Literal.String.Interpol */
.highlight .sx { color: #e6db74 } /* Literal.String.Other */
.highlight .sr { color: #e6db74 } /* Literal.String.Regex */
.highlight .s1 { color: #e6db74 } /* Literal.String.Single */
.highlight .ss { color: #e6db74 } /* Literal.String.Symbol */
.highlight .bp { color: #f8f8f2 } /* Name.Builtin.Pseudo */
.highlight .vc { color: #f8f8f2 } /* Name.Variable.Class */
.highlight .vg { color: #f8f8f2 } /* Name.Variable.Global */
.highlight .vi { color: #f8f8f2 } /* Name.Variable.Instance */
.highlight .il { color: #ae81ff } /* Literal.Number.Integer.Long */
"""


def generate_html(input_file: str, output_file: str = None) -> str:
    """
    Generates HTML with syntax highlighting from a Python file.
    
    Args:
        input_file: Path to input .py file
        output_file: Path to output .html file (optional)
    
    Returns:
        Path to the created HTML file
    """
    # Check if file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"File '{input_file}' not found")
    
    # Read file contents
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Generate HTML with highlighting
    lexer = PythonLexer()
    formatter = HtmlFormatter(
        style='monokai',
        linenos=True,
        cssclass='highlight',
        hl_lines=[]
    )
    
    highlighted_code = highlight(code, lexer, formatter)
    
    # Create complete HTML document
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{os.path.basename(input_file)} - Python Code</title>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <style>
        {MONOKAI_CSS}
    </style>
</head>
<body>
    <div class="code-container">
        <div class="file-header">{os.path.basename(input_file)}</div>
        <div class="code-wrapper">
            {highlighted_code}
        </div>
    </div>
</body>
</html>"""
    
    # Determine output filename
    if output_file is None:
        output_file = Path(input_file).with_suffix('.html')
    
    # Save HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return str(output_file)


def main():
    """Main script function."""
    if len(sys.argv) < 2:
        print("Usage: python highlight.py <path_to_file.py>")
        print("Example: python highlight.py main.py")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        output_file = generate_html(input_file)
        print(f"[+] HTML file successfully created: {output_file}")
        print(f"[+] Open it in a browser to view")
    except FileNotFoundError as e:
        print(f"[-] Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[-] An error occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()