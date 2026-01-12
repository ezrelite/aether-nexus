# ⚡ AETHER: UNIFIED AI AGENT (v2.0)
> *A self-correcting, autonomous intelligence running locally.*

Aether is a modular AI agent designed for **Resilience, Autonomy, and Local Intelligence**. It combines high-speed cloud inference (Groq) with local "hands" (OS Control) and "memory" (RAG/JSON).

## 🌟 Standout Features

### 1. 🧠 Adaptable Brain (Hybrid Intelligence)
*   **Dual Engine**: Automatically switches between **Llama 3 70B** (Deep Thinker) and **Llama 3 8B** (Fast/Unlimited) based on user preference or API rate limits.
*   **Self-Healing**: If the heavy model hits a Rate Limit (429), Aether *instantly* falls back to the 8B model to keep working without interruption.

### 2. 📚 Deep Brain (RAG & Knowledge)
*   **Local Ingestion**: "Reads" PDF and Text files from your Desktop, Downloads, or Documents.
*   **Semantic Search**: Uses `ChromaDB` + `all-MiniLM-L6-v2` to understand context, not just keywords.
*   **Smart Discovery**: You don't need full paths. Just ask: *"Read secret_plan.txt"*, and it finds it.

### 3. 🔴 Red Team Mode (Adversarial Logic)
*   **Critical Thinking**: Triggers a 3-step internal debate before answering complex queries:
    1.  **Builder**: Proposes a plan.
    2.  **Destroyer**: Ruthlessly critiques the plan for flaws.
    3.  **Refiner**: Pivots to a superior, battle-tested solution.

### 4. 🦾 Autonomous "Hands"
*   **Self-Correction**: If it hallucinates a path or hits an error, it retries with new logic (e.g., Fuzzy Path Repair).
*   **Tool Chaining**: Can plan multi-step workflows (e.g., "Search web -> Summarize -> Save to Desktop").
*   **Desktop Control**: Can `SAVE_FILE`, `OPEN_APP` (Chrome, Notepad), and `LIST_FILES`.

### 5. 💾 Long-Term Memory
*   **Persistence**: Remembers facts across sessions via `memory.json`.
*   **Context Aware**: Injects your preferences into every new conversation.

## 🚀 Usage
```bash
streamlit run aether_run.py
```
**Quick Commands:**
*   *"Read the report on my desktop."*
*   *"Critique my business idea."* (Red Team)
*   *"Research Quantum Physics and save a summary."*

## 🏗️ Architecture
*   **`src/brain.py`**: LLM & Red Team Logic.
*   **`src/knowledge.py`**: Vector DB & RAG.
*   **`src/tools.py`**: OS & Web Tools.
*   **`aether_run.py`**: UI & System Prompt.
