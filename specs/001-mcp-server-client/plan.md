# Implementation Plan: MCP server y cliente (say_hello)

## Overview
- Server MCP TCP que expone la herramienta `say_hello(nombre: string)` y responde "Hola, {nombre}" (UTF-8).
- Cliente MCP que se conecta por TCP a `localhost:8765`, llama `say_hello` y muestra el resultado.
- Idioma por defecto: español.
- Punto de entrada del servidor: `say_hello.py`.

## Scope
- Incluir: servidor TCP, cliente CLI, validación de nombre, manejo de errores, README de uso.
- Excluir: autenticación, despliegue cloud, logs avanzados, observabilidad.

## Architecture & Design
- Protocolo: MCP sobre TCP (localhost, puerto configurable por ENV `MCP_PORT` default 8765).
- Server (Python):
  - Archivo de entrada: `say_hello.py`.
  - Librería: `fastmcp>=0.3.0` (server & tool), `anyio` para ciclo de vida.
  - Tool: `say_hello` con schema (input `name: str`, max len 256, no vacío).
- Client (Python):
  - Archivo: `client.py`.
  - Conexión MCP TCP al servidor, invoca tool y imprime la salida.
  - Dependencias: `mcp` (cliente), `anyio`.

## Dependencies
- fastmcp>=0.3.0
- anyio>=4.0.0
- mcp
- httpx>=0.27.0 (opcional; no requerido para TCP puro MCP)
- openai (opcional; no requerido)

## Project Structure
- `say_hello.py`  (server TCP, entrypoint)
- `client.py`     (cliente MCP)
- `README.md`     (instrucciones)

## Implementation Tasks
1. Server TCP (`say_hello.py`)
   - Inicializar server FastMCP en TCP `localhost:8765`.
   - Registrar tool `say_hello(name: str)`.
   - Validaciones: no vacío, len<=256; errores legibles.
   - Manejo de señales/salida limpia.
2. Client CLI (`client.py`)
   - Aceptar argumento `--name` o posicional.
   - Conectarse a `localhost:8765` (puerto por ENV `MCP_PORT`).
   - Invocar tool y `print` del resultado; código 0 si ok; !=0 en error.
3. Documentación (`README.md`)
   - Cómo instalar deps con `uvx`/`uv`.
   - Cómo iniciar servidor y ejecutar cliente.
   - Variables de entorno (puerto).
4. Validación manual
   - Arrancar server, ejecutar cliente con "Lucía"; ver "Hola, Lucía".
   - Probar errores (vacío, largo, servidor caído).

## Commands (local)
- Instalar deps (opción 1, pip):
  - `uv pip install fastmcp anyio mcp`
- Ejecutar server:
  - `python say_hello.py` (usa `MCP_PORT=8765` por defecto)
- Ejecutar cliente:
  - `python client.py --name "Lucía"`

## Error Handling
- Validación entrada: mensaje: "El nombre es requerido" o "El nombre excede 256 caracteres".
- Conexión: si no conecta, mensaje claro y exit code 1.
- Timeouts: exit code 1; sugerir reintentar.

## Acceptance Criteria (map to Spec)
- SC-001: Latencia local <500ms (comando cliente medido manualmente en entornos típicos).
- SC-002: Cliente imprime saludo exacto y sale con 0.
- SC-003: Errores con mensajes claros y exit != 0.
- SC-004: README permite levantar y probar en <5 minutos.

## Risks & Mitigations
- Compatibilidad cliente MCP: usar APIs estables de `mcp` y `fastmcp`.
- Windows consola y UTF-8: forzar UTF-8 en ejemplo si es necesario.
- Puerto ocupado: permitir configurar `MCP_PORT` y validar al inicio.

## Timeline (indicativo)
- Día 1: Server TCP y tool con validación.
- Día 1: Cliente CLI e integración.
- Día 1: README y validación manual.
