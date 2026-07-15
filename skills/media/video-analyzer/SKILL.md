---
name: video-analyzer
description: Watch and analyze videos from YouTube URLs or local/downloaded video files (mp4, mov, mkv, webm). Produces summaries, answers questions about content, and deep-dives into specific time segments ("what happens between 2:15 and 2:45", "explica el minuto 3"). Use this skill whenever the user shares a video URL or video file path, or asks to watch, summarize, transcribe, analyze, take notes on, or understand any part of a video — even casually phrased ("resume este video", "qué dicen en el segundo 40", "analiza este clip", a bare YouTube link with a question). Trigger for YouTube, Shorts, reels, and downloaded files alike.
---

# Video Analyzer

Claude can't stream video directly. This skill bridges that gap: a Python pipeline (vendored from [bradautomates/claude-video](https://github.com/bradautomates/claude-video), MIT — see THIRD_PARTY_NOTICES.md) downloads the video if needed, extracts auto-scaled JPEG frames with ffmpeg, pulls a timestamped transcript (native captions first, Whisper API fallback), and prints a markdown report listing every frame path. Claude then `Read`s the frames as images, aligns them with the transcript, and answers the user's actual question.

## Language of output

Respond in the language the user used to ask. If they ask in Spanish, summaries and notes go in Spanish even if the video is in English (quote verbatim lines in the original language). If they ask in English, answer in English. If they explicitly request a language, that wins.

## Choosing the right mode

Pick the cheapest mode that actually answers the question — frames are expensive in tokens, so don't extract more video than the question needs.

| Situation | Mode |
|---|---|
| General/factual question about a YouTube video with captions ("does he mention X?", "what's the conclusion?") | **Transcript-only**: fetch captions, skim, answer. No frames. |
| "Summarize / analyze / take notes on this video" | **Full watch**: run the pipeline on the whole video, read all frames. |
| Question about a specific moment or range ("qué pasa entre el 0:40 y el 1:10", "explain the chart at 2:15") | **Segment deep-dive**: run with `--start`/`--end`. Denser frames inside the range. |
| Several distinct moments of interest | **Multi-segment**: one pipeline run per segment, shared `--out-dir`. |
| Video > 10 min and the user wants everything | Confirm first; suggest segment(s) or a transcript-first pass, then frames only where the transcript is unclear or visuals matter. |

### Transcript-only fast path

For captioned YouTube videos where visuals likely don't matter:

```bash
yt-dlp --skip-download --write-auto-subs --write-subs --sub-langs "es,en,.*" --sub-format vtt -o "/tmp/va-sub/%(id)s" "<url>"
```

Then read the `.vtt`, answer from it. If the answer hinges on something visual (a chart, a demo, on-screen code), escalate to a segment deep-dive at the relevant timestamp instead of guessing.

## Dependencies

- **ffmpeg + ffprobe** on PATH — frame/audio extraction
- **yt-dlp** on PATH — download + caption fetching (`pip install yt-dlp --break-system-packages` if missing)
- **Python 3.9+**
- **Optional:** Whisper key for videos without captions: `GROQ_API_KEY` (preferred) or `OPENAI_API_KEY` in `~/.config/watch/.env`. Without one, captioned videos work fine; uncaptioned videos return frames-only.

Verify with `python scripts/setup.py --check` the first time, or when a run fails with a missing-binary error.

## Pipeline

```bash
python scripts/watch.py "<youtube-url-or-local-path>" [flags]
```

Flags:
- `--start T` / `--end T` — focus on a section (`SS`, `MM:SS`, or `HH:MM:SS`). Auto-scales fps denser inside the range. Use for ANY question about a specific moment.
- `--max-frames N` — lower the cap for a tighter token budget (default 80, hard max 100).
- `--resolution W` — frame width in px (default 512). Bump to 1024 when the question involves reading on-screen text, code, slides, or charts.
- `--whisper groq|openai` — force a Whisper backend.
- `--no-whisper` — skip transcription (frames-only). Use for videos with no audio track.
- `--out-dir DIR` — working directory (default: auto tmp dir). Reuse one dir for multi-segment runs so cleanup is a single `rm -rf`.

Auto-fps budgets (full-video mode): ≤30s → ~30 frames; ≤1min → ~40; 1–3min → ~60; 3–10min → ~80; >10min → 100 sparse (warning printed — prefer segments).

