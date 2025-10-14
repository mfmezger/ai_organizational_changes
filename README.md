# AI Organizational Changes

## Description
This repository contains code to analyze organizational changes using AI models.


**Table of Contents:**
- [AI Organizational Changes](#ai-organizational-changes)
  - [Description](#description)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Monitoring](#monitoring)




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

```python
ai_organizational_changes
    ├── init_model.py # methods to initialize the models: OpenRouter, Cohere, Gemini
    ├── main.py # Main loop for async execution of the queries.
    └── model.py # Definition of the Output Format for the models.
````

## Monitoring

This repository uses Monitoring and Logging via Pydantic Logfire.
To use Logfire you either need an account in the cloud service or self deploy Logfire.
