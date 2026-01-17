# 🤖 Accompanying code repository for the paper "Generative AI's Impact on Organizational Design: An Analysis Based on Human-AI Collaboration"

## What does this program even do?

**In short:** This program asks AI models (like ChatGPT, Claude, etc.) which jobs might be affected by AI.

### 📚 Background

Artificial intelligence has been rapidly increasing in sophistication and impact, reinforcing discussions of its extensive potential to disrupt individual jobs and organizations. Through our investigation into the disruptive potential of generative artificial intelligence (genAI) on organizations, we don't just study genAI — **we also team up with it**.

We consolidated data from the **O*Net 2023 database** to create a list of **85 corporate knowledge worker roles** (and associated skill levels). Then, together with **five different genAI team members**, we assessed which roles genAI will automate or augment (human with AI) in the near future.

#### Coding Definitions

- 🔴 **Automated by AI** — Machines take over a human task completely
- 🟡 **Augmented with AI** — Humans collaborate closely with machines to perform a task
- 🟢 **Human-only** — The job remains performed by humans without AI involvement

> 📖 *Based on: Raisch, S., & Krakowski, S. (2021). Artificial Intelligence and Management: The Automation-Augmentation Paradox. Academy of Management Review, 46(1), 192–210. https://doi.org/10.5465/amr.2018.0072*

### An Example:
You give the program a list of jobs (e.g., "Accountant", "Secretary", "Programmer") and the AI tells you:
- 🔴 **Will be replaced by AI** - The job will probably disappear
- 🟡 **Will be supported by AI** - Humans will work together with AI
- 🟢 **Stays human** - The job doesn't need AI

---

## 🤔 Why Use LLMs for This? Are They Even Reliable?

A fair question: *"Can we trust AI to judge which jobs will be affected by AI?"*

Short answer: **Yes, and here's why.**

### The Problem with Human Coders

Traditional qualitative research uses human coders to categorize data. But humans have problems:

| Issue | Description |
|-------|-------------|
| 🧠 **Subjectivity** | Different researchers interpret the same data differently |
| 😴 **Fatigue** | Humans get tired and make more mistakes over time |
| 💭 **Bias** | Personal opinions and experiences influence coding decisions |
| 📊 **Inconsistency** | The same person might code differently on different days |

To combat this, researchers typically use **multiple coders** and measure **inter-rater reliability** — checking if different humans agree with each other.

### LLMs Are More Consistent Than Humans

Recent research has shown that Large Language Models actually **outperform humans** in consistency:

> **Tai et al. (2024)** emphasize the subjectivity of qualitative data coding due to human coder bias. To improve reliability, multiple coders are traditionally used.

> **Gilardi et al. (2023)** found that LLMs offer consistent performance in coding tasks, **outperforming human coders in consistency**. This suggests LLMs as a reliable alternative for qualitative data analysis.

### Why LLMs Work Well for This Task

| Advantage | Explanation |
|-----------|-------------|
| ✅ **Perfect consistency** | Same prompt + temperature 0 = same answer every time |
| ✅ **No fatigue** | Job #85 is coded with the same quality as Job #1 |
| ✅ **No personal bias** | LLMs don't have career anxieties about automation |
| ✅ **Multiple "coders"** | We use 5-6 different models as independent raters |
| ✅ **Transparent process** | The exact prompt and parameters are documented |

### But Wait — Isn't This Circular?

You might wonder: *"Using AI to predict AI's impact on jobs... isn't that biased?"*

**Actually, no.** Here's why:

1. **LLMs are trained on human knowledge** — they reflect collective human understanding of jobs and automation
2. **We use multiple models** — if GPT-5, Claude, and Gemini all agree, that's like having 5 expert coders agree
3. **Results are transparent** — you can see exactly what each model said and why
4. **It's a prediction, not a fact** — we're measuring AI's *assessment*, which is the research question itself

### The Meta-Twist 🌀

There's actually something beautiful here: **we're using human-AI collaboration to study human-AI collaboration**. The research method mirrors the research topic — AI and humans working together to understand how AI and humans will work together.

