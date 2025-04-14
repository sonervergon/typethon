#!/bin/bash

echo "🔧 Setting up Python environment for Typethon..."

# Check if pyenv is installed
if ! command -v pyenv &> /dev/null; then
    echo "📦 pyenv not found. Installing pyenv..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install pyenv
    else
        echo "⚠️ This script currently supports automatic pyenv installation only on macOS."
        echo "Please install pyenv manually for your system and run this script again."
        exit 1
    fi
    
    # Add pyenv init to shell configuration
    SHELL_CONFIG=""
    if [[ -f "$HOME/.zshrc" ]]; then
        SHELL_CONFIG="$HOME/.zshrc"
    elif [[ -f "$HOME/.bashrc" ]]; then
        SHELL_CONFIG="$HOME/.bashrc"
    elif [[ -f "$HOME/.bash_profile" ]]; then
        SHELL_CONFIG="$HOME/.bash_profile"
    else
        echo "⚠️ Could not find shell configuration file (.zshrc, .bashrc, or .bash_profile)."
        echo "Please add the following lines to your shell configuration file manually:"
        echo 'export PYENV_ROOT="$HOME/.pyenv"'
        echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"'
        echo 'eval "$(pyenv init -)"'
    fi
    
    if [[ -n "$SHELL_CONFIG" ]]; then
        echo "📝 Adding pyenv configuration to $SHELL_CONFIG"
        echo '' >> "$SHELL_CONFIG"
        echo '# pyenv configuration' >> "$SHELL_CONFIG"
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> "$SHELL_CONFIG"
        echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> "$SHELL_CONFIG"
        echo 'eval "$(pyenv init -)"' >> "$SHELL_CONFIG"
    fi
    
    # Initialize pyenv in current shell
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    
    echo "✅ pyenv has been installed and initialized in the current shell."
fi

# Check if Python 3.9.18 is installed via pyenv
if ! pyenv versions | grep -q "3.9.18"; then
    echo "📦 Python 3.9.18 not found. Installing Python 3.9.18 via pyenv..."
    pyenv install 3.9.18
    echo "✅ Python 3.9.18 has been installed."
fi

# Set Python 3.9.18 as the global version
if [[ "$(pyenv global)" != "3.9.18" ]]; then
    echo "🔄 Setting Python 3.9.18 as the global version..."
    pyenv global 3.9.18
    
    # Initialize pyenv in current shell to apply changes
    eval "$(pyenv init -)"
    echo "✅ pyenv has been initialized with Python 3.9.18 in the current shell."
fi

# Get the Python version to verify
PYTHON_VERSION=$(python --version 2>&1)
echo "🐍 Using Python: $PYTHON_VERSION"

# Check if we have the correct Python version
if [[ ! "$PYTHON_VERSION" =~ "3.9.18" ]]; then
    echo "⚠️ Warning: Python 3.9.18 is not being used in the current shell."
    echo "Let's try to fix this by reinitializing pyenv..."
    
    # Force reload pyenv in current shell
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    hash -r
    
    # Check Python version again
    PYTHON_VERSION=$(python --version 2>&1)
    echo "🐍 Now using Python: $PYTHON_VERSION"
    
    if [[ ! "$PYTHON_VERSION" =~ "3.9.18" ]]; then
        echo "⚠️ Warning: Still not using Python 3.9.18."
        echo "Please run the following commands manually or restart your terminal:"
        echo 'export PYENV_ROOT="$HOME/.pyenv"'
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"'
        echo 'eval "$(pyenv init -)"'
    fi
fi

echo "✅ Python environment setup complete!"
echo "Python 3.9.18 is now available for all Python applications in this project." 