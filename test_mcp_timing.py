#!/usr/bin/env python3
"""Script de teste para diagnosticar problemas de sincronização MCP."""

import asyncio
import json
import sys
import os
from asyncio import subprocess

async def test_mcp_server():
    """Testa o servidor MCP simulando comunicação cliente."""
    print("🚀 Iniciando teste do servidor MCP...")

    # Inicia o servidor em background
    print("📡 Iniciando servidor MCP...")
    env = os.environ.copy()
    env.update({
        'JINA_API_KEY': 'dummy_key_for_test',
        'GEMINI_API_KEY': 'dummy_key_for_test',
        'DEEPL_API_KEY': 'dummy_key_for_test',
        'REDIS_URL': 'redis://localhost:6379',
        'LOG_LEVEL': 'DEBUG',
        'PYTHONIOENCODING': 'utf-8'
    })

    try:
        # Inicia o processo do servidor
        process = await asyncio.create_subprocess_exec(
            sys.executable, '-m', 'enhanced_mcp_server.main',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )

        print("⏳ Aguardando servidor inicializar...")
        await asyncio.sleep(2)  # Aguarda inicialização

        # Verifica se há logs em stderr
        try:
            stderr_data = await asyncio.wait_for(process.stderr.read(1024), timeout=0.1)
            if stderr_data:
                print(f"📄 Logs em stderr: {stderr_data.decode().strip()}")
        except asyncio.TimeoutError:
            print("📄 Nenhum log em stderr ainda")

        # Testa initialize request
        print("📤 Enviando initialize request...")
        initialize_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        # Envia request
        request_json = json.dumps(initialize_request) + "\n"
        process.stdin.write(request_json.encode())
        await process.stdin.drain()

        # Lê resposta
        print("📥 Aguardando resposta do initialize...")
        try:
            response_data = await asyncio.wait_for(process.stdout.readline(), timeout=5.0)
            response_str = response_data.decode().strip()
            print(f"📄 Dados brutos recebidos: '{response_str}'")
            response = json.loads(response_str)
            print(f"✅ Resposta do initialize: {response}")
        except json.JSONDecodeError as e:
            print(f"❌ Erro de JSON: {e}")
            print(f"📄 Dados que causaram erro: '{response_str}'")
            raise

        # Testa tools/list request
        print("📤 Enviando tools/list request...")
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }

        request_json = json.dumps(tools_request) + "\n"
        process.stdin.write(request_json.encode())
        await process.stdin.drain()

        # Lê resposta
        print("📥 Aguardando resposta do tools/list...")
        response_data = await asyncio.wait_for(process.stdout.readline(), timeout=5.0)
        response = json.loads(response_data.decode().strip())

        print(f"✅ Resposta do tools/list: {response}")

        # Testa tools/call request
        print("📤 Enviando tools/call request...")
        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "fetch",
                "arguments": {
                    "url": "https://httpbin.org/get"
                }
            }
        }

        request_json = json.dumps(call_request) + "\n"
        process.stdin.write(request_json.encode())
        await process.stdin.drain()

        # Lê resposta
        print("📥 Aguardando resposta do tools/call...")
        response_data = await asyncio.wait_for(process.stdout.readline(), timeout=10.0)
        response = json.loads(response_data.decode().strip())

        print(f"✅ Resposta do tools/call: {response}")

    except asyncio.TimeoutError:
        print("❌ Timeout aguardando resposta do servidor")
        # Lê stderr para debug
        stderr_data = await process.stderr.read()
        print(f"Stderr: {stderr_data.decode()}")
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        # Lê stderr para debug
        try:
            stderr_data = await process.stderr.read()
            print(f"Stderr: {stderr_data.decode()}")
        except Exception:
            pass
    finally:
        # Termina o processo
        try:
            process.terminate()
            await asyncio.wait_for(process.wait(), timeout=5.0)
        except Exception:
            process.kill()
            await process.wait()

if __name__ == "__main__":
    asyncio.run(test_mcp_server())