# MCP Server y Cliente (say_hello)

Servidor MCP sobre HTTP (TCP) que expone la herramienta `say_hello(name)` y cliente que la consume.

- Transporte: HTTP en `http://127.0.0.1:8765/mcp` (configurable)
- Idioma por defecto: español
- Punto de entrada servidor: `say_hello.py`
- Cliente: `client.py`

## Requisitos
- Python 3.12+
- Windows PowerShell (este repo está configurado en Windows)

## Instalación de dependencias
Con pip (global o venv):

```
python -m pip install --upgrade pip
python -m pip install fastmcp anyio mcp
```

Opcional con uv (si tienes uv):

```
uv pip install fastmcp anyio mcp
``;

## Variables de entorno (opcionales)
- `MCP_URL` (tiene prioridad si está definido). Ejemplo: `https://evolutionary-fuchsia-shark.fastmcp.app/mcp`
- `MCP_API_KEY` (si está definido, el cliente envía `Authorization: Bearer <MCP_API_KEY>`) 
- `MCP_HOST` (default `127.0.0.1`)
- `MCP_PORT` (default `8765`)
- `MCP_HTTP_PATH` (default `/mcp`)

## Ejecutar el servidor

```
python say_hello.py
```

Esto levanta el servidor MCP HTTP en `http://127.0.0.1:8765/mcp`.

## Ejecutar el cliente

Con `.env` (recomendado para despliegue FastMCP): crea un archivo `.env` con:

```
MCP_URL=https://evolutionary-fuchsia-shark.fastmcp.app/mcp
MCP_API_KEY=tu_api_key
```

```
python client.py --name "Lucía"
```

Salida esperada:

```
Hola, Lucía
```

## Errores comunes
- Nombre vacío: `El nombre es requerido` (exit code 1)
- Nombre >256: `El nombre excede 256 caracteres` (exit code 1)
- Servidor no disponible: error de conexión (exit code 1)

## Notas
- `.windsurf/` está en `.gitignore` por seguridad.
- Puerto configurable vía `MCP_PORT`; si está ocupado, el servidor fallará en el arranque.
