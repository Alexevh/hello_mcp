import os
import sys
import argparse
import anyio
from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.auth import BearerAuth


def build_url() -> str:
    # Prefer explicit MCP_URL if provided (e.g., FastMCP deployment)
    mcp_url = os.getenv("MCP_URL")
    if mcp_url:
        return mcp_url
    host = os.getenv("MCP_HOST", "127.0.0.1")
    port = int(os.getenv("MCP_PORT", "8765"))
    path = os.getenv("MCP_HTTP_PATH", "/mcp")
    if not path.startswith("/"):
        path = "/" + path
    return f"http://{host}:{port}{path}"


async def run(name: str):
    url = build_url()
    api_key = os.getenv("MCP_API_KEY")
    auth = BearerAuth(api_key) if api_key else None
    async with Client(url, auth=auth) as client:
        try:
            result = await client.call_tool("say_hello", {"name": name})
        except Exception as e:
            print(f"Error al invocar la herramienta: {e}", file=sys.stderr)
            raise SystemExit(1)
        try:
            # Extraer texto del contenido (respuesta MCP)
            content = getattr(result, "content", None)
            if content and len(content) > 0 and getattr(content[0], "text", None):
                print(content[0].text)
            else:
                # Fallback si la respuesta es simple
                print(str(result))
        except Exception as e:
            print(f"Error procesando la respuesta: {e}", file=sys.stderr)
            raise SystemExit(1)


def main(argv=None):
    # Load .env variables if present
    load_dotenv()
    # Ensure UTF-8 output on Windows consoles
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser(description="Cliente MCP para say_hello")
    parser.add_argument("--name", "-n", required=True, help="Nombre a saludar")
    args = parser.parse_args(argv)

    nombre = (args.name or "").strip()
    if not nombre:
        print("El nombre es requerido", file=sys.stderr)
        return 1
    if len(nombre) > 256:
        print("El nombre excede 256 caracteres", file=sys.stderr)
        return 1

    try:
        anyio.run(run, nombre)
    except SystemExit as se:
        return int(se.code)
    except Exception as e:
        print(f"Error de conexión o ejecución: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
