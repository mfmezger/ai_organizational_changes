# 🤖 Accompanying code repository for the paper "Generative AI's Impact on Organizational Design: An Analysis Based on Human-AI Collaboration"

## What does this program do?

**In short:** This program asks genAI models (like ChatGPT, Claude, etc.) which jobs might be affected by AI.

### 📚 Background

Artificial intelligence has been rapidly increasing in sophistication and impact, reinforcing discussions of its extensive potential to disrupt individual jobs and organizations. Through our investigation into the disruptive potential of generative artificial intelligence (genAI) on organizations, we don't just study genAI — **we also collaborate with it**.

We consolidated data from the **O*Net 2023 database** to create a list of **85 corporate knowledge worker roles** (and associated skill levels). Then, together with **five different genAI models**, we assessed which roles AI will automate or augment (human with AI) in the near future.

---

## 🤔 Why use LLMs for This? Are they reliable?

A valid question: *"Can we trust AI to judge which jobs will be affected by AI?"*

Short answer: **Yes, for the following reasons.**

### The Problem with Human Coders

Traditional qualitative research uses human coders to categorize data. But humans have problems:

| Issue | Description |
|-------|-------------|
| 🧠 **Subjectivity** | Different researchers interpret the same data differently |
| 😴 **Fatigue** | Humans get tired and make more mistakes over time |
| 💭 **Bias** | Personal opinions and experiences influence coding decisions |
| 📊 **Inconsistency** | The same person might code differently on different days |

### Metric 🌀

To combat this, researchers typically use **multiple coders** and measure **inter-rater reliability** — checking if different humans agree with each other.

> **Gwet, K., (2001)** Handbook of inter-rater reliability. Gaithersburg, MD: STATAXIS Publishing Company, pp.223-246.

Cronbach alpha is not a suitable metric for this as it is designed for measuring reliability of items (questions of a questionnaire):

> "Any research based on measurement must be concerned with the accuracy or dependability or, as we usually call it, reliability of measurement. A reliability coefficient demonstrates whether the test designer was correct in expecting a certain collection of items to yield interpretable statements about individual differences (25)." Cronbach (1951), p.1

> **Cronbach, L.J. (1951)** Coefficient alpha and the internal structure of tests. Psychometrika 16, 297–334 (1951). https://doi.org/10.1007/BF02310555

### LLMs are more consistent than humans

Recent research has shown that Large Language Models actually **outperform humans** in consistency:

> **Tai et al. (2024)** emphasize the subjectivity of qualitative data coding due to human coder bias. To improve reliability, multiple coders are traditionally used.

> **Gilardi et al. (2023)** found that LLMs offer consistent performance in coding tasks, **outperforming human coders in consistency**. This suggests LLMs as a reliable alternative for qualitative data analysis.

### Why LLMs work well for this task

| Advantage | Explanation |
|-----------|-------------|
| ✅ **Perfect consistency** | Same prompt + temperature 0 = same answer every time |
| ✅ **No fatigue** | Job #85 is coded with the same quality as Job #1 |
| ✅ **No personal bias** | LLMs don't have career anxieties about automation |
| ✅ **Multiple "coders"** | We use 5-6 different models as independent raters |
| ✅ **Transparent process** | The exact prompt and parameters are documented |

### Methodological Consideration: Potential Bias

You might wonder: *"Using AI to predict AI's impact on jobs... isn't that biased?"*

**This is not the case.** Here's why:

1. **LLMs are trained on human knowledge** — they reflect collective human understanding of jobs and automation
2. **We use multiple models** — if GPT-5, Claude, and Gemini all agree, that's like having 5 expert coders agree
3. **Results are transparent** — you can see exactly what each model said and why
4. **It is a prediction, not a fact** — we are measuring AI's *assessment*, which is the research question itself

### Methodological Approach

This research employs human-AI collaboration to study human-AI collaboration. The research method mirrors the research topic — AI and humans working together to understand how AI and humans will work together.

> 📖 *References:*
> - *Tai, R. H., Bentley, L. R., Xia, X., Sitt, J. M., Fankhauser, S. C., Chicas-Mosier, A. M., & Monteith, B. G. (2024). An Examination of the Use of Large Language Models to Aid Analysis of Textual Data. International Journal of Qualitative Methods, 23. https://doi.org/10.1177/16094069241231168*
> - *Gilardi, F., Alizadeh, M., & Kubli, M. (2023). ChatGPT outperforms crowd workers for text-annotation tasks. Proceedings of the National Academy of Sciences, 120(30), e2305016120. https://doi.org/10.1073/pnas.2305016120*

