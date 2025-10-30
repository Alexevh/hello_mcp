# Quickstart: OpenAI + FastMCP (count_r)

## Prerrequisitos
- Python 3.12+
- Variables en `.env` (en repo root):
  - `OPENAI_API_KEY=...`
  - `MCP_URL=...` (si usas servidor remoto) o usa localhost
  - `MCP_API_KEY=...` (si el servidor requiere Bearer)

## Instalar dependencias
```
python -m pip install --upgrade pip
python -m pip install fastmcp anyio mcp python-dotenv openai
```

## Ejecutar servidor MCP local (propuesto)
```
python count_r_server.py
```
Por defecto: HTTP en `http://127.0.0.1:8765/mcp`.

## Probar tool `count_r`
- Vía cliente MCP (ejemplo por implementar) o con el orquestador del modelo.

## Demo con OpenAI (gpt-4o-mini)
```
python openai_demo.py --text "Río arriba"
```
- Esperado: modelo utiliza la tool `count_r` y devuelve el conteo de 'r'/'R'.

## Notas
- Límite de entrada: 10,000 caracteres
- Encoding UTF-8
- Autenticación Bearer opcional con `MCP_API_KEY`
