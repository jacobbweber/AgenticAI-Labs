# Running Your First Lab
 
Let's test your connection by running a single Python script. When this script prints generated text from your model to the screen, you'll know your environment is fully ready!

---

## 1. Verify Your Python Installation

Open your terminal and check that Python is installed:

```text
python --version
```

If that command returns an error or is unrecognized, try `python3 --version`. Use whichever command works on your system for the remaining steps.

---

## 2. Check Your Model Connection

If you haven't created your `.env` file yet, copy the example template from your terminal at the repository root:

```bash
cp .env.example .env
```

```powershell
copy .env.example .env
```

Make sure your active provider is configured in `.env`:

- **For Ollama**: Verify that Ollama is running and has your model downloaded by running `ollama list`. The model name in `.env` should match the name in that list.
- **For LM Studio**: Start the local server inside the app, and make sure `OLLAMA_HOST` in `.env` matches the server's port (typically `http://127.0.0.1:1234`).
- **For Cloud Providers**: Ensure your API key and URL are uncommented in `.env` as described in [Cloud APIs](./03_cloud_apis.md).

---

## 3. Run the Reference Test Script

This repository includes a pre-written reference script for the first lab so you can immediately test your setup.

From the root directory, run:

```text
python education/00_atoms/lab1_script_posts_json.py
```

The script will automatically read your `.env` configuration, connect to the provider, and request a response.

---

## What You Should See

If everything is connected properly, the model will output a short response describing HTTP POST requests. 

| Output | Meaning & Next Steps |
|---|---|
| **A few sentences of text** | **Success!** Your setup is working smoothly. You are ready to start Chapter 00. |
| **`URLError` or Connection Refused** | The script cannot reach the server at `OLLAMA_HOST`. Make sure Ollama or LM Studio is running. |
| **HTTP 404 Error** | The provider is running, but cannot find the specified model name. Check `ollama list` or your `.env` model string. |
| **Empty Response** | The model responded but generated no text. Try a slightly larger model or check model availability. |

---

## 4. Writing the Lab Yourself

Now that your setup is verified, you are ready to learn by building!

Open [`education/00_atoms/00_script_provider_weights.md`](../education/00_atoms/00_script_provider_weights.md) to read the core concept. Then open [`education/00_atoms/lab1_script_posts_json.md`](../education/00_atoms/lab1_script_posts_json.md) to see the lab brief.

> **Tip**: If you want to write the code from scratch, delete `lab1_script_posts_json.py` and implement it following the brief. Keeping markdown briefs while deleting `.py` files allows you to reset any lab at any time.

---

## Keep in Mind

If you are using a compact 1B model on a CPU, its responses may be brief or simplistic. That is completely normal! The value of these labs is learning how scripts send JSON, parse responses, and manage tool loops. Whenever you observe unexpected model behaviors, record them under the **Notes** section of your lab brief.

---

**Next**: Head over to [Chapter 00: Script, Provider, Weights](../education/00_atoms/00_script_provider_weights.md) to begin the course!
