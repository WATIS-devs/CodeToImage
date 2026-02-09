# Python Code Highlighter

![Python Code Highlighter](icon.ico)

A beautiful Python code to HTML converter with Monokai syntax highlighting. Convert your Python files into syntax-highlighted HTML documents instantly.

## Features

- 🎨 **Monokai Theme**: Beautiful dark theme with vibrant colors
- 🖱️ **Drag & Drop**: Simply drag and drop .py files into the window
- 🌐 **GUI Application**: User-friendly interface built with PyQt6
- 💻 **CLI Support**: Command-line interface for automation
- 📁 **One File**: Single .exe file - no installation required
- 🚀 **Fast**: Instant conversion of Python files to HTML
- 🔢 **Line Numbers**: Automatic line numbering in output
- 🌍 **Cross-platform**: Works on Windows, macOS, and Linux

## Screenshots

The application features a clean, dark interface with the iconic Monokai color scheme:

- Drag & drop zone for quick file conversion
- Automatic browser opening of generated HTML
- Status indicators for user feedback
- GitHub author attribution link

## Installation

### Option 1: Standalone Executable (Recommended for Windows)

1. Download `Python Code Highlighter.exe` from the [Releases](https://github.com/WATIS-devs/codetoimage1/releases) section
2. Double-click to run - no installation needed!

### Option 2: From Source

1. Clone the repository:
```bash
git clone https://github.com/WATIS-devs/codetoimage1.git
cd codetoimage1
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/gui_highlighter.py
```

## Usage

### GUI Application

1. Launch `Python Code Highlighter.exe` (Windows) or run `python src/gui_highlighter.py`
2. Drag and drop any `.py` file into the window, OR
3. Click "Select File" and choose your Python file
4. HTML file will be created automatically
5. Choose to open it in your browser

### Command Line Interface

```bash
# Convert a single file
python src/highlight.py your_script.py

# The HTML file will be created in the same directory
```

## Output

The generated HTML file includes:

- ✅ Full syntax highlighting (Monokai theme)
- ✅ Line numbers
- ✅ Responsive design
- ✅ File header with filename
- ✅ Fira Code font (Google Fonts)
- ✅ Copy-paste ready code
- ✅ Beautiful dark theme

## Requirements

For running from source:

- Python 3.7 or higher
- PyQt6
- Pygments

See `requirements.txt` for complete list.

## Building the Executable

To create a standalone .exe file:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Build executable:
```bash
pyinstaller --onefile --windowed --icon=icon.ico --name="Python Code Highlighter" src/gui_highlighter.py
```

The executable will be created in the `dist/` directory.

## File Structure

```
codetoimage1/
├── src/                       # Source code
│   ├── highlight.py            # CLI version
│   ├── gui_highlighter.py      # GUI version
├── release/                   # Pre-built executables
│   └── Python Code Highlighter.exe
├── dist/                      # Build output
├── build/                     # Build artifacts
├── README.md                  # This file
├── LICENSE                    # MIT License
├── requirements.txt           # Python dependencies
└── .gitignore                # Git ignore rules
```

## Color Scheme (Monokai)

The application uses the classic Monokai color palette:

| Element | Color | Hex |
|----------|--------|------|
| Background | Dark Gray | `#272822` |
| Keywords | Cyan | `#66d9ef` |
| Strings | Yellow | `#e6db74` |
| Comments | Gray | `#75715e` |
| Functions | Green | `#a6e22e` |
| Numbers | Purple | `#ae81ff` |
| Operators | Pink | `#f92672` |

## Author

**Created by [WATIS-devs](https://github.com/WATIS-devs)**

- GitHub: [@WATIS-devs](https://github.com/WATIS-devs)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [Pygments](https://pygments.org/) - Python syntax highlighter library
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework
- Monokai theme by Wimer Hazenberg

## Version History

### Version 1.0.0 (2026-02-09)
- Initial release
- GUI with drag & drop support
- CLI interface
- Monokai syntax highlighting
- Standalone Windows executable
- English interface

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ by WATIS-devs**