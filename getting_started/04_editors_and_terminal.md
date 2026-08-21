# Choosing Where to Write and Run Your Labs

To complete the labs, you only need two basic tools: a way to view and edit files in this repository, and a terminal to run Python commands like `python script_name.py`.

Any of the development environments listed below will work smoothly. Pick whichever tool you feel most comfortable with!

> **Important**: Always open the **repository root folder** (the main folder containing `AGENTS.md`). If you open an individual chapter subfolder instead, your editor or AI assistant might miss important course configuration rules.

---

## 1. Cursor

Cursor is an AI-powered code editor built on VS Code.
1. Download and install [Cursor](https://cursor.com).
2. Go to **File → Open Folder...** and select the root folder of this repository.
3. Open the chat panel and ask Cursor to review the chapter module with you and help write the lab script (e.g., *"Let's read education/00_atoms/00_script_provider_weights.md together, then write lab1_script_posts_json.py based on the brief."*).
4. Cursor automatically detects and follows the guidelines in `AGENTS.md`.

---

## 2. VS Code

Visual Studio Code is a popular, lightweight code editor.
1. Download and install [VS Code](https://code.visualstudio.com).
2. Go to **File → Open Folder...** and select the root folder of this repository.
3. Open a built-in terminal window by selecting **Terminal → New Terminal** from the top menu.
4. Run your Python lab scripts directly from that terminal.
5. You can write the Python code yourself or pair-program using extensions like GitHub Copilot.

---

## 3. Claude Code

Claude Code is a command-line interface for pairing with Anthropic's Claude.
1. Install Claude Code by following Anthropic's official setup documentation.
2. In your terminal, navigate (`cd`) to this repository's root folder.
3. Start `claude` and ask it to begin at Chapter 00 while following the instructions in `AGENTS.md`.
4. Keep the scope focused: allow it to implement only the current lab brief.

---

## 4. Antigravity

Antigravity is Google's agentic coding assistant.
1. Open this repository's root folder in Antigravity. It will automatically load `AGENTS.md` and repository guidelines.
2. Start in `education/00_atoms/`.
3. Work through each lab brief, creating the corresponding `.py` file and running it in the integrated terminal.

---

## 5. Standard Terminal & Text Editor

If you prefer a classic, distraction-free environment, you can complete the entire course using any plain text editor (like Notepad, TextEdit, or Sublime) and a command-line terminal:

```powershell
cd path\to\script-to-agent-labs
python --version
```

Make sure your system has Python 3.10 or newer installed. If Python is not recognized, install it from [python.org](https://www.python.org/downloads/) (checking **Add python.exe to PATH**), and restart your terminal.

---

## How to Prompt AI Assistants for Help

When collaborating with an AI coding assistant, keep your instructions focused and direct:

> *"Please open `education/00_atoms/lab1_script_posts_json.md`. Help me write that specific script. Keep the code focused strictly on the brief without adding extra libraries or unnecessary features."*

---

**Next Steps**: [Run your first lab script](./05_first_lab.md).