> 📖 *References:*
> - *Tai, R. H., Bentley, L. R., Xia, X., Sitt, J. M., Fankhauser, S. C., Chicas-Mosier, A. M., & Monteith, B. G. (2024). An Examination of the Use of Large Language Models to Aid Analysis of Textual Data. International Journal of Qualitative Methods, 23. https://doi.org/10.1177/16094069241231168*
> - *Gilardi, F., Alizadeh, M., & Kubli, M. (2023). ChatGPT outperforms crowd workers for text-annotation tasks. Proceedings of the National Academy of Sciences, 120(30), e2305016120. https://doi.org/10.1073/pnas.2305016120*

---

## 🧪 How This Works: Programmatic AI vs. "Chatting with ChatGPT"

This section explains **why we use code to talk to AI models** instead of just typing prompts into ChatGPT like a normal person.

### The Problem with Manual Prompting

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

### Our Solution: Programmatic Prompting

Instead of chatting, we write **code** that:

1. **Sends the exact same prompt** to every AI model
2. **Forces structured responses** (not free-form text)
3. **Logs everything** for reproducibility
4. **Processes hundreds of jobs automatically**

### How Our Prompt is Constructed

The prompt lives in `main.py` line 33:

```python
system_prompt = """Based on what you know, can you please read the following 
role and predict which roles are likely to be impacted by generative AI 
and which skills specifically for the role will be impacted by generative AI"""
```

This **system prompt** sets the AI's behavior. Then, for each job, we send:

```python
response = await agent.run(f"Job:\n{job}")
```

So if the job is "Accountant", the AI receives:
```
Job:
Accountant
```

### The Magic: Structured Output (No More Rambling!)

Here's where it gets interesting. In `model.py`, we define **exactly** what the AI must return:

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

### Why This Matters for Research

| Aspect | ChatGPT Website | Our Programmatic Approach |
|--------|-----------------|---------------------------|
| **Reproducibility** | ❌ Can't prove what you asked | ✅ Code is the proof |
| **Consistency** | ❌ Different phrasing = different results | ✅ Exact same prompt every time |
| **Scalability** | ❌ 425 manual queries? LOL | ✅ Runs overnight automatically |
| **Structure** | ❌ Free-form text, must parse by hand | ✅ JSON, directly into Excel |
| **Temperature control** | ❌ Hidden, changes randomly | ✅ Set to 0 for determinism |
| **Multi-model comparison** | ❌ Switch tabs, retype everything | ✅ Loop through 5 models automatically |
| **Rate limit handling** | ❌ "Try again later" 😤 | ✅ Automatic retry with backoff |
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

### TL;DR: Why Code > ChatGPT for Research

🎯 **Precision**: We control exactly what we ask  
🔁 **Reproducibility**: Anyone can run the same code, get same results  
📊 **Structure**: Data goes straight into analysis tools  
⚡ **Scale**: 425 API calls while you sleep  
🔬 **Science**: This is how serious AI research works

---

## 💰 Cost Calculation: What Does This Cost?

Running AI models via API costs money. Here's a breakdown of what to expect.

### Number of API Requests

| Component | Count |
|-----------|-------|
| Jobs to analyze | 85 |
| AI models used | 6 |
| **Total API calls** | **85 × 6 = 510** |

### Token Usage Per Request (Estimated)

| Type | Tokens | Description |
|------|--------|-------------|
| System prompt | ~50 | The instruction we give the AI |
| Job input | ~10 | "Job:\nAccountant" |
| Response output | ~150-300 | The structured JSON response |
| **Total per request** | **~250-400 tokens** |

### Cost Per Model (Approximate)

Prices vary by model and provider. These are **estimates** based on OpenRouter pricing (as of 2024):

| Model | Input $/1M tokens | Output $/1M tokens | Est. Cost (510 calls) |
|-------|-------------------|--------------------|-----------------------|
| GPT-5 | $5.00 | $15.00 | ~$1.50 - $3.00 |
| Claude 4.5 Sonnet | $3.00 | $15.00 | ~$1.00 - $2.50 |
| Gemini 2.5 Pro | $1.25 | $5.00 | ~$0.40 - $0.80 |
| Gemini 3 Flash | $0.10 | $0.40 | ~$0.03 - $0.06 |
| Grok 4 | $3.00 | $15.00 | ~$1.00 - $2.50 |
| Cohere Command | $2.50 | $10.00 | ~$0.80 - $1.50 |

