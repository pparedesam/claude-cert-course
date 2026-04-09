import sys
sys.path.append('..')
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

history = []
print("Chat con Claude -- escribe 'salir' para terminar\n")

while True:
    user_input = input("Tu: ").strip()
    if not user_input or user_input.lower() in ("salir", "exit", "quit"):
        print("\nHasta luego!")
        break

    history.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=history
    )

    assistant_reply = response.content[0].text
    history.append({"role": "assistant", "content": assistant_reply})
    print(f"\nClaude: {assistant_reply}\n")