## 🧪 How This Works: Programmatic AI vs. "Chatting with ChatGPT"

This section explains **why we use code to talk to AI models** instead of just typing prompts into ChatGPT like a normal person.

### The problem with manual prompting

When you use ChatGPT through the website, you might type something like:

> *"Hey ChatGPT, will accountants be replaced by AI?"*

This has several problems for **scientific research**:

| Problem | Why it matters |
|---------|----------------|
| 🎲 **Inconsistent results** | Ask the same question twice, get different answers |
| 📝 **No structure** | The AI might give you a 3-paragraph essay or a single word |
| 🔄 **Not reproducible** | You can't prove you asked exactly this question |
| ⏱️ **Doesn't scale** | Asking 85 jobs × 5 models = 425 manual questions? No thanks |
| 🧠 **Human bias** | You might unconsciously phrase questions differently |

### Our solution: Programmatic prompting

Instead of chatting, we write **code** that:

1. **Sends the exact same prompt** to every AI model
2. **Forces structured responses** (not free-form text)
3. **Logs everything** for reproducibility
4. **Processes hundreds of jobs automatically**
---
### 📚 Design
---

#### Coding Definitions

- 🔴 **Automated by AI** — Machines take over a human task completely (defined in the programming code as "likely_automated_by_AI")
- 🟡 **Augmented with AI** — Humans collaborate closely with machines to perform a task (defined in the programming code as "likely_augmented_with_AI")
- 🟢 **Human-only** — The job remains performed by humans without AI involvement (defined in the programming code as "likely_human_only")

> 📖 *Based on: Raisch, S., & Krakowski, S. (2021). Artificial Intelligence and Management: The Automation-Augmentation Paradox. Academy of Management Review, 46(1), 192–210. https://doi.org/10.5465/amr.2018.0072*


### How our prompt is constructed

The prompt construction involves two key components:

#### 1. System Prompt

The system prompt is defined in `main.py` line 33:

```python
system_prompt = """Based on what you know, can you please read the following
role and predict which roles are likely to be impacted by generative AI
and which skills specifically for the role will be impacted by generative AI"""
```

#### 2. Model Docstring (Automatic)

The Pydantic AI framework automatically includes the docstring from the `JobReplacementPrediction` model in the prompt. This docstring provides detailed instructions about the expected output format and field definitions:

```python
class JobReplacementPrediction(BaseModel):
    """Model for job replacement prediction.

    Attributes:
        job_title (str): The title of the job.
        genai_impact (bool): Whether the job is likely to be automated by AI. Automation means that machines take over a human task. Whether the job is likely to be augmented with AI. Augmentation means that Humans collaborate closely with machines to perform a task. Whether the job is likely to remain human-only.
        skills (list[str]): List of skills that the genai takes over completely.
        explanation (str): Explanation for the prediction. Maximum 100 words.
    """
```

This **docstring** provides context and definitions for the structured output, ensuring consistent interpretation across different AI models.

#### Complete Prompt Structure

When processing a job, the AI receives the combined instruction: system prompt + model docstring + job input.

```python
response = await agent.run(f"Job:\n{job}")
```

If the job is "Accountant", the AI receives the complete context: system instructions, output format specifications, and the job title itself.

### The Magic: Structured output (No more rambling!)

In `model.py`, we define **exactly** what the AI must return using a Pydantic model:

```python
class JobReplacementPrediction(BaseModel):
    job_title: str
    genai_impact: Literal[
        "likely_automated_by_ai",
        "likely_augmented_with_ai",
        "likely_human_only"
    ]
    skills: list[str]
    explanation: str
```

The full model definition includes a comprehensive docstring that explains each field's meaning and purpose (see `model.py` lines 6-13). This docstring, along with the system prompt, is automatically included in the instruction sent to each AI model, ensuring consistent interpretation and output formatting across all models.

This means the AI **cannot** respond with:

> *"Well, it depends on many factors... in my opinion... blah blah..."*

Instead, it **must** return a structured object like:

```json
{
  "job_title": "Accountant",
  "genai_impact": "likely_augmented_with_ai",
  "skills": ["data entry", "invoice processing", "report generation"],
  "explanation": "Accountants will use AI for routine tasks but remain essential for judgment calls and client relationships."
}
```
**Example output (disclaimer: everything is genAI generated except the first column):**
| job_title | genai_impact | skills | explanation | job |
|:---|:---|:---|:---|:---|
| Accountant | likely_augmented | ['Data entry', 'Financial analysis'] | Generative AI is likely to augment the roles of accountants and auditors by automating repetitive tasks such as data entry, bookkeeping, and routine financial analysis. This technology can also assist in drafting financial reports, reducing the time spent on these activities. However, the need for human oversight in complex decision-making, ethical judgments, and client interactions will remain crucial. Accountants and auditors will increasingly need to develop skills in AI literacy, data interpretation, and strategic advisory to complement AI capabilities. | Accountant |