### Total Estimated Cost

| Scenario | Cost |
|----------|------|
| **All 6 models, 85 jobs** | **~$5 - $12** |
| Only cheap models (Gemini Flash) | ~$0.05 |
| Only expensive models (GPT-5, Claude) | ~$3 - $6 |

### Cost Formula

```
Total Cost = (Input Tokens × Input Price) + (Output Tokens × Output Price)

For 510 calls with ~300 tokens average:
Total Tokens ≈ 510 × 300 = 153,000 tokens per model
```

### Tips to Reduce Costs

- 🧪 **Test with one model first** before running all 6
- 💨 **Use Gemini Flash** for testing — it's nearly free
- 📉 **Reduce job list** — test with 10 jobs before running 85
- 🔁 **Don't re-run unnecessarily** — results are saved to `results/`

> ⚠️ **Note:** Prices change frequently! Check [OpenRouter pricing](https://openrouter.ai/models) or individual provider websites for current rates.

---

## 🏗️ Installation Step by Step

### Step 1: Install UV

UV is a program that installs other programs (like an app store for developers).

1. Open **PowerShell** (Press Windows key, type "PowerShell", press Enter)
2. Copy this command and press Enter:

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

3. Close PowerShell and open it again

### Step 2: Prepare the Project

1. Open PowerShell
2. Navigate to the project folder:

```powershell
cd "D:\Programming Projects\ai_organizational_changes"
```

3. Install all required dependencies:

```powershell
uv sync
```

✅ Done! Everything is now installed.

---

## 🔑 Setting Up API Keys

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

## 📝 Adding Jobs

Jobs are listed in the `jobs.txt` file.

### How it works:

- Each line = one job
- One job per line
- Just write the job name

### Example (jobs.txt):

```
Accountant
Secretary
Programmer
Web Designer
Sales Representative
```

---

## ▶️ Running the Program

1. Open PowerShell
2. Navigate to the project folder:

```powershell
cd "D:\Programming Projects\ai_organizational_changes"
```

3. Start the program:

```powershell
uv run python -m ai_organizational_changes.main
```

### What happens now?

1. The program reads all jobs from `jobs.txt`
2. It asks different AI models (GPT-5, Claude, Gemini, etc.)
3. Each model analyzes every job
4. The results are saved

**⏱️ This takes a while!** The more jobs and models, the longer it takes. Go grab a coffee ☕

---

## 📊 Viewing Results

After the run, you'll find the results in the `results/` folder:

```
results/
├── openai_gpt-5_20260117_130000.json      ← For programmers
├── openai_gpt-5_20260117_130000.xlsx      ← For Excel fans
├── anthropic_claude-4.5_20260117_130100.json
├── anthropic_claude-4.5_20260117_130100.xlsx
└── ... (etc. for each model)
```

### Opening the Excel file:

You can simply open the `.xlsx` files with Excel. You'll see:

| Job | genai_impact | skills | explanation |
|-----|--------------|--------|-------------|
| Accountant | likely_augmented_with_ai | ["Data entry", "Report creation"] | The accountant will work together with AI... |

### Impact Types Explained:

| Value | Meaning | Emoji |
|-------|---------|-------|
| `likely_automated_by_ai` | Job will probably be replaced by AI | 🔴 |
| `likely_augmented_with_ai` | Human + AI will work together | 🟡 |
| `likely_human_only` | Job stays human | 🟢 |

---

## 🔧 Changing Models (For Advanced Users)

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

You can delete or add lines. Search on https://openrouter.ai/models for available models.

---

## ❓ Common Problems

### "API Key not found"
→ Did you create the `.env` file? Is the correct key in there?

### "Rate Limit" / "429 Error"
→ You sent too many requests. Wait a few minutes and try again.

### "uv: command not found"
→ UV wasn't installed correctly. Go back to Step 1.

### Nothing happens at all
→ Check if `jobs.txt` exists and has jobs in it.

---

## 📁 Project Structure

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

**That's it! You can now make AI predictions for jobs! 🎉**
