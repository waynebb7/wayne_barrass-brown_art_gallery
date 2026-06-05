"""Export Cursor JSONL transcript to ChatGPT-style markdown."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
DEFAULT_JSONL = Path(
    r"C:\Users\wayne\.cursor\projects\d-git-wayne-barrass-brown-art-gallery"
    r"\agent-transcripts\f8a3e0ac-24c0-4150-bea5-2e55f6a851f3"
    r"\f8a3e0ac-24c0-4150-bea5-2e55f6a851f3.jsonl"
)
DEFAULT_OUTPUT = ROOT / "CURSOR_CONVERSATION_TRANSCRIPT.md"


def extract_text(entry: dict) -> str:
    parts: list[str] = []
    for block in entry.get("message", {}).get("content", []):
        if block.get("type") == "text":
            text = block.get("text", "")
            if text:
                parts.append(text)
    return "\n\n".join(parts).strip()


def clean_user_text(text: str) -> str:
    return re.sub(r"</?user_query>\s*", "", text).strip()


def clean_assistant_text(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?:\[REDACTED\]\s*){2,}", "[REDACTED]\n\n", text)
    return text.strip()


def role_label(role: str) -> str:
    name = "User" if role == "user" else "Assistant"
    color = "blue" if role == "user" else "green"
    return (
        f'<span style="font-size:2em; color:{color}; font-weight:bold;">{name}</span>'
    )


def build_messages(jsonl_path: Path) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []

    for line in jsonl_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue

        entry = json.loads(line)
        role = entry.get("role", "assistant")
        text = extract_text(entry)
        text = clean_user_text(text) if role == "user" else clean_assistant_text(text)

        if not text or text == "[REDACTED]":
            continue

        if messages and messages[-1]["role"] == role:
            messages[-1]["text"] += "\n\n" + text
            messages[-1]["text"] = re.sub(r"\n{3,}", "\n\n", messages[-1]["text"]).strip()
        else:
            messages.append({"role": role, "text": text})

    return messages


def export_transcript(jsonl_path: Path, output_path: Path) -> int:
    messages = build_messages(jsonl_path)
    exported = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    parts = [f"# Exported Conversation\n\n_Exported: {exported}_\n\n"]
    for message in messages:
        parts.append(f"{role_label(message['role'])}\n\n{message['text']}\n")

    output_path.write_text("\n".join(parts).replace("\r\n", "\n"), encoding="utf-8")
    return len(messages)


def main() -> None:
    jsonl_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_JSONL
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUTPUT

    if not jsonl_path.exists():
        raise SystemExit(f"Transcript not found: {jsonl_path}")

    count = export_transcript(jsonl_path, output_path)
    print(f"Wrote {output_path}")
    print(f"Messages: {count}")


if __name__ == "__main__":
    main()
