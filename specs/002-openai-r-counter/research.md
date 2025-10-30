# Research: OpenAI + FastMCP (count_r)

## Decisions

- Decision: FastMCP HTTP transport for server
  - Rationale: Alineado con despliegue FastMCP y cliente actual via URL
  - Alternatives: STDIO (local), SSE (legacy); HTTP es preferible para deploy

- Decision: Tool `count_r(texto)` sensible a mayúsc/minúscula ('r' y 'R')
  - Rationale: Requisito explícito contar ambas
  - Alternatives: Normalizar a minúscula; descartado para preservar semántica explícita

- Decision: Límite de entrada 10k caracteres, UTF-8
  - Rationale: Evitar payloads grandes/DoS y aclarar compatibilidad
  - Alternatives: Sin límite; descartado por riesgos

- Decision: Auth Bearer opcional con `MCP_API_KEY`
  - Rationale: Endpoint público debe poder protegerse
  - Alternatives: Sin auth; descartado en producción

- Decision: Integración con OpenAI `gpt-4o-mini` con tool-use
  - Rationale: Requisito de la consigna; modelo económico y capaz
  - Alternatives: Otros modelos OpenAI; no necesarios para el PoC

## Open Questions (resolved)

- ¿Case-sensitivity? → Contar 'r' y 'R' (sensible a mayúscula)
- ¿Error en texto vacío? → Sí, validación con mensaje claro
- ¿Formato de salida? → `{ "count": <int> }` como texto/JSON serializable

## Implementation Notes

- FastMCP server: registrar tool con hint de tipos y docstring; `mcp.run(transport="http", ...)`
- Cliente/orquestador OpenAI: habilitar tools en el prompt y mapear llamada a `count_r`
- Logs: agregar mensajes de validación y conteo (nivel info/debug)
