# GroqCLI-Chatbot 🤖

> A professional, production-ready terminal-based AI chatbot powered by GroqCloud API

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Templates](#templates)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

**GroqCLI-Chatbot** is a powerful, feature-rich CLI chatbot that brings AI assistance directly to your terminal. Built with Python and powered by GroqCloud's ultra-fast inference engine, it provides a professional, production-ready interface for AI interactions.

### Why GroqCLI-Chatbot?

- ⚡ **Lightning-fast responses** - Powered by GroqCloud's optimized infrastructure
- 🎨 **Beautiful terminal UI** - Rich formatting with syntax highlighting
- 📋 **Smart templates** - Pre-built prompts for common tasks
- 💾 **Conversation management** - Save, load, and organize your chats
- 🚀 **Production-ready** - Clean code, comprehensive testing, error handling

---

## ✨ Features

### Core Features
- 🤖 **AI Chat** - Natural conversations with context memory
- 📋 **5 Essential Templates** - Pre-built prompts (code, debug, review, explain, summarize)
- 💾 **Save/Load** - Export conversations in JSON, Markdown, or Text
- 🎨 **Syntax Highlighting** - Beautiful code formatting with line numbers
- ⌨️ **Enhanced Input** - Multi-line support, command history
- 🔒 **Type-safe** - Full type hints throughout

### Advanced Features
- **Multiple Models** - Choose from 4 AI models
- **Auto-save** - Conversations saved automatically on exit
- **Structured Output** - Clean, easy-to-copy code blocks
- **Random Tips** - Helpful tips on startup
- **Professional UI** - Animated banner and clean interface

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- [UV package manager](https://docs.astral.sh/uv/) (recommended) or pip
- GroqCloud API key ([Get one free](https://console.groq.com/keys))

### Installation (3 steps)

```bash
# 1. Clone repository
git clone https://github.com/Krishnanivja12/GroqCli-Chatbot.git
cd GroqCli-chatbot

# 2. Install with UV (recommended)
uv sync

# 3. Configure
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Run

```bash
uv run groqcli
```

That's it! 🎉

---

## 📦 Installation

### Method 1: UV (Recommended - Fast!)

UV is a blazing-fast Python package manager.

```bash
# Install UV (if not already installed)
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/Krishnanivja12/GroqCli-Chatbot.git
cd GroqCli-chatbot
uv sync
```

### Method 2: pip (Traditional)

```bash
# Clone repository
git clone https://github.com/Krishnanivja12/GroqCli-Chatbot.git
cd GroqCli-chatbot

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -e .
```

---

## ⚙️ Configuration

### 1. Get GroqCloud API Key

1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up (free!)
3. Create a new API key
4. Copy the key (starts with `gsk_`)

### 2. Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit .env file
# Add your API key:
GROQ_API_KEY=gsk_your_actual_key_here
```

### 3. Configuration Options

Edit `.env` file:

```env
# GroqCloud API (Required)
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Chatbot Settings
CHATBOT_NAME=Atlas
CHATBOT_MAX_HISTORY=20
CHATBOT_TEMPERATURE=0.7
CHATBOT_MAX_TOKENS=1024
```

---

## 🎮 Usage

### Basic Usage

```bash
# Start chatbot
uv run groqcli

# Or with pip installation
groqcli
```

### With Options

```bash
# Use different model
uv run groqcli --model llama-3.1-8b-instant

# Adjust temperature (creativity)
uv run groqcli --temperature 0.9

# Disable syntax highlighting
uv run groqcli --no-highlight

# Show version
uv run groqcli --version
```

### Example Session

```
👤 You: What is Python?

🤖 Atlas: Python is a high-level programming language...
```

### Using Templates

```
👤 You: /template code
       Write a function to reverse a string

🤖 Atlas: [Provides structured code with explanation]
```

### Saving Conversations

```
👤 You: /save json
✅ Conversation saved to: conversations/conversation_20260209_123456.json
```

---

## 📋 Commands

### Basic Commands

| Command | Shortcut | Description |
|---------|----------|-------------|
| `/help` | `/h` | Show all commands |
| `/clear` | `/c` | Clear conversation history |
| `/quit` | `/q`, `/exit` | Exit chatbot |

### Templates

| Command | Description |
|---------|-------------|
| `/templates` | List all 5 templates |
| `/template <name>` | Use a template |
| `/t <name>` | Short form |

**Example:**
```bash
/template code
/t explain
```

### Conversation Management

| Command | Description |
|---------|-------------|
| `/save [format]` | Save conversation (json/md/txt) |
| `/load [file]` | Load a conversation |
| `/list` | List saved conversations |

**Example:**
```bash
/save json
/save md
/list
/load conversation_20260209_123456.json
```

### Information

| Command | Shortcut | Description |
|---------|----------|-------------|
| `/history` | - | Show conversation history |
| `/model` | `/m` | Show model info |
| `/stats` | `/s` | Show session statistics |

---

## 📝 Templates

GroqCLI-Chatbot includes 5 essential templates for common tasks:

### 1. Code Template
**Usage:** `/template code` or `/t code`

**Purpose:** Get help writing code

**Example:**
```
/template code
Write a Python function to calculate factorial
```

**Output:** Structured code with:
- Brief explanation
- Code in proper blocks with syntax highlighting
- Comments
- Usage example

### 2. Debug Template
**Usage:** `/template debug` or `/t debug`

**Purpose:** Debug code and fix errors

**Example:**
```
/template debug
My code gives IndexError: list index out of range
```

**Output:** Structured debugging help with:
- Issue identification
- Fixed code
- Explanation
- Prevention tips

### 3. Review Template
**Usage:** `/template review` or `/t review`

**Purpose:** Get code review and suggestions

**Example:**
```
/template review
[paste your code]
```

**Output:** Professional code review with:
- Strengths
- Issues found
- Suggestions
- Best practices

### 4. Explain Template
**Usage:** `/template explain` or `/t explain`

**Purpose:** Learn and understand concepts

**Example:**
```
/template explain
What is a decorator in Python?
```

**Output:** Clear explanation with:
- Definition
- Key points
- Example code
- Summary

### 5. Summarize Template
**Usage:** `/template summarize` or `/t summarize`

**Purpose:** Summarize long content

**Example:**
```
/template summarize
[paste long text or code]
```

**Output:** Concise summary with:
- Main points
- Key takeaways
- Brief overview

---

## 🤖 Available Models

### 1. llama-3.3-70b-versatile (Default)
- Best quality and reasoning
- Recommended for most tasks
- Balanced speed and performance

### 2. llama-3.1-8b-instant
- Fastest responses
- Good for quick questions
- Lower cost

### 3. mixtral-8x7b-32768
- Large context window (32K tokens)
- Good for long conversations
- Balanced performance

### 4. gemma2-9b-it
- Efficient
- Instruction-tuned
- Good for specific tasks

### CLI Options

```bash
# Use different model
uv run groqcli --model llama-3.1-8b-instant

# Adjust temperature (creativity)
uv run groqcli --temperature 0.9

# Disable syntax highlighting
uv run groqcli --no-highlight

# Show version
uv run groqcli --version
```

---

## 💡 Examples

### Example 1: Writing Code

```
👤 You: /template code
       Write a Python function to check if a number is prime

🤖 Atlas:

Here's a Python function to check if a number is prime:

📝 PYTHON Code
──────────────────────────────────────────────────────────────────
  1 │ def is_prime(n):
  2 │     """Check if a number is prime."""
  3 │     if n < 2:
  4 │         return False
  5 │     for i in range(2, int(n ** 0.5) + 1):
  6 │         if n % i == 0:
  7 │             return False
  8 │     return True
  9 │ 
 10 │ # Usage example
 11 │ print(is_prime(17))  # True
 12 │ print(is_prime(4))   # False
──────────────────────────────────────────────────────────────────
💡 Tip: Select with mouse to copy

The function checks divisibility up to the square root of n for efficiency.
```

### Example 2: Debugging

```
👤 You: /template debug
       My code: list[10] gives IndexError

🤖 Atlas:

Issue Identified:
The error occurs when trying to access an index that doesn't exist.

Fixed Code:
──────────────────────────────────────────────────────────────────
  1 │ # Check list length first
  2 │ if len(list) > 10:
  3 │     value = list[10]
  4 │ else:
  5 │     print("Index out of range")
──────────────────────────────────────────────────────────────────

Prevention: Always check list length before accessing indices.
```

### Example 3: Learning

```
👤 You: /template explain
       What is a decorator in Python?

🤖 Atlas:

Definition:
A decorator is a function that modifies another function's behavior.

Key Points:
• Wraps another function
• Adds functionality without changing original code
• Uses @ syntax

Example:
──────────────────────────────────────────────────────────────────
  1 │ def my_decorator(func):
  2 │     def wrapper():
  3 │         print("Before")
  4 │         func()
  5 │         print("After")
  6 │     return wrapper
  7 │ 
  8 │ @my_decorator
  9 │ def say_hello():
 10 │     print("Hello!")
──────────────────────────────────────────────────────────────────

Summary: Decorators enhance functions elegantly.
```

---

## 🔧 Troubleshooting

### Issue 1: "Module not found"

**Solution:**
```bash
uv sync
# or
pip install -e .
```

### Issue 2: "GROQ_API_KEY is required"

**Solution:**
1. Check `.env` file exists
2. Verify `GROQ_API_KEY=gsk_...` is set
3. Make sure key starts with `gsk_`
4. No spaces around `=`

### Issue 3: "Cannot connect to GroqCloud"

**Solution:**
- Check internet connection
- Verify API key is valid
- Try different model: `uv run groqcli --model llama-3.1-8b-instant`

### Issue 4: Slow Startup

**Solution:**
- Check internet connection
- First run is slower (model loading)
- Subsequent runs are faster

### Issue 5: Code Not Copying

**Solution:**
- Use mouse to select code
- Code blocks have line numbers for easy selection
- Look for "💡 Tip: Select with mouse to copy"

---

## 📊 Project Structure

```
GroqCli-chatbot/
├── src/growcli/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Entry point & main loop
│   ├── chat_engine.py           # Groq API integration
│   ├── config.py                # Configuration management
│   ├── conversation_manager.py  # Save/load conversations
│   ├── templates.py             # Template system (5 templates)
│   ├── input_handler.py         # Enhanced input
│   ├── syntax_highlighter.py    # Code highlighting
│   ├── banner.py                # Animated banner
│   ├── cost_tracker.py          # Cost tracking
│   ├── model_selector.py        # Model selection
│   ├── prompts.py               # System prompts
│   └── utils.py                 # Utility functions
├── tests/                       # Test suite
├── conversations/               # Saved conversations
├── .env                         # Configuration (create from .env.example)
├── .env.example                 # Example configuration
├── pyproject.toml               # Dependencies
└── README.md                    # This file
```

---

## 🎓 Advanced Usage

### Multi-line Input

End line with `\` to continue:

```
👤 You: What is Python?\
       Tell me about its features\
       And give examples
```

### Conversation Management

```bash
# Save in different formats
/save json    # Structured data
/save md      # Readable markdown
/save txt     # Plain text

# List saved conversations
/list

# Load a conversation
/load conversation_20260209_123456.json
```

### Session Statistics

```bash
/stats

📊 Conversation Summary:
   Total messages: 10
   Total tokens: 5,234
   Model: llama-3.3-70b-versatile
```

---

## 🚀 Features Roadmap

### Implemented ✅
- [x] AI Chat with context memory
- [x] 5 essential templates
- [x] Save/Load conversations
- [x] Syntax highlighting
- [x] Cost tracking module
- [x] Model selector module
- [x] Animated banner
- [x] Clean, professional UI

### Planned 🔜
- [ ] Keyboard shortcuts (Ctrl+L, H, S, T, R, E)
- [ ] Streaming responses (token-by-token)
- [ ] File attachments
- [ ] Code execution
- [ ] Web search integration
- [ ] Conversation search
- [ ] Export to PDF/HTML

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- **GroqCloud** - Ultra-fast AI inference
- **Rich** - Beautiful terminal UI
- **UV** - Fast Python package manager

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/groqcli-chatbot/issues)
- **Documentation**: This README
- **GroqCloud**: [https://console.groq.com](https://console.groq.com)

---

## 🎉 Quick Reference

### Starting Chatbot

```bash
# Start
uv run groqcli
```

### Essential Commands
```bash
/help          # Show all commands
/templates     # List templates
/template code # Use code template
/save json     # Save conversation
/quit          # Exit
```

### Essential Templates
```bash
/t code        # Write code
/t debug       # Fix errors
/t review      # Review code
/t explain     # Learn concepts
/t summarize   # Summarize content
```

### Quick Start
```bash
# Install
uv sync

# Configure
cp .env.example .env
# Add GROQ_API_KEY

# Run
uv run groqcli
```

---

**Made with ❤️ using GroqCloud and Python**

**Version:** 0.1.0 | **Status:** Production Ready ✅

---

## 📸 Screenshots

### Startup
```
╔═══════════════════════════════════════════════════════════════════╗
║              ╔═══════════════════════════════════╗                ║
║              ║   CHATBOT  •  v0.1.0  •  2026     ║                ║
║              ╚═══════════════════════════════════╝                ║
╚═══════════════════════════════════════════════════════════════════╝

⚡ Lightning-fast AI responses
🎯 Production-ready chatbot
🎨 Beautiful terminal interface
```

### Chat Interface
```
👤 You: What is Python?

🤖 Atlas: Python is a high-level programming language...
──────────────────────────────────────────────────────────────────
💡 Tokens: 150 | Latency: 1.2s
```

### Code Output
```
📝 PYTHON Code
──────────────────────────────────────────────────────────────────
  1 │ def factorial(n):
  2 │     if n <= 1:
  3 │         return 1
  4 │     return n * factorial(n-1)
──────────────────────────────────────────────────────────────────
💡 Tip: Select with mouse to copy
```

---

**🚀 Start chatting now: `uv run groqcli`**
