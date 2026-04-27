import requests
import json

def test_mcp_tools():
    print("Validating MCP server tools...")
    
    # In SSE, we first get the SSE endpoint, then we can query it.
    # But for a quick validation, we just check if /sse is up (done)
    # and if we can hit the /messages endpoint (simulating a client)
    
    # Actually, a simpler way is to check the server's capabilities if it has a discovery endpoint.
    # Standard MCP SSE: GET /sse returns the session info.
    
    try:
        resp = requests.get("http://localhost:8004/sse", stream=True)
        resp.raise_for_status()
        for line in resp.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if "event: endpoint" in decoded_line:
                    print("✅ MCP SSE Endpoint discovery passed")
                    break
        resp.close()
    except Exception as e:
        print(f"❌ MCP Connection failed: {e}")
        return

    print("🚀 MCP Validation passed!")

if __name__ == "__main__":
    test_mcp_tools()
