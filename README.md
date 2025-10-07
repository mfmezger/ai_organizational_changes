# AI Organizational Changes


## Description


## Installation

This project is implemented using uv. You can find out how to install uv here:

```link
docs.astral.sh/uv/getting-started/installation/
```

Then you can install the dependencies using uv:

```bash
uv sync
```


## Usage

To choose the model set it in the model name in the main file in line 55.

You can choose different LLM Providers already integrated are:

- Gemini API
- Cohere API
- OpenRouter (you can basically use every model via openrouter)

Choose the correct provider you want in the ```main.py``` file lines 57-66. As default OpenRouter with OpenAIs GPT-5 is set.

## Monitoring

This repository uses Monitoring and Logging via Pydantic Logfire.
To use Logfire you either need an account in the cloud service or self deploy Logfire.
