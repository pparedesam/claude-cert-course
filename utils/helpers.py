"""
utils/helpers.py
Utilidades compartidas para el curso de certificación de Claude.
"""

import os
from dotenv import load_dotenv
import anthropic

# Carga las variables de entorno desde .env
load_dotenv()


def get_client() -> anthropic.Anthropic:
    """Retorna un cliente Anthropic configurado con la API key del entorno."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "No se encontró ANTHROPIC_API_KEY. "
            "Crea un archivo .env con tu clave o exporta la variable de entorno."
        )
    return anthropic.Anthropic(api_key=api_key)


# Modelos disponibles
MODELS = {
    "opus":   "claude-opus-4-5",
    "sonnet": "claude-sonnet-4-5",
    "haiku":  "claude-haiku-3-5",
}

DEFAULT_MODEL = MODELS["sonnet"]


def simple_chat(prompt: str, model: str = DEFAULT_MODEL, max_tokens: int = 1024) -> str:
    """Envía un mensaje simple y retorna el texto de la respuesta."""
    client = get_client()
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def chat_with_system(
    prompt: str,
    system: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 1024,
) -> str:
    """Envía un mensaje con system prompt y retorna el texto de la respuesta."""
    client = get_client()
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def print_response(response_text: str, title: str = "Respuesta de Claude") -> None:
    """Imprime la respuesta con formato legible."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(response_text)
    print(f"{'='*60}\n")
