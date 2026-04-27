# Zettelkasten Note Taker (ZNT)

ZNT is a **"Vitamin-Boosted Link & Idea Saver"** designed for humans to build a Second Brain and for AI agents to participate in the process via an MCP (Model Context Protocol) adapter.

## 🚀 Features

- **Markdown Editor:** Full-featured writing environment for your thoughts.
- **D3.js Graph View:** Interactive, physics-based visualization of your notes and their connections.
- **MCP Server:** A standalone bridge that allows AI agents to ingest links, create connected notes, and update relationships in your graph.
- **Privacy First:** Notes are stored locally as standard `.md` files in a flat-file structure.
- **Dockerized:** Easy deployment with one command.

## 🛠 Tech Stack

- **Backend:** FastAPI (Python 3.11) + SQLAlchemy + SQLite.
- **Frontend:** Vite + React + D3.js.
- **Agentic Adapter:** FastMCP (Python).
- **Orchestration:** Docker / OrbStack.

## 📦 Quick Start

### Prerequisites
- Docker and Docker Compose (OrbStack recommended for macOS).

### Launching the Application
1. Clone the repository:
   ```bash
   git clone https://github.com/diegoeguz90/zettelkasten-note-taker.git
   cd zettelkasten-note-taker
   ```

2. Start the services:
   ```bash
   docker-compose up -d --build
   ```

3. Open your browser:
   - **Frontend Dashboard:** [http://localhost:8002](http://localhost:8002)
   - **Backend API:** [http://localhost:8003/docs](http://localhost:8003/docs)

## 🤖 AI Agent Integration (MCP)

ZNT exposes an MCP server that provides tools for agents:

- `ingest_link`: Saves a URL as a new note.
- `create_connected_note`: Writes a note and links it to existing ones.
- `create_connection`: Defines a relationship between two nodes.

To use it, obtain your **MCP API Key** from the top right corner of the web dashboard.

## 📁 Directory Structure

```text
zettelkasten-note-taker/
├── backend/            # FastAPI Backend & SQLite DB
│   ├── app/            # Application logic
│   └── storage/        # Notes (.md) and DB storage
├── frontend/           # Vite + React Dashboard
├── mcp_server/         # FastMCP Agent Adapter
└── docker-compose.yml  # Orchestration
```

## 📝 License
MIT
