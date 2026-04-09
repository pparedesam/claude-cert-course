
# mcp_math_server.py
# Servidor MCP con herramientas matemáticas

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
import math
import json

app = Server("math-server")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """Lista todas las herramientas disponibles."""
    return [
        types.Tool(
            name="calcular",
            description="Realiza cálculos matemáticos",
            inputSchema={
                "type": "object",
                "properties": {
                    "expresion": {
                        "type": "string",
                        "description": "Expresión matemática a evaluar (ej: 2+2, sqrt(16))"
                    }
                },
                "required": ["expresion"]
            }
        ),
        types.Tool(
            name="es_primo",
            description="Verifica si un número es primo",
            inputSchema={
                "type": "object",
                "properties": {
                    "numero": {"type": "integer", "description": "Número a verificar"}
                },
                "required": ["numero"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Ejecuta la herramienta solicitada."""
    if name == "calcular":
        try:
            # Evaluar expresión de forma segura
            allowed_names = {k: v for k, v in math.__dict__.items() 
                           if not k.startswith('_')}
            result = eval(arguments["expresion"], {"__builtins__": {}}, allowed_names)
            return [types.TextContent(type="text", text=str(result))]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {e}")]

    elif name == "es_primo":
        n = arguments["numero"]
        if n < 2:
            resultado = False
        else:
            resultado = all(n % i != 0 for i in range(2, int(n**0.5) + 1))
        return [types.TextContent(type="text", 
                                   text=f"{n} {'ES' if resultado else 'NO ES'} primo")]

@app.list_resources()
async def list_resources() -> list[types.Resource]:
    """Lista recursos disponibles."""
    return [
        types.Resource(
            uri="math://constants",
            name="Constantes Matemáticas",
            description="Constantes matemáticas importantes",
            mimeType="application/json"
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    """Lee un recurso por URI."""
    if str(uri) == "math://constants":
        constants = {
            "pi": math.pi,
            "e": math.e,
            "tau": math.tau,
            "inf": float('inf')
        }
        return json.dumps(constants, indent=2)
    raise ValueError(f"Recurso no encontrado: {uri}")

@app.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    """Lista prompts disponibles."""
    return [
        types.Prompt(
            name="resolver_problema",
            description="Template para resolver problemas matemáticos paso a paso",
            arguments=[
                types.PromptArgument(
                    name="problema",
                    description="El problema matemático a resolver",
                    required=True
                )
            ]
        )
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: dict) -> types.GetPromptResult:
    """Retorna un prompt por nombre."""
    if name == "resolver_problema":
        problema = arguments.get("problema", "")
        return types.GetPromptResult(
            description="Resolver problema paso a paso",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"""Resuelve este problema matemático paso a paso:

Problema: {problema}

Instrucciones:
1. Identifica los datos del problema
2. Determina las operaciones necesarias
3. Resuelve paso a paso
4. Verifica el resultado
5. Presenta la respuesta final claramente"""
                    )
                )
            ]
        )

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
