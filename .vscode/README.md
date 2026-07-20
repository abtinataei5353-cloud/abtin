# VS Code Extensions for Abtin Development

## Recommended Extensions

```json
{
    "recommendations": [
        "ms-python.python",              // Python support
        "ms-python.vscode-pylance",      // Type checking and IntelliSense
        "ms-python.debugpy",             // Debugger
        "ms-python.black-formatter",     // Code formatter
        "charliermarsh.ruff",            // Fast Python linter
        "GitHub.copilot",                // AI code assistance
        "ms-vscode.makefile-tools",      // Makefile support
        "ms-vscode-remote.remote-containers", // Docker support
    ]
}
```

## Quick Start

### 1. Open the Project in VS Code
```bash
cd path/to/abtin
code .
```

### 2. Install Dependencies
```bash
# Terminal in VS Code (Ctrl+`)
make install
make install-dev
```

### 3. Run the Application

**Option A: Press F5**
- VS Code will use the configuration in `.vscode/launch.json`
- Select "Python: Abtin" if prompted

**Option B: Use the Run Button**
- Click the ▶️ (Run) button in the top-right corner

**Option C: Use Terminal**
```bash
python run.py
```

**Option D: Use Makefile**
```bash
make run
```

### 4. Debugging

**Set Breakpoints**
- Click on the line number in the editor to set breakpoints
- Breakpoints will appear as red dots

**Debug Controls**
- Use the Debug toolbar (play, pause, step, etc.)
- Or use keyboard shortcuts:
  - `F10` - Step over
  - `F11` - Step into
  - `Shift+F11` - Step out
  - `F5` - Continue

**Debug Console**
- View at the bottom of the screen
- Evaluate expressions and view variables

## Development Workflow

### Running Tests
```bash
# Terminal
make test          # Run all tests
make test-cov      # Run tests with coverage
```

### Code Quality
```bash
make lint          # Check code quality
make format        # Auto-format code
```

### File Structure
```
abtin/
├── run.py                 # ⭐ Entry point - Run this!
├── src/
│   ├── main.py            # Application launcher
│   ├── ui/
│   │   └── main_window.py # Main UI window
│   ├── analysis/          # Analysis algorithms
│   ├── data/              # Data handling
│   ├── config/            # Configuration
│   └── utils/             # Utilities
├── tests/                 # Test files
├── .vscode/
│   ├── launch.json        # Debug configuration
│   └── settings.json      # Editor settings
└── requirements.txt       # Dependencies
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'src'"
- Make sure you're in the project root directory
- The `PYTHONPATH` is set in `.vscode/launch.json`
- Try: `export PYTHONPATH="${PWD}"` in terminal

### PyQt6 not found
```bash
pip install PyQt6
```

### Port already in use
- Change the port in `src/config/settings.py`
- Or kill the process: `lsof -ti :5000 | xargs kill -9`

### Performance Issues
- Check: Activity Monitor / Task Manager for resource usage
- Disable extensions in `.vscode/extensions` if too slow

## Tips

- **IntelliSense**: Type `Ctrl+Space` for code completion
- **Go to Definition**: `F12` or `Ctrl+Click`
- **Find References**: `Shift+F12`
- **Format Document**: `Shift+Alt+F`
- **Terminal**: `Ctrl+`` to toggle integrated terminal

## Next Steps

1. Install the recommended extensions
2. Run `make install-dev` to set up the environment
3. Press `F5` to launch the application
4. Start developing! 🚀
