import os
import json
from typing import Annotated

from fastmcp import FastMCP, Context
try:
    from openai import OpenAI
except Exception:  # OpenAI SDK opcional
    OpenAI = None

# Configuración
DEFAULT_PORT = int(os.getenv("MCP_PORT", "8765"))
HOST = os.getenv("MCP_HOST", "127.0.0.1")
PATH = os.getenv("MCP_HTTP_PATH", "/mcp")

mcp = FastMCP("say_hello_server")

def _count_r_core(texto: str) -> int:
    texto_norm = (texto or "").strip()
    if not texto_norm:
        raise ValueError("El texto es requerido")
    if len(texto_norm) > 10000:
        raise ValueError("El texto excede 10000 caracteres")
    return sum(1 for ch in texto_norm if ch == 'r' or ch == 'R')

@mcp.tool
async def say_hello(name: Annotated[str, "Nombre de la persona a saludar"]) -> str:
    """Devuelve un saludo personalizado en español dado un nombre.

    Reglas:
    - name no puede ser vacío ni sólo espacios.
    - Longitud máxima: 256 caracteres.
    """
    nombre = (name or "").strip()
    if not nombre:
        raise ValueError("El nombre es requerido")
    if len(nombre) > 256:
        raise ValueError("El nombre excede 256 caracteres")
    return f"Hola, {nombre}"

@mcp.tool
async def count_r(texto: Annotated[str, "Texto en el que contar letras 'r' y 'R'"]) -> int:
    return _count_r_core(texto)

def run_openai_demo(prompt_text: str) -> None:
    if OpenAI is None:
        raise RuntimeError("El SDK de OpenAI no está instalado. Instala 'openai'.")
    client = OpenAI()
    tools = [
        {
            "type": "function",
            "function": {
                "name": "count_r",
                "description": "Cuenta las letras 'r' y 'R' en un texto",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "texto": {"type": "string"}
                    },
                    "required": ["texto"]
                },
            },
        }
    ]
    messages = [
        {"role": "system", "content": "Eres un asistente que usa herramientas MCP para cálculos exactos."},
        {"role": "user", "content": f"Cuenta cuántas 'r' hay en: {prompt_text}"},
    ]
    first = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    msg = first.choices[0].message
    tool_calls = getattr(msg, "tool_calls", None)
    if tool_calls:
        messages.append({"role": msg.role, "content": msg.content or "", "tool_calls": [tc.model_dump() for tc in tool_calls]})
        tool_messages = []
        for tc in tool_calls:
            if tc.function and tc.function.name == "count_r":
                args = json.loads(tc.function.arguments or "{}")
                texto = args.get("texto", "")
                count = _count_r_core(texto)
                tool_messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps({"count": count}, ensure_ascii=False),
                })
        messages.extend(tool_messages)
        final = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        print((final.choices[0].message.content or "").strip())
    else:
        print((msg.content or "").strip())

if __name__ == "__main__":
    demo_text = os.getenv("OPENAI_DEMO_TEXT")
    run_demo = os.getenv("RUN_OPENAI_DEMO", "0")
    if run_demo == "1" and demo_text:
        run_openai_demo(demo_text)
    else:
        # Ejecuta servidor HTTP (TCP) en host/puerto configurables
        mcp.run(transport="http", host=HOST, port=DEFAULT_PORT, path=PATH)
