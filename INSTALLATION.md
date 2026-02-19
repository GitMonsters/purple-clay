# Installation Guide

## Prerequisites

Purple Clay requires Python 3.8 or higher. Before installing Purple Clay, you need to have Python installed on your system.

## Check if Python is Installed

Run the following command in your terminal:

```bash
python --version
# or
python3 --version
```

If you see a version number (e.g., `Python 3.10.0`), Python is installed. If you get a "command not found" error, you need to install Python first.

## Installing Python

### macOS

**Option 1: Using Homebrew (Recommended)**

1. Install Homebrew if you don't have it:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install Python:
   ```bash
   brew install python3
   ```

3. Verify installation:
   ```bash
   python3 --version
   pip3 --version
   ```

**Option 2: Official Python Installer**

1. Download the latest Python 3 installer from [python.org](https://www.python.org/downloads/macos/)
2. Run the `.pkg` file and follow the installation wizard
3. Open a new terminal and verify:
   ```bash
   python3 --version
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Linux (Fedora/RHEL/CentOS)

```bash
sudo dnf install python3 python3-pip
```

### Windows

1. Download the latest Python 3 installer from [python.org](https://www.python.org/downloads/windows/)
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation
4. Verify installation in Command Prompt or PowerShell:
   ```bash
   python --version
   pip --version
   ```

## Installing Purple Clay

Once Python is installed, you can install Purple Clay:

### Quick Installation

```bash
# Clone the repository
git clone https://github.com/GitMonsters/purple-clay.git
cd purple-clay

# Install Purple Clay and its dependencies
pip3 install -e .
```

**Note**: Use `pip3` on macOS/Linux if `pip` is not found. On Windows, use `pip`.

### Alternative: Install dependencies only

If you just want to run the examples without installing the package:

```bash
# Clone the repository
git clone https://github.com/GitMonsters/purple-clay.git
cd purple-clay

# Install dependencies
pip3 install -r requirements.txt
```

## Verification

Test that everything is installed correctly:

```bash
# Run the interactive demo
python3 purple_clay_demo.py
```

Or test in Python:

```bash
python3 -c "from purple_clay import EmergentSpacetime, QuantumFlow; print('Purple Clay installed successfully!')"
```

## Troubleshooting

### "pip: command not found" or "pip3: command not found"

**Solution 1**: Use the Python module syntax:
```bash
python3 -m pip install -e .
```

**Solution 2**: Install pip manually:
```bash
# macOS/Linux
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Or on Ubuntu/Debian
sudo apt install python3-pip
```

### "python: command not found" on macOS/Linux

Try using `python3` instead:
```bash
python3 --version
python3 purple_clay_demo.py
```

You can create an alias in your shell configuration:
```bash
# Add to ~/.zshrc or ~/.bashrc
alias python=python3
alias pip=pip3
```

### Permission errors during installation

Use the `--user` flag to install in your user directory:
```bash
pip3 install --user -e .
```

Or create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

### "ModuleNotFoundError" when importing purple_clay

Make sure you're in the purple-clay directory and have installed the package:
```bash
cd purple-clay
pip3 install -e .
```

## Using Virtual Environments (Recommended)

Virtual environments keep your Purple Clay installation isolated:

```bash
# Create virtual environment
python3 -m venv purple_clay_env

# Activate it
# On macOS/Linux:
source purple_clay_env/bin/activate
# On Windows:
purple_clay_env\Scripts\activate

# Install Purple Clay
pip install -e .

# When done, deactivate
deactivate
```

## Next Steps

Once installed, see:
- [QUICKSTART.md](QUICKSTART.md) for your first simulation
- [README.md](README.md) for features and examples
- [SCIENTIFIC_BACKGROUND.md](SCIENTIFIC_BACKGROUND.md) for theory

## Getting Help

If you continue to have issues:
1. Check that Python 3.8+ is installed: `python3 --version`
2. Check that pip is available: `pip3 --version`
3. Try using a virtual environment
4. Open an issue on [GitHub](https://github.com/GitMonsters/purple-clay/issues) with your error message and system information
