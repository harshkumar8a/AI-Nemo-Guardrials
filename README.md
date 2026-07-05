# AI-Nemo-Guardrails Project

## 🧮 Secure Math Assistant (FastAPI + LangGraph + NeMo Guardrails)

A high-performance, asynchronous single-page chatbot designed to safely and accurately evaluate mathematical expressions. The application uses **NeMo Guardrails** combined with **Groq (Llama 3)** to intercept and block conversational or off-topic prompts before routing clean, verified math equations into an isolated **LangGraph** execution engine.

---

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)
![LangChain](https://img.shields.io/badge/LangChain-Framework-blueviolet)
![Groq](https://img.shields.io/badge/Groq-LLM-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Memory-blue)

---


## 🎥 Demo



## 🚀 Key Features

* **Dual-Layer Defense:** Combines NeMo Guardrails (`.co` flow logic) with automated validation scripts to completely block conversational text injections (e.g., *"What is Python?"*).
* **Deterministic Math Engine:** Bypasses LLM math hallucinations entirely by dynamically parsing and evaluating equations safely inside a sandboxed environment.
* **State Machine Orchestration:** Uses `LangGraph` to manage conditional app states across input verification and processing steps.
* **Async-First Design:** Built on FastAPI using non-blocking asynchronous clients (`.ainvoke` and `generate_async`) for fast response times.
* **Clean Single-Page UI:** Minimalist HTML/CSS/JavaScript interface featuring custom-styled alert statuses for blocked inputs.

---

## 📂 Project Architecture

```text
nemo-langgraph-fastapi/
│
├── config/
│   ├── config.yml           # Core guardrail configurations & engine maps
│   └── general.co           # Colang safety flows for off-topic filtering
│
├── static/
│   ├── index.html           # Main frontend interface page
│   ├── style.css            # Chatbot styling sheet
│   └── script.js            # Asynchronous fetch client logic
│
├── main.py                  # FastAPI server, LangGraph setup, & provider registrations
└── README.md                # Project documentation
```

---



## 🛠️ Step-by-Step Installation

### 1. Clone the Project & Enter Directory
```bash
git clone https://github.com/harshkumar8a/AI-Nemo-Guardrials
cd nemo-langgraph-fastapi
uv init
uv sync
.venv/Scripts/Activate
```

### 2. Install Required Dependencies
Ensure your environment manager is active, then execute:
```bash
pip install fastapi uvicorn nemoguardrails langgraph langchain-groq python-dotenv
```

### 3. Add Your Environment Keys
Create a `.env` file in your root folder or configure your terminal environment directly:
```bash
# Groq api key
GROQ_API_KEY = "groq_api_key"

# Ollama (initilze this download the local ollama)
OLLAMA_BASE_URL=http://localhost:11434
# ollama pull llama3.2:latest 
OLLAMA_MODEL=llama3.2:latest 

# LangSmith
LANGCHAIN_API_KEY="langsmit_api_key"
LANGCHAIN_PROJECT="AI-NEMOGUARDRAIL"
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

---

## 💻 Running the Application

Launch the server using your Python launcher tool (`uv` runtime or regular Python environment):

```bash
uv run python -m main
# OR
python main.py
```

Once initialized, open your browser and navigate to the base address:
🔗 **`http://127.0.0`**

---

## 📸 Screenshots





## 🧪 Testing Scenarios

| Prompt Example | Intended System Action | Frontend Visual Feedback |
| :--- | :--- | :--- |
| `(15 * 4) + 100` | **Allowed.** Calculation processed deterministically. | Gray bubble showing: `The result is 160.` |
| `What is Python?` | **Blocked.** Intercepted by input guardrails. | Red bubble showing: `I am a specialized math assistant...` |
| `Tell me a joke` | **Blocked.** Intercepted by input guardrails. | Red bubble showing: `I am a specialized math assistant...` |
| `50 / 0` | **Handled.** Caught safely by processing engine. | Gray bubble showing: `Error: Division by zero is undefined.` |

---

# 🎯 Roadmap

## Completed

- [x] Mathmatical Calculation
- [x] Groq Integration
- [x] AI Nemo- Guardrail
- [x] FastAPI Backend

## Coming Soon

- [ ] Multi-language Support
- [ ] User Authentication
- [ ] Docker Compose
- [ ] CI/CD Pipeline
- [ ] Unit Testing
- [ ] AI Evals
- [ ] Monitoring

---


# 📌 Key Learnings

This project provided practical experience in:

* Most work on the async python
* Uses the nemo-gurdrail for security
* Implement a Langsmith 


---

# 🤝 Contributing

Contributions, improvements, and suggestions are welcome.

Feel free to open issues or submit pull requests.

---


# 👨‍💻 Author

Developed by [Harsh Kumar] 

**LinkedIn**: [Link](https://www.linkedin.com/in/harshkumar-8h/)

AI Engineer | Generative AI | AI Guardrail | LLM Applications
