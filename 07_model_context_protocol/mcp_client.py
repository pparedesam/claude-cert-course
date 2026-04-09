
# mcp_client.py
# Cliente MCP que usa Claude para interactuar con el servidor

import asyncio
import json
import os
from dotenv import load_dotenv
import anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()
claude = anthropic.Anthropic()

async def run_mcp_client():
    # Conectar al servidor MCP
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_math_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1. Listar herramientas disponibles
            tools_result = await session.list_tools()
            print("Herramientas disponibles:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # 2. Convertir herramientas MCP a formato Anthropic
            anthropic_tools = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                }
                for tool in tools_result.tools
            ]

            # 3. Bucle de conversación con herramientas
            messages = [{
                "role": "user",
                "content": "¿Cuánto es sqrt(256) + 37? Y también dime si 97 es primo."
            }]

            while True:
                response = claude.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=1024,
                    tools=anthropic_tools,
                    messages=messages
                )

                if response.stop_reason == "end_turn":
                    print("
Claude:", response.content[0].text)
                    break

                if response.stop_reason == "tool_use":
                    messages.append({"role": "assistant", "content": response.content})
                    tool_results = []

                    for block in response.content:
                        if block.type == "tool_use":
                            print(f"Usando: {block.name}({block.input})")
                            # Llamar herramienta en el servidor MCP
                            result = await session.call_tool(block.name, block.input)
                            print(f"Resultado: {result.content[0].text}")
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result.content[0].text
                            })

                    messages.append({"role": "user", "content": tool_results})

if __name__ == "__main__":
    asyncio.run(run_mcp_client())