### Why this matters for research

| Aspect | ChatGPT Website | Our Programmatic Approach |
|--------|-----------------|---------------------------|
| **Reproducibility** | ❌ Cannot prove what was asked | ✅ Code is the proof |
| **Consistency** | ❌ Different phrasing = different results | ✅ Exact same prompt every time |
| **Scalability** | ❌ 425 manual queries impractical | ✅ Runs overnight automatically |
| **Structure** | ❌ Free-form text, must parse by hand | ✅ JSON, directly into Excel |
| **Temperature control** | ❌ Hidden, changes randomly | ✅ Set to 0 for determinism |
| **Multi-model comparison** | ❌ Switch tabs, retype everything | ✅ Loop through 5 models automatically |
| **Rate limit handling** | ❌ "Rate limit exceeded" | ✅ Automatic retry with backoff |
| **Logging** | ❌ Hope you copied it somewhere | ✅ Logfire records everything |

### The Temperature Setting

In our code, we use `temperature=0`:

```python
agent = init_agent(
    system_prompt=system_prompt,
    model_name=model_name,
    temperature=0,  # ← This is important!
)
```

**Temperature** controls randomness:
- `temperature=0` → Same question = same answer (deterministic)
- `temperature=1` → More creative, but less consistent

For scientific research, we want **reproducibility**, so we use 0.

> 📖 *See: Renze, M. (2024, November). The Effect of Sampling Temperature on Problem Solving in Large Language Models. In Y. Al-Onaizan, M. Bansal, & Y.-N. Chen, Findings of the Association for Computational Linguistics: EMNLP 2024, Miami, Florida, USA.*

### Summary: Advantages of Programmatic Approach

🎯 **Precision**: We control exactly what we ask  
🔁 **Reproducibility**: Anyone can run the same code, get same results  
📊 **Structure**: Data goes straight into analysis tools  
⚡ **Scale**: 425 API calls while you sleep  

---

## 💰 Cost calculation: What does this cost?

Running AI models via API costs money. The following section provides a cost breakdown.
Disclaimer: We repeated the runs because a new genAI model from Google was deployed during the ongoing research activities. Therefore six models are depicted in the following. Five models are reflected in the associated paper.

### Number of API Requests

| Component | Count |
|-----------|-------|
| Jobs to analyze | 85 |
| AI models used | 6 |
| **Total API calls** | **85 × 6 = 510** |

### Token usage per request (Estimated)

| Type | Tokens | Description |
|------|--------|-------------|
| System prompt | ~50 | The instruction we give the AI |
| Job input | ~10 | "Job:\nAccountant" |
| Response output | ~150-300 | The structured JSON response |
| **Total per request** | **~250-400 tokens** |

### Cost per model (Approximate)

Prices vary by model and provider. These are **estimates** based on OpenRouter pricing (as of model execution time in 2026):

| Model | Input $/1M tokens | Output $/1M tokens | Est. Cost (510 calls) |
|-------|-------------------|--------------------|-----------------------|
| GPT-5 | $1.25 | $10.00 | ~$1.50 - $2.00 |
| Claude 4.5 Sonnet | $3.00 | $15.00 | ~$1.00 - $2.50 |
| Gemini 2.5 Pro | $1.25 | $10.00 | ~$1.50 - $2.00 |
| Gemini 3 Flash | $0.50 | $3.00 | ~$0.40 - $0.60 |
| Grok 4 | $3.00 | $15.00 | ~$1.00 - $2.50 |
| Cohere Command | $2.50 | $10.00 | ~$0.80 - $1.50 |

### Total estimated cost

| Scenario | Cost |
|----------|------|
| **All 6 models, 85 jobs** | **~$8 - $11** |
| Only cheap models (Gemini Flash) | ~$0.50 |
| Only expensive models (GPT-5, Claude) | ~$3 - $5 |

### Cost formula

```
Total Cost = (Input Tokens × Input Price) + (Output Tokens × Output Price)

For 510 calls with ~300 tokens average:
Total Tokens ≈ 510 × 300 = 153,000 tokens per model
```

