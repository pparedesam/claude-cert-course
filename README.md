# Claude Certification Course

Repositorio con notebooks y ejercicios del curso de certificación oficial de Anthropic Claude.
Cubre desde el acceso básico a la API hasta agentes, RAG, MCP y uso avanzado de modelos.

---

## Estructura del Curso

| Modulo | Contenido |
|--------|-----------|
| `01_accessing_claude_api/` | Peticiones, conversaciones multi-turno, system prompts, temperatura, streaming y datos estructurados |
| `02_prompt_evaluation/` | Workflow de evaluacion, datasets de prueba, grading por modelo y por codigo |
| `03_prompt_engineering/` | Claridad, especificidad, XML tags y ejemplos |
| `04_tool_use/` | Tool functions, schemas, manejo de bloques, multi-turn con tools, text edit y web search |
| `05_rag_agentic_search/` | Chunking, embeddings, flujo RAG completo, BM25 y pipeline multi-index |
| `06_features_of_claude/` | Extended thinking, imagenes, PDFs, citations, prompt caching y Files API |
| `07_model_context_protocol/` | Clientes MCP, definicion de tools/resources/prompts, server inspector |
| `08_claude_code_computer_use/` | Claude Code en accion, integracion con servidores MCP |
| `09_agents_and_workflows/` | Paralelizacion, chaining, routing, agentes con tools |

---

## Configuracion rapida

### Opcion A — Script automatico (recomendado)

Funciona en macOS y Linux. Instala dependencias, crea el entorno virtual y registra el kernel en VSCode:

```bash
bash setup.sh
```

### Opcion B — Manual

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name=claude-course --display-name "Python (Claude Course)"
```

### API Key

```bash
cp .env.example .env
# Editar .env y agregar: ANTHROPIC_API_KEY=sk-ant-...
```

Obtener API key en: https://console.anthropic.com/

---

## Uso en VSCode

1. Abrir el proyecto en VSCode
2. En cada notebook, seleccionar el kernel **Python (Claude Course)** (esquina superior derecha)
3. Ejecutar las celdas con `Shift+Enter` comenzando desde la primera

---

## Modelos utilizados

| Modelo | Uso recomendado |
|--------|----------------|
| `claude-opus-4-5` | Tareas complejas, razonamiento avanzado |
| `claude-sonnet-4-5` | Uso general en el curso (balance costo/rendimiento) |
| `claude-haiku-3-5` | Tareas rapidas y de bajo costo |

---

## Requisitos

- Python 3.10 o superior
- Cuenta en Anthropic con creditos de API
- VSCode con extension Jupyter (`ms-toolsai.jupyter`)

---

## Recursos

- [Documentacion oficial](https://docs.anthropic.com)
- [Consola de Anthropic](https://console.anthropic.com)
- [Referencia de la API](https://docs.anthropic.com/en/api/getting-started)
- [Modelos disponibles](https://docs.anthropic.com/en/docs/about-claude/models)
