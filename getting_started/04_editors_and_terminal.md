# Where you write and run the labs

You need two things: a folder that holds this repo, and a way to run `python some_file.py`.

Any of the tools below work. You do not need all of them.

Open the **repo root** (the folder that contains `AGENTS.md`). If you open a chapter folder instead, the AI IDE may miss the course rules.

## Cursor

1. Install [Cursor](https://cursor.com).
2. **File → Open Folder** and pick this repo.
3. Open the chat. Ask it to read `education/00_atoms/00_script_provider_weights.md` with you, then write `lab1_script_posts_json.py` from the brief.
4. Cursor reads `AGENTS.md` on its own. You do not paste those rules.

This is the path the course was written for.

## VS Code

1. Install [VS Code](https://code.visualstudio.com).
2. **File → Open Folder** and pick this repo.
3. Open a terminal in VS Code (**Terminal → New Terminal**).
4. Run the scripts from that terminal (see [first lab](./05_first_lab.md)).

You can write the Python yourself, or use GitHub Copilot / another chat add-on. The markdown is still the assignment.

## Claude Code

1. Install Claude Code from Anthropic's docs.
2. In a terminal, `cd` into this repo root.
3. Run `claude`. Ask it to start at chapter 00 and follow `AGENTS.md`.

Same rule: the lab brief is the whole assignment. Do not let it skip to a later chapter.

## Antigravity

1. Open this repo root in Antigravity so it reads `AGENTS.md`.
2. Start at `education/00_atoms/`.
3. Write the `.py` next to the brief. Run it in the built-in terminal.

## Terminal only

You can do the whole course with a text editor and a terminal.

```powershell
cd path\to\AgenticAI-Labs
python --version
```

You want Python 3.10 or newer. If that command is not found, install Python from [python.org](https://www.python.org/downloads/) and check **Add python.exe to PATH**, then open a new terminal.

To get the files without git:

1. On GitHub, click **Code → Download ZIP**.
2. Unzip it.
3. `cd` into the unzipped folder.

To get the files with git:

```text
git clone https://github.com/jacobbweber/AgenticAI-Labs.git
cd AgenticAI-Labs
```

## How to ask the AI for help

Say this, in your own words:

> Open `education/00_atoms/lab1_script_posts_json.md`. Write that script. Do not add extra features.

If it invents a second lab or pulls in a framework, stop it. Point at `AGENTS.md`.

Next: [run the first lab](./05_first_lab.md).
