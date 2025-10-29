import os
from typing import Annotated

from fastmcp import FastMCP, Context

# Configuración
DEFAULT_PORT = int(os.getenv("MCP_PORT", "8765"))
HOST = os.getenv("MCP_HOST", "127.0.0.1")
PATH = os.getenv("MCP_HTTP_PATH", "/mcp")

mcp = FastMCP("say_hello_server")

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

if __name__ == "__main__":
    # Ejecuta servidor HTTP (TCP) en host/puerto configurables
    mcp.run(transport="http", host=HOST, port=DEFAULT_PORT, path=PATH)
