#!/usr/bin/env python3
"""
GUI application for converting Python files to HTML with Monokai syntax highlighting.
Use drag-and-drop to drop .py files into the window.
"""

import sys
import os
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPalette, QColor, QFont
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

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
.highlight .c { color: #75715e }
.highlight .err { color: #960050; background-color: #1e0010 }
.highlight .k { color: #66d9ef }
.highlight .l { color: #ae81ff }
.highlight .n { color: #f8f8f2 }
.highlight .o { color: #f92672 }
.highlight .p { color: #f8f8f2 }
.highlight .cm { color: #75715e }
.highlight .cp { color: #75715e }
.highlight .c1 { color: #75715e }
.highlight .cs { color: #75715e }
.highlight .ge { font-style: italic }
.highlight .gs { font-weight: bold }
.highlight .kc { color: #66d9ef }
.highlight .kd { color: #66d9ef }
.highlight .kn { color: #f92672 }
.highlight .kp { color: #66d9ef }
.highlight .kr { color: #66d9ef }
.highlight .kt { color: #66d9ef }
.highlight .ld { color: #e6db74 }
.highlight .m { color: #ae81ff }
.highlight .s { color: #e6db74 }
.highlight .na { color: #a6e22e }
.highlight .nb { color: #f8f8f2 }
.highlight .nc { color: #a6e22e }
.highlight .no { color: #66d9ef }
.highlight .nd { color: #a6e22e }
.highlight .ni { color: #f8f8f2 }
.highlight .ne { color: #a6e22e }
.highlight .nf { color: #a6e22e }
.highlight .nl { color: #f8f8f2 }
.highlight .nn { color: #f8f8f2 }
.highlight .nx { color: #a6e22e }
.highlight .py { color: #f8f8f2 }
.highlight .nt { color: #f92672 }
.highlight .nv { color: #f8f8f2 }
.highlight .ow { color: #f92672 }
.highlight .w { color: #f8f8f2 }
.highlight .mf { color: #ae81ff }
.highlight .mh { color: #ae81ff }
.highlight .mi { color: #ae81ff }
.highlight .mo { color: #ae81ff }
.highlight .sb { color: #e6db74 }
.highlight .sc { color: #e6db74 }
.highlight .sd { color: #e6db74 }
.highlight .s2 { color: #e6db74 }
.highlight .se { color: #ae81ff }
.highlight .sh { color: #e6db74 }
.highlight .si { color: #e6db74 }
.highlight .sx { color: #e6db74 }
.highlight .sr { color: #e6db74 }
.highlight .s1 { color: #e6db74 }
.highlight .ss { color: #e6db74 }
.highlight .bp { color: #f8f8f2 }
.highlight .vc { color: #f8f8f2 }
.highlight .vg { color: #f8f8f2 }
.highlight .vi { color: #f8f8f2 }
.highlight .il { color: #ae81ff }
"""


class DropZoneWidget(QWidget):
    """Widget for drag and drop files."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumSize(400, 300)
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        """Initialize interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Icon and text
        self.icon_label = QLabel("📄")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 64px;")
        
        self.title_label = QLabel("Drag & drop .py file here")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #f8f8f2;
        """)
        
        self.subtitle_label = QLabel("or click button to select file")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setStyleSheet("""
            font-size: 14px;
            color: #75715e;
        """)
        
        # File selection button
        self.select_button = QPushButton("Select File")
        self.select_button.setFixedWidth(150)
        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: #66d9ef;
                color: #272822;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7adff5;
            }
            QPushButton:pressed {
                background-color: #4cc9e9;
            }
        """)
        self.select_button.clicked.connect(self.parent_window.select_file)
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.select_button, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)
        self.update_style()
    
    def update_style(self):
        """Update widget style."""
        self.setStyleSheet("""
            DropZoneWidget {
                background-color: #272822;
                border: 3px dashed #3e3d32;
                border-radius: 10px;
            }
            DropZoneWidget:hover {
                border-color: #66d9ef;
            }
        """)
    
    def set_drag_over_style(self):
        """Style when dragging."""
        self.setStyleSheet("""
            DropZoneWidget {
                background-color: #2a2b26;
                border: 3px dashed #66d9ef;
                border-radius: 10px;
            }
        """)
        self.title_label.setText("Drop file here")
        self.title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #66d9ef;
        """)
    
    def reset_style(self):
        """Return to normal style."""
        self.update_style()
        self.title_label.setText("Drag & drop .py file here")
        self.title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #f8f8f2;
        """)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle file drag enter event."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.set_drag_over_style()
    
    def dragLeaveEvent(self, event):
        """Handle file drag leave event."""
        self.reset_style()
    
    def dropEvent(self, event: QDropEvent):
        """Handle file drop event."""
        self.reset_style()
        
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.endswith('.py'):
                self.parent_window.process_file(file_path)
            else:
                QMessageBox.warning(
                    self, 
                    "Error", 
                    "Please select a file with .py extension"
                )


class HighlighterWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize interface."""
        self.setWindowTitle("Python Code Highlighter - Monokai")
        self.setMinimumSize(600, 500)
        
        # Apply Monokai theme
        self.apply_monokai_theme()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header
        header_label = QLabel("Python Code Highlighter")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #a6e22e;
        """)
        
        # Drag and drop zone
        self.drop_zone = DropZoneWidget(self)
        
        # Status
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 12px;
            color: #75715e;
        """)
        
        # GitHub link
        github_link = QLabel('Created by <a href="https://github.com/WATIS-devs" style="color: #a6e22e; text-decoration: none;">WATIS-devs</a>')
        github_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        github_link.setOpenExternalLinks(True)
        github_link.setTextFormat(Qt.TextFormat.RichText)
        github_link.setStyleSheet("""
            font-size: 11px;
            color: #a6e22e;
        """)
        
        main_layout.addWidget(header_label)
        main_layout.addWidget(self.drop_zone)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(github_link)
        
        central_widget.setLayout(main_layout)
    
    def apply_monokai_theme(self):
        """Apply Monokai theme to window."""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0x27, 0x28, 0x22))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0xf8, 0xf8, 0xf2))
        palette.setColor(QPalette.ColorRole.Base, QColor(0x27, 0x28, 0x22))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(0x27, 0x28, 0x22))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(0xf8, 0xf8, 0xf2))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0xf8, 0xf8, 0xf2))
        palette.setColor(QPalette.ColorRole.Text, QColor(0xf8, 0xf8, 0xf2))
        palette.setColor(QPalette.ColorRole.Button, QColor(0x27, 0x28, 0x22))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(0xf8, 0xf8, 0xf2))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(0xff, 0x00, 0x00))
        palette.setColor(QPalette.ColorRole.Link, QColor(0xa6, 0xe2, 0x2e))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0x66, 0xd9, 0xef))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0x27, 0x28, 0x22))
        QApplication.setPalette(palette)
    
    def select_file(self):
        """Open file selection dialog."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Python file",
            "",
            "Python Files (*.py)"
        )
        if file_path:
            self.process_file(file_path)
    
    def process_file(self, file_path: str):
        """Process selected file."""
        try:
            self.status_label.setText(f"Processing file: {os.path.basename(file_path)}")
            QApplication.processEvents()
            
            output_file = self.generate_html(file_path)
            
            self.status_label.setText(f"Successfully created: {os.path.basename(output_file)}")
            
            # Success message
            reply = QMessageBox.question(
                self,
                "Success!",
                f"HTML file successfully created:\n{output_file}\n\nOpen it in browser?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.open_in_browser(output_file)
        
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "File not found")
            self.status_label.setText("Error: file not found")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")
            self.status_label.setText("Error during processing")
    
    def generate_html(self, input_file: str) -> str:
        """Generate HTML with syntax highlighting."""
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
        output_file = Path(input_file).with_suffix('.html')
        
        # Save HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        return str(output_file)
    
    def open_in_browser(self, file_path: str):
        """Open file in default browser."""
        if sys.platform == 'win32':
            os.startfile(file_path)
        elif sys.platform == 'darwin':
            subprocess.run(['open', file_path])
        else:
            subprocess.run(['xdg-open', file_path])


def main():
    """Main application function."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = HighlighterWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()