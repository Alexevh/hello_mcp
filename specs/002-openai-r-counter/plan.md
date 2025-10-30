# Implementation Plan: OpenAI + FastMCP: herramienta contadora de 'r'

**Branch**: `[002-openai-r-counter]` | **Date**: 2025-10-29 | **Spec**: `./spec.md`
**Input**: Feature specification from `/specs/002-openai-r-counter/spec.md`

**Note**: Generated via `/speckit.plan`.

## Summary

Construir una tool MCP `count_r(texto)` en un servidor FastMCP (HTTP/TCP) que cuente 'r' y 'R'. Integrar con OpenAI `gpt-4o-mini` para que el modelo invoque la tool (tool use) y devuelva el conteo. Seguridad por Bearer opcional vía `MCP_API_KEY`.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.12  
**Primary Dependencies**: fastmcp, anyio, mcp, python-dotenv, openai (SDK)  
**Storage**: N/A  
**Testing**: Manual e2e (cliente + modelo), opcional pytest unit para `count_r`  
**Target Platform**: Dev Windows local; despliegue FastMCP remoto (HTTP)  
**Project Type**: Single project (scripts Python)  
**Performance Goals**: Tool `count_r` <200 ms local; respuesta modelo <2 s con tool  
**Constraints**: Entrada ≤10k chars; UTF-8; Auth Bearer si aplica  
**Scale/Scope**: PoC educativo, bajo tráfico

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

La constitución del proyecto es genérica (placeholders). No hay gates específicos definidos; proceder sin violaciones. Se mantendrá simplicidad (scripts, sin frameworks innecesarios) y documentación mínima.

## Project Structure

### Documentation (this feature)

```text
specs/002-openai-r-counter/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/ (si aplica)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# Código existente
say_hello.py                # servidor ejemplo (otra feature)
client.py                   # cliente MCP genérico

# Para esta feature (propuesto)
count_r_server.py           # servidor FastMCP con tool count_r
openai_demo.py              # script que llama a gpt-4o-mini y usa la tool
```

**Structure Decision**: Mantener scripts en raíz para PoC. Documentar en quickstart. Sin tests formales por ahora.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