The report on stdout contains: header (Title, Uploader, Duration, Transcript source), a `## Frames` section with `- \`<absolute-path>\` (t=MM:SS)` lines, a `## Transcript` section with `[MM:SS] text` lines, and `Work dir: <path>` in the footer.

## Workflow

### 1. Parse what the user actually wants

- Identify the source: URL or local path. For local files, verify the file exists before running.
- Identify the ask: full summary, specific question, or segment(s). Convert phrasings like "los primeros 30 segundos", "del minuto 2 al 3", "la parte donde habla de precios" into `--start`/`--end` values. For fuzzy references ("la parte donde…"), do a transcript-only pass first to locate the timestamp, then deep-dive that range.

### 2. Run the pipeline

```bash
# Full watch
python scripts/watch.py "<source>"

# Segment deep-dive
python scripts/watch.py "<source>" --start 2:15 --end 2:45

# Segment with readable on-screen text
python scripts/watch.py "<source>" --start 0:40 --end 1:10 --resolution 1024

# Multi-segment (shared work dir)
python scripts/watch.py "<source>" --start 0:00 --end 0:30 --out-dir /tmp/va-job
python scripts/watch.py "<source>" --start 4:10 --end 4:50 --out-dir /tmp/va-job
```

Capture stdout — it's the map to everything.

### 3. Read every listed frame

Read ALL frame paths in a single message (parallel `Read` calls — they render as images). Pair each frame's `t=MM:SS` with the transcript line at that timestamp. Don't skip frames: visuals carry what the transcript misses (B-roll, on-screen text, graphics, demos, emotion).

**Work dir placement in sandboxed environments (e.g. Cowork):** the Read tool may not reach bash's `/tmp`. Before running the pipeline, prefer passing `--out-dir` inside a directory Read can open (such as the session outputs folder). If Read fails on a frame path, don't retry path variants one by one — copy the whole `frames/` folder into a Read-accessible location in a single `cp -r`, read from there, and delete the copies during cleanup.

### 4. Answer or write notes

For a direct question, answer it directly, citing timestamps like `[2:31]`.

For a summary/notes request, write `<work-dir>/<slug>-notes.md` (ask where to save if the user wants it permanent) with this structure, in the user's language:

```markdown
# <Title>

**Fuente:** <URL o ruta local> · **Duración:** <mm:ss> · **Transcripción:** <captions / whisper / ninguna>

## Resumen en una línea
<≤20 palabras — la idea central>

## TL;DR
<3–5 bullets con los argumentos o momentos clave>

## Línea de tiempo
- **[00:00]** <qué se ve + qué se dice>
<una fila por momento relevante, no por frame>

## Citas clave
> "<cita textual en idioma original>" — [mm:ss]

## Notas visuales
<lo que el video muestra y la transcripción sola no captura>
```

For a segment deep-dive, structure the answer around the range: what happens second by second, what's said, what's shown, and the answer to the user's specific question first.

### 5. Clean up

Delete the work dir after writing the answer/notes (`Work dir:` path from the report footer → `rm -rf`). It holds the full video + frames. If the user passed a non-tmp `--out-dir`, ask before deleting. Never delete the user's original local video file.

## Common gotchas

- **Shorts / age-gated / members-only / region-locked** — yt-dlp may fail. Surface its stderr verbatim; don't retry silently and don't invent content.
- **No captions + no Whisper key** — report says `Transcript: none available`. Tell the user they can add a Groq key in `~/.config/watch/.env`, or proceed frames-only (`--no-whisper`) and say the analysis is visual-only.
- **Local file with no audio** — use `--no-whisper`.
- **Videos > 30 min** — confirm before a full run; a sparse 100-frame scan of a 60-min video is rarely useful. Locate the relevant part via transcript, then segment deep-dive.
- **Fuzzy segment references** — never guess timestamps. Locate via transcript first.
- **Groq rate-limit** — the script retries Groq twice then errors; pass `--whisper openai` to switch.

## What NOT to do

- Don't "watch" a video by inventing content from its title or thumbnail. If the pipeline fails, say so.
- Don't write the summary before actually reading the frames.
- Don't run a full-video extraction when the question is about one moment — use `--start`/`--end`.
- Don't skip cleanup; frame dumps + downloads are large.