> ⚠️ **Note:** Prices change frequently! Check [OpenRouter pricing](https://openrouter.ai/models) or individual provider websites for current rates.

---

## 🏗️ Installation step by step

### Step 1: Install UV

UV is a package manager for Python projects. Install it following the instructions at:

https://docs.astral.sh/uv/getting-started/installation/

### Step 2: Prepare the project

1. Navigate to the project folder:

```bash
cd path/to/ai_organizational_changes
```

2. Install all required dependencies:

```bash
uv sync
```

✅ Done! Everything is now installed.

---

## 🔑 Setting up API keys

API keys are like passwords that allow the program to communicate with AI services.

### What you need (at least one of these):

| Service | Website | What for? |
|---------|---------|-----------|
| **OpenRouter** | https://openrouter.ai | Access to many AI models (GPT-5, Claude, Gemini...) |
| **Cohere** | https://cohere.com | Specialized AI provider |
| **Logfire** | https://logfire.pydantic.dev | For monitoring (optional) |

### How to set up the keys:

1. Create a new file named `.env` in the project folder
2. Write the following (replace with your actual keys):

```
OPENROUTER_API_KEY=your_key_here
COHERE_API_KEY=your_key_here
LOGFIRE_TOKEN=your_token_here
```

> ⚠️ **IMPORTANT:** Never share your `.env` file with anyone! These are your secret passwords!

---

## 📝 Adding jobs

Jobs are listed in the `jobs.txt` file.

### How it works:

- Each line = one job
- One job per line
- Write the job name

### Example (jobs.txt):

```
Accountant
Secretary
Programmer
Web Designer
Sales Representative
```

---

## ▶️ Running the program

1. Navigate to the project folder:

```bash
cd path/to/ai_organizational_changes
```

2. Start the program:

```bash
uv run python -m ai_organizational_changes.main
```

### What happens now?

1. The program reads all jobs from `jobs.txt`
2. It asks different AI models (GPT-5, Claude, Gemini, etc.)
3. Each model analyzes every job
4. The results are saved

**⏱️ This takes a while!** The more jobs and models, the longer it takes. This process may take several minutes to complete.

---

## 📊 Viewing results

After the run, you'll find the results in the `results/` folder:

```
results/
├── openai_gpt-5_20260117_130000.json      ← JSON for programmers
├── openai_gpt-5_20260117_130000.xlsx      ← Excel for citizen users
├── anthropic_claude-4.5_20260117_130100.json
├── anthropic_claude-4.5_20260117_130100.xlsx
└── ... (etc. for each model)
```

### Opening the excel file:

Open the `.xlsx` files with Excel. The output will display:

| Job | genai_impact | skills | explanation |
|-----|--------------|--------|-------------|
| Accountant | likely_augmented_with_ai | ["Data entry", "Report creation"] | The accountant will work together with AI... |

### Impact types explained:

| Value | Meaning | Emoji |
|-------|---------|-------|
| `likely_automated_by_ai` | Job will probably be replaced by AI | 🔴 |
| `likely_augmented_with_ai` | Human + AI will work together | 🟡 |
| `likely_human_only` | Job stays human | 🟢 |

---

## 🔧 Changing models (For advanced users)

If you want to test other AI models, open the file:
`src/ai_organizational_changes/main.py`

In lines 23-30 you'll find the list of models:

```python
MODELS: list[str] = [
    "openai/gpt-5",
    "anthropic/claude-4.5-sonnet",
    "google/gemini-3-flash-preview",
    "google/gemini-2.5-pro",
    "x-ai/grok-4",
    "command-a-reasoning-08-2025",
]
```

Delete or add lines as needed. Search on https://openrouter.ai/models for available models.

---

## ❓ Common problems

### "API Key not found"
→ Did you create the `.env` file? Is the correct key in there?

### "Rate Limit" / "429 Error"
→ You sent too many requests. Wait a few minutes and try again.

### "uv: command not found"
→ UV wasn't installed correctly. Go back to Step 1.

### Nothing happens at all
→ Check if `jobs.txt` exists and has jobs in it.

---

## 📁 Project structure

```
ai_organizational_changes/
├── 📄 jobs.txt                 ← Your list of jobs
├── 📄 .env                     ← Your secret API keys
├── 📁 results/                 ← This is where results go
└── 📁 src/
    └── 📁 ai_organizational_changes/
        ├── main.py             ← The main program
        ├── model.py            ← How results look
        └── init_model.py       ← Connection to AI services
```

---

## 🎯 Summary

1. **Install UV** → `irm https://astral.sh/uv/install.ps1 | iex`
2. **Install dependencies** → `uv sync`
3. **Save API keys in `.env`**
4. **Add jobs to `jobs.txt`**
5. **Start the program** → `uv run python -m ai_organizational_changes.main`
6. **View results in `results/`**

**The program is now ready to generate AI predictions for jobs.**
