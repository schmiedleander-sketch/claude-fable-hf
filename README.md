---
title: Claude Fable 5 HF
emoji: 🤗
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 5.29.0
app_file: app.py
pinned: false
---

# Claude Fable 5 for Hugging Face

A full Hugging Face Space app inspired by the feel and structure of a strong reasoning assistant, without using Anthropic's proprietary model, API, or private prompt.

This project is a clean, deployable Gradio app that:
- Sends chat requests to Hugging Face Inference Providers
- Uses a configurable model from `MODEL_ID`
- Reads a Hugging Face token from the Space secret `HF_TOKEN`
- Includes a Fable-style system prompt for independent assistant behavior
- Works as a standalone local app or Hugging Face Space

## Features

- Chat interface with user/assistant history
- Temperature and max-token controls
- Error handling for invalid model/token/provider configuration
- Easy swapping of model provider and model ID
- Local testing via `python app.py`

## Required secrets/variables

In a Hugging Face Space:
- Secret: `HF_TOKEN`
- Optional variable: `MODEL_ID` (default: `HuggingFaceH4/zephyr-7b-beta`)

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export HF_TOKEN=hf_...
export MODEL_ID=HuggingFaceH4/zephyr-7b-beta
python app.py
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:HF_TOKEN="hf_..."
$env:MODEL_ID="HuggingFaceH4/zephyr-7b-beta"
python app.py
```

## Notes

This is an open-source demo scaffold. It does not replicate proprietary Anthropic systems or claim access to Claude/Fable internals, model weights, or private infrastructure.

Use a model that is reachable through your Hugging Face account and inference provider. Availability, quota, and pricing vary by account and selected model.
