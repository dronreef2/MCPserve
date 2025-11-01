#!/usr/bin/env python3
"""Script de teste para o servidor MCP."""

import asyncio
import httpx
import json

async def test_server():
    """Testa o servidor MCP."""
    async with httpx.AsyncClient() as client:
        # Testa tools/list
        response = await client.post(
            "http://localhost:8001/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list"
            }
        )
        print("Tools/list response:")
        print(json.dumps(response.json(), indent=2))

        # Testa ping
        response = await client.post(
            "http://localhost:8001/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "ping",
                    "arguments": {}
                }
            }
        )
        print("\nPing response:")
        print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    # Inicia o servidor em background
    import subprocess
    import time
    server = subprocess.Popen(["python", "-m", "enhanced_mcp_server.main", "--http"])
    time.sleep(2)  # Espera o servidor iniciar

    try:
        asyncio.run(test_server())
    finally:
        server.terminate()
        server.wait()