#!/usr/bin/env bash
#
# Setup verification script for Purple Clay
# Checks prerequisites and provides helpful guidance

set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║                  Purple Clay - Setup Verification Script                    ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track if we have all requirements
ALL_GOOD=true

# Function to check command existence
check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $2 found: $(command -v $1)"
        return 0
    else
        echo -e "${RED}✗${NC} $2 not found"
        return 1
    fi
}

# Function to check Python version
check_python_version() {
    local python_cmd=$1
    if command -v "$python_cmd" &> /dev/null; then
        local version=$($python_cmd --version 2>&1 | awk '{print $2}')
        local major=$(echo $version | cut -d. -f1)
        local minor=$(echo $version | cut -d. -f2)
        
        if [ "$major" -ge 3 ] && [ "$minor" -ge 8 ]; then
            echo -e "${GREEN}✓${NC} $python_cmd version $version (>= 3.8 required)"
            return 0
        else
            echo -e "${RED}✗${NC} $python_cmd version $version (< 3.8, upgrade required)"
            return 1
        fi
    fi
    return 1
}

echo "Checking prerequisites..."
echo ""

# Check for Python
echo "1. Checking Python installation..."
PYTHON_FOUND=false

if check_python_version "python3"; then
    PYTHON_CMD="python3"
    PYTHON_FOUND=true
elif check_python_version "python"; then
    PYTHON_CMD="python"
    PYTHON_FOUND=true
else
    echo -e "${RED}✗${NC} Python 3.8+ not found"
    ALL_GOOD=false
fi
echo ""

# Check for pip
echo "2. Checking pip installation..."
PIP_FOUND=false

if [ "$PYTHON_FOUND" = true ]; then
    if check_command "pip3" "pip3"; then
        PIP_CMD="pip3"
        PIP_FOUND=true
    elif check_command "pip" "pip"; then
        PIP_CMD="pip"
        PIP_FOUND=true
    else
        echo -e "${YELLOW}⚠${NC}  pip not found, trying 'python -m pip'..."
        if $PYTHON_CMD -m pip --version &> /dev/null; then
            echo -e "${GREEN}✓${NC} pip available via 'python -m pip'"
            PIP_CMD="$PYTHON_CMD -m pip"
            PIP_FOUND=true
        else
            echo -e "${RED}✗${NC} pip not available"
            ALL_GOOD=false
        fi
    fi
else
    echo -e "${YELLOW}⚠${NC}  Skipping pip check (Python not found)"
    ALL_GOOD=false
fi
echo ""

# Check for git
echo "3. Checking git installation..."
if check_command "git" "git"; then
    GIT_FOUND=true
else
    echo -e "${YELLOW}⚠${NC}  git not found (optional, but needed to clone repository)"
    GIT_FOUND=false
fi
echo ""

# Summary
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

if [ "$ALL_GOOD" = true ]; then
    echo -e "${GREEN}✓ All prerequisites met!${NC}"
    echo ""
    echo "You can now install Purple Clay:"
    echo ""
    echo "  $PIP_CMD install -e ."
    echo ""
    echo "Then run the demo:"
    echo ""
    echo "  $PYTHON_CMD purple_clay_demo.py"
    echo ""
else
    echo -e "${RED}✗ Some prerequisites are missing${NC}"
    echo ""
    echo "Please install the missing components:"
    echo ""
    
    if [ "$PYTHON_FOUND" = false ]; then
        echo "📌 Python 3.8+:"
        echo ""
        echo "  macOS (with Homebrew):"
        echo "    brew install python3"
        echo ""
        echo "  macOS (official installer):"
        echo "    Download from https://www.python.org/downloads/macos/"
        echo ""
        echo "  Ubuntu/Debian:"
        echo "    sudo apt update && sudo apt install python3 python3-pip"
        echo ""
        echo "  Fedora/RHEL:"
        echo "    sudo dnf install python3 python3-pip"
        echo ""
        echo "  Windows:"
        echo "    Download from https://www.python.org/downloads/windows/"
        echo "    (Make sure to check 'Add Python to PATH' during installation)"
        echo ""
    fi
    
    if [ "$PIP_FOUND" = false ] && [ "$PYTHON_FOUND" = true ]; then
        echo "📌 pip:"
        echo ""
        echo "  macOS/Linux:"
        echo "    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py"
        echo "    $PYTHON_CMD get-pip.py"
        echo ""
        echo "  Ubuntu/Debian:"
        echo "    sudo apt install python3-pip"
        echo ""
    fi
    
    if [ "$GIT_FOUND" = false ]; then
        echo "📌 git (optional):"
        echo ""
        echo "  macOS:"
        echo "    brew install git"
        echo ""
        echo "  Ubuntu/Debian:"
        echo "    sudo apt install git"
        echo ""
        echo "  Or download from https://git-scm.com/downloads"
        echo ""
    fi
    
    echo "For detailed installation instructions, see INSTALLATION.md"
fi

echo "═══════════════════════════════════════════════════════════════════════════════"

exit 0
