import os
from typing import Any

import gradio as gr
from huggingface_hub import InferenceClient

MODEL_ID = os.getenv("MODEL_ID", "HuggingFaceH4/zephyr-7b-beta")
HF_TOKEN = os.getenv("HF_TOKEN")

SYSTEM_PROMPT = """You are Fable, a thoughtful, capable assistant inspired by the style of a strong
reasoning model. Your job is to be precise, helpful, and structured.

Core behavior:
- Answer direct questions clearly and accurately.
- For difficult tasks, break them into steps and explain the reasoning in plain language.
- Be transparent about uncertainty and ask clarifying questions when needed.
- Prefer practical, useful answers over fluff.
- Maintain a calm, professional, and warm tone.
- Do not claim to be Claude, Anthropic, or any private model.
- Do not claim to have access to systems, logs, or privileged information you do not have.
- If the user asks for code, explain it clearly and provide usable examples when appropriate.
- If the user provides incomplete context, ask targeted clarifying questions before assuming.
"""


def _history_messages(history: list[Any]) -> list[dict[str, str]]:
    """Normalize Gradio history into a list of chat dicts."""
    messages: list[dict[str, str]] = []

    for item in history or []:
        if isinstance(item, dict):
            role = str(item.get("role", "")).strip()
            content = item.get("content")
            if role in ("user", "assistant") and isinstance(content, str) and content.strip():
                messages.append({"role": role, "content": content.strip()})
            continue

        if isinstance(item, (list, tuple)) and len(item) == 2:
            left, right = item
            pair = [("user", left), ("assistant", right)]
            for role, value in pair:
                if isinstance(value, str) and value.strip():
                    messages.append({"role": role, "content": value.strip()})

    return messages


def respond(message: str, history: list[Any], temperature: float, max_tokens: int) -> str:
    if not HF_TOKEN:
        raise gr.Error(
            "Missing HF_TOKEN. Add it as a secret in your Hugging Face Space settings."
        )

    if not message or not message.strip():
        raise gr.Error("Please enter a message before sending.")

    client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(_history_messages(history))
    messages.append({"role": "user", "content": message.strip()})

    try:
        result = client.chat_completion(
            messages=messages,
            temperature=float(temperature),
            max_tokens=int(max_tokens),
        )

        answer = result.choices[0].message.content
        if isinstance(answer, str) and answer.strip():
            return answer.strip()

        return "The model returned an empty response. Try again with a different prompt or model."

    except gr.Error:
        raise
    except Exception as exc:
        raise gr.Error(
            "The inference request failed. Please check that the HF_TOKEN is valid, "
            "the selected model is available for your account, and the provider has capacity. "
            f"Details: {exc}"
        ) from exc


demo = gr.ChatInterface(
    fn=respond,
    chatbot=gr.Chatbot(type="messages", height=560),
    title="Claude Fable 5 HF",
    description=(
        "A Hugging Face demo app inspired by a strong reasoning assistant. "
        "This is independent of Anthropic and uses the model configured in the app environment."
    ),
    additional_inputs=[
        gr.Slider(0.0, 1.5, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(64, 2048, value=768, step=64, label="Max new tokens"),
    ],
    examples=[
        "Explain a difficult concept in simple terms.",
        "Plan a weekend project from idea to launch.",
        "Help me debug a Python error and explain the root cause.",
        "Write a concise product brief for a new AI tool.",
    ],
)

if __name__ == "__main__":
    demo.queue().launch()
