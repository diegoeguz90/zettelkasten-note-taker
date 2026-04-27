import os
import requests
from mcp.server.fastmcp import FastMCP

# Setup FastMCP
mcp = FastMCP("ZNT_Agentic_Adapter")

ZNT_API_URL = os.getenv("ZNT_API_URL", "http://localhost:8000/api")
ZNT_API_KEY = os.getenv("ZNT_API_KEY", "")

headers = {
    "Authorization": f"Bearer {ZNT_API_KEY}"
}

@mcp.tool()
def ingest_link(url: str, title: str, summary: str) -> str:
    """Agent submits a URL. Backend saves it as a new note with the URL in its content."""
    content = f"# {title}\n\n**URL:** {url}\n\n**Summary:** {summary}"
    
    response = requests.post(
        f"{ZNT_API_URL}/notes/",
        json={"title": title, "content": content, "connected_to_note_ids": []},
        headers=headers
    )
    if response.status_code == 200:
        return f"Link ingested successfully. Note ID: {response.json().get('id')}"
    return f"Failed to ingest link: {response.text}"

@mcp.tool()
def create_connected_note(title: str, content: str, connected_to_note_ids: list[str]) -> str:
    """Agent writes a new note and automatically wires up connections to existing target IDs."""
    response = requests.post(
        f"{ZNT_API_URL}/notes/",
        json={
            "title": title, 
            "content": content, 
            "connected_to_note_ids": connected_to_note_ids
        },
        headers=headers
    )
    if response.status_code == 200:
        return f"Note created and connected. Note ID: {response.json().get('id')}"
    return f"Failed to create note: {response.text}"

@mcp.tool()
def create_connection(source_id: str, target_id: str) -> str:
    """Agent explicitly defines a connection between two existing notes."""
    response = requests.post(
        f"{ZNT_API_URL}/graph/connections",
        json={"source_id": source_id, "target_id": target_id},
        headers=headers
    )
    if response.status_code == 200:
        return f"Connection created successfully."
    return f"Failed to create connection: {response.text}"

import uvicorn

if __name__ == "__main__":
    # Use SSE transport for persistent background execution in Docker
    # The MCP app is available via mcp.sse_app for FastMCP.
    uvicorn.run(mcp.sse_app, host="0.0.0.0", port=8000)
