# Running Models Locally with Ollama and LM Studio

Both Ollama and LM Studio let you run AI models directly on your own computer. They run in the background and listen for incoming HTTP requests on a specific port. Your lab scripts will send JSON data to that port to get model responses.

You only need to install one of these tools to complete the course:
- **Ollama (Recommended)**: This is the simplest way to get started. Ollama is lightweight, runs from the command line, and natively supports the `/api/generate` endpoint used in our first few labs.
- **LM Studio**: This provides a user-friendly graphical desktop interface. It serves models using the OpenAI-compatible `/v1/chat/completions` endpoint. It is a great choice if you prefer a visual interface or already have models downloaded in LM Studio.

## Option 1: Setting up Ollama (Recommended)

1. **Install Ollama**: Download and install the app from [https://ollama.com/download](https://ollama.com/download).
2. **Download your model**: Open your terminal and pull the model you selected:

```text
ollama pull llama3.2:1b
```

3. **Keep Ollama running**: On Windows and macOS, Ollama starts automatically and runs quietly in your system tray. On Linux, run `ollama serve` in a terminal window.
4. **Test the model**: Run a quick test in your terminal to verify that the model responds:

```text
ollama run llama3.2:1b "Say hello in one sentence."
```

5. **Configure your project**: From the root of this repository, copy the example environment file if you haven't already:

```bash
cp .env.example .env
```

```powershell
copy .env.example .env
```

Ensure the following Ollama settings are uncommented in your `.env` file:

```text
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2:1b
```

> **Note**: `127.0.0.1` represents your local computer (localhost), and port `11434` is Ollama's default listening port. If `ollama pull` shows a memory error, return to [Pick a Model](./01_pick_a_model.md) and pick a smaller size.

## Option 2: Setting up LM Studio

1. **Install LM Studio**: Download and install the app from [https://lmstudio.ai](https://lmstudio.ai).
2. **Download a model**: Inside LM Studio, search for your preferred model family and download a **Q4** quantized model that fits your available memory.
3. **Start the local server**: Navigate to the **Developer / Local Server** tab inside LM Studio, select your model, and click **Start Server**. Note the port number (which defaults to `1234`).
4. **Configure your project**: Open your `.env` file, uncomment the LM Studio lines, and update the model name to match the model loaded in LM Studio:

```text
OLLAMA_HOST=http://127.0.0.1:1234
OLLAMA_MODEL=the-name-shown-in-lm-studio
```

Chapter 00 shows the request format for both Ollama and OpenAI-style servers. When using LM Studio, your script will connect to `/v1/chat/completions` and read `choices[0].message.content`.

## Which Tool Should You Choose?

| Your Goal | Best Choice |
|---|---|
| Follow course labs directly with minimal configuration | **Ollama** |
| Experiment with models using a visual desktop app before coding | **LM Studio** |
| Use both tools depending on the project | Both work great! Just point `OLLAMA_HOST` in `.env` to whichever port is active. |

You do not need any external cloud account or internet connection to run local models.

---

**Next Steps**: [Set up your code editor](./04_editors_and_terminal.md), then [run your first lab script](./05_first_lab.md). If you would rather use a cloud provider instead, see [Cloud APIs](./03_cloud_apis.md).
