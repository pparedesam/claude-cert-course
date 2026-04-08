# Módulo 08 — Claude Code y Computer Use

## Claude Code

Claude Code es una CLI (interfaz de línea de comandos) que trae las capacidades de Claude directamente al terminal, optimizada para tareas de programación.

### Instalación

```bash
# Requiere Node.js 18+
npm install -g @anthropic-ai/claude-code

# Verificar instalación
claude --version
```

### Uso básico

```bash
# Iniciar sesión interactiva
claude

# Modo no-interactivo (ideal para scripts)
claude -p "refactoriza este archivo para mejor legibilidad" --files src/main.py

# Con aprobación automática (precaución)
claude --dangerously-skip-permissions -p "añade tests unitarios"
```

### Comandos principales en sesión

| Comando | Descripción |
|---------|-------------|
| `/help` | Ver ayuda |
| `/clear` | Limpiar contexto |
| `/compact` | Compactar conversación larga |
| `/memory` | Ver y editar memoria de Claude |
| `/cost` | Ver tokens usados |
| `/exit` | Salir |

### MCP con Claude Code

Añade servidores MCP en `~/.claude.json`:

```json
{
  "mcpServers": {
    "math-server": {
      "command": "python",
      "args": ["/ruta/al/mcp_math_server.py"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
    }
  }
}
```

### Mejores prácticas

1. **CLAUDE.md**: Crea un archivo `CLAUDE.md` en tu proyecto con:
   - Contexto del proyecto
   - Convenciones de código
   - Comandos útiles de build/test

2. **Permisos**: Usa `--allowedTools` para limitar qué puede hacer Claude
3. **Git**: Claude Code se integra con git para mostrar diff antes de cambios

### Computer Use

Computer Use permite a Claude controlar directamente un ordenador:
- Mover el ratón
- Hacer clic
- Escribir texto
- Hacer capturas de pantalla

```python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    tools=[{"type": "computer_20241022", "name": "computer", 
            "display_width_px": 1024, "display_height_px": 768}],
    messages=[{"role": "user", "content": "Abre un navegador y ve a anthropic.com"}],
    betas=["computer-use-2024-10-22"]
)
```

> ⚠️ Computer Use está en beta. Usar con precaución en entornos de producción.
