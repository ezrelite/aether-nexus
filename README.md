# AETHER: Autonomous Executive Task & High-Efficiency Router

**AETHER** is a Cognitive Operating Layer (COL) that transforms a Docker container into an autonomous multi-agent workstation.

## Core Concept
Provide an open-source "Company-in-a-Box" where a "Nexus" brain orchestrates specialized workers (Navigator, Architect, Analyst) to execute complex goals via the Model Context Protocol (MCP).

## Key Differentiator
**Verifiable Autonomy**: Every step generates a structured artifact (JSON/Log) to solve the black-box problem.

## Architecture
- **Nexus**: Recursive Planner (The Brain)
- **Workers**: Specialized Agents (The Hands)
    - **Navigator**: Web Search & Browsing
    - **Architect**: File System & Code Execution
    - **Analyst**: Data Synthesis & Reporting
- **Cortex**: Redis Memory System

## Quick Start
1. Copy `.env.example` to `.env` and set your `GOOGLE_API_KEY`.
2. Install dependencies:
   ```bash
   pip install -e .
   ```
3. Run the API:
   ```bash
   python run.py
   ```
4. Test with curl:
   ```bash
   curl -X POST "http://localhost:8000/v1/run" \
     -H "Content-Type: application/json" \
     -d '{"intent": "Create a file named demo.txt with content Hello Aether", "autonomy_level": "high"}'
   ```
5. Launch Mission Control (UI):
   ```bash
   streamlit run src/frontend/dashboard.py
   ```

## Docker Setup
1. Run `docker compose up --build`.
2. Access API at `http://localhost:8000`.
