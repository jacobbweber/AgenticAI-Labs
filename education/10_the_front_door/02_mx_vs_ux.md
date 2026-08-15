# 10: Machine experience vs user experience

After this page you can say which payload is for the model and which is for the person. There is no paired lab for this page.

## Data
**MX** (machine experience) is the payload the model and the tools need. In this chapter that means tool JSON, traces, and `<think>` blocks. A trace is a log of what the loop did (which tool, which args, which error). `<think>` is text the model produces for itself before the visible answer. Chapter 12 strips it.

**UX** (user experience) is the payload the person needs. Visible tokens, buttons, and errors in one sentence.

A **channel** is one stream of frames with one job. MX and UX are two channels. They can share one HTTP connection if you tag each frame. They must not share one text box.

**Demux** means split one incoming stream into those two channels. Chapter 12 does the CoT (chain-of-thought) split. This page only names the two sides.

This page has no `.py`. The SSE lab yields both MX-like frames (`tool_call_start`, `tool_call_result`) and UX-like frames (`token_delta`). `OLLAMA_HOST` defaults to `http://192.168.1.29:11434`. `OLLAMA_MODEL` defaults to `qwen3.6:35b-a3b-65k`. Port `11434` is Ollama.

## Information
If you dump MX into the page, the person sees tool JSON and `<think>` text. That looks like a broken UI. It is not a model bug. The page drew the wrong channel.

A debug panel can show MX. The main view should not. Split first. Then draw UX. Log MX.

## Knowledge
1. Tag each frame as MX or UX, or put them on two routes.
2. Show UX on the main view: tokens, buttons, one-sentence errors.
3. Log MX: tool JSON, traces, `<think>`.
4. Do not print `tool_call_start` args or `<think>` into the same string as `token_delta`.
5. Do not write the chapter 12 splitter here. Name the two channels only.

## Wisdom
Stop when you can point at a frame and say MX or UX. Do not build the demuxer or a debug panel yet. If you add them now, a leaked `<think>` block could come from the splitter or from the page.

## The When and Why
- **When:** you have both a model stream and a person watching a page.
- **Why:** mixing MX and UX looks like a broken UI. The person asked for tokens, not tool JSON.

## How it works

```mermaid
flowchart TD
    subgraph mxux_stream [Incoming stream]
        S["SSE or WebSocket frames"]
    end
    subgraph mxux_demux [Split]
        D["demux by event_type or tag"]
    end
    subgraph mxux_ux [User channel]
        U["main view tokens buttons errors"]
    end
    subgraph mxux_mx [Machine channel]
        M["log tool JSON traces think"]
    end
    S --> D
    D -->|"token_delta type token"| U
    D -->|"tool_call_start tool_call_result think"| M
```

Walkthrough of the frames lab 1 already yields:

1. `session_started` is MX (session status). Log it. Do not draw it as chat text.
2. `token_delta` with `data.delta` is UX. Append it to the visible string.
3. `tool_call_start` with `tool_name` `read_file` and `args.path` `config.json` is MX. Log it. A debug panel may show the name. The main view should not dump the args JSON.
4. `tool_call_result` with `output` `{'env': 'prod'}` is MX. Same rule.
5. `turn_complete` is MX status. The UX side can show "done" in one sentence. It should not dump `total_events`.

The new fact is two channels. The splitter is chapter 12.

## Data contract

**Intended UX frame**

```json
{ "type": "token", "text": "string" }
```

**Intended MX frame** (not drawn on the main view)

```json
{ "type": "tool", "tool_name": "string", "args": {} }
```

Lab 1 does not use `type` / `text`. It uses `event_type` and `data.delta`. See Notes.

## Lab
No extra lab for this page. Use the SSE lab and say which frames are MX and which are UX.

- Module: [this file](./02_mx_vs_ux.md)
- Lab 1: [lab1_sse_streaming_api.md](./lab1_sse_streaming_api.md) — mixed frames. Point at each `event_type`.
- Stub: [STUB_mx_vs_ux.md](./STUB_mx_vs_ux.md) — what a real split lab would cover. Not runnable.
- Chapter 12: the CoT demuxer.

## Related
- **Chapter 12 CoT demux:** the splitter for `<think>` vs visible text.
- **01_frontend.md:** the page that must draw only UX on the main view.
- **00_fastapi_sse.md:** the frames that arrive mixed.

## Notes
- Keep the existing ideas: MX is tool JSON, traces, and `<think>`. UX is visible tokens, buttons, and one-sentence errors. A debug panel can show MX. The main view should not.
- No paired `.py` for this page. Lab 1 already mixes MX and UX in one generator. The intended UX key is `{ "type": "token", "text": "string" }`. The script uses `event_type` `token_delta` and `data.delta`.
- Moved from modules/05/03.
