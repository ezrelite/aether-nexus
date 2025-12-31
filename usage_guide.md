# 📘 AETHER Nexus: Operator's Manual

## 🚀 Quick Start (The "Golden Path")

To ensure the system works perfectly every time, follow this exact startup sequence.

### 1. Start the Backend (The Cortex)
This must always run first. It initializes the database (Memory) and the AI Brain.
1.  Open **Terminal 1**.
2.  Navigate to the project folder:
    ```powershell
    cd aether-core
    ```
3.  Run the engine:
    ```powershell
    python run.py
    ```
    *Wait until you see:* `INFO: Application startup complete.`

### 2. Start the Frontend (Mission Control)
1.  Open **Terminal 2**.
2.  Navigate to the project folder:
    ```powershell
    cd aether-core
    ```
3.  Launch the dashboard:
    ```powershell
    streamlit run src/frontend/dashboard.py
    ```
    *This will automatically open your web browser to `http://localhost:8501`.*

---

## 🎮 How to Execute Missions

### The Interface
*   **Intent Box**: This is where you talk to the AI. Be specific.
*   **Autonomy Level**:
    *   **Low (Safe Mode)**: 🛡️ The AI can READ files but **CANNOT** write files, delete files, or run terminal commands. Use this for research/planning.
    *   **High (God Mode)**: ⚡ The AI has **FULL PERMISSION** to create files, overwrite code, and execute shell commands. Use this for building software or fixing system issues.

### Example Missions
**Safe (Low Autonomy):**
> "Research the history of the Python language and outline the key versions."

**Active (High Autonomy):**
> "Create a python script named 'hello_nexus.py' that prints the current system time, then execute it."

---

## 🔧 Troubleshooting & Stability

### If the API "Hangs" or Fails
Google's Free Tier has strict limits. If the AI stops successfully:
1.  **Check Terminal 1**: Is it printing `Waiting 45 seconds...`? If so, just wait. It is handling the rate limit for you.
2.  **Mock Fallback**: If the API is totally unreachable, the system will auto-switch to "Demo Mode" and return a pre-scripted plan. This proves the system is healthy, even if the Brain is temporarily offline.

### If the UI is Blank
1.  Refresh the browser (`Ctrl+R` / `F5`).
2.  Ensure Terminal 1 is still running without errors.

### "Repository Not Found" Error
If verification fails, ensure you are in the `aether-core` directory, not the parent `aether` directory.

---

## 📂 Project Structure
*   `run.py`: The entry point for the backend.
*   `src/nexus/planner.py`: The "Brain". Handles the Google Gemini connection and Retry Logic.
*   `src/nexus/engine.py`: The "Coordinator". Manages workers and Safety Checks.
*   `src/workers/`: The tools available to the AI (Architect for files, Navigator for search).
