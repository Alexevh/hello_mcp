# Feature Specification: OpenAI + FastMCP: herramienta contadora de 'r'

**Feature Branch**: `[002-openai-r-counter]`  
**Created**: 2025-10-29  
**Status**: Draft  
**Input**: User description: "Crear una integración entre OpenAI API y FastMCP utilizando el modelo gpt-4o-mini y una tool que cuente las letras 'r' en una palabra o frase como MCP Server en FastMCP, utilizada por el modelo de OpenAI especificado."

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Tool MCP cuenta 'r' (Priority: P1)

Como desarrollador, quiero un servidor FastMCP que exponga una herramienta `count_r(texto)` que cuente cuántas letras 'r' (minúscula y mayúscula) hay en una palabra o frase, para poder ser consumida por clientes MCP o por un orquestador.

**Why this priority**: La tool es el núcleo funcional; sin ella no hay integración útil.

**Independent Test**: Invocar `count_r("rRRosa")` devuelve `3` en menos de 200 ms localmente.

**Acceptance Scenarios**:

1. **Given** servidor MCP en ejecución, **When** se llama `count_r("perro")`, **Then** retorna `2`.
2. **Given** servidor MCP, **When** `count_r("")`, **Then** retorna error de validación indicando texto requerido.

---

### User Story 2 - Integración OpenAI (gpt-4o-mini) consume la tool (Priority: P2)

Como usuario, quiero que el modelo OpenAI `gpt-4o-mini` pueda resolver peticiones del tipo "¿cuántas 'r' hay en X?" utilizando la tool MCP `count_r` para asegurar precisión y trazabilidad.

**Why this priority**: Demuestra integración modelo + herramientas MCP (tool use) y agrega valor práctico.

**Independent Test**: Con `OPENAI_API_KEY` configurada, realizar una llamada que instruya al modelo a usar la tool para el texto "Río arriba" y obtener el conteo correcto.

**Acceptance Scenarios**:

1. **Given** API key válida, **When** se consulta al modelo con prompt que requiera contar 'r', **Then** el flujo ejecuta la tool `count_r` y la respuesta incluye el conteo correcto.

---

### User Story 3 - Seguridad y errores (Priority: P3)

Como operador, quiero autenticación por API key para el servidor MCP y manejo claro de errores en entradas inválidas o fallas de red, para operar de forma segura.

**Why this priority**: Protege el endpoint y mejora la DX.

**Independent Test**: Probar sin API key o con key inválida y verificar respuestas 401/403 apropiadas; probar texto inválido y errores claros.

**Acceptance Scenarios**:

1. **Given** falta de `MCP_API_KEY`, **When** un cliente intenta invocar la tool, **Then** recibe error de autenticación.
2. **Given** `texto` >10k caracteres, **When** se solicita `count_r`, **Then** devuelve error de validación por tamaño.

---

### User Story 4 - Manejo de texto vacío o sólo espacios (Priority: P4)

Como usuario, quiero que la herramienta `count_r` maneje correctamente textos vacíos o que contengan sólo espacios, devolviendo un error de validación claro.

**Why this priority**: Mejora la experiencia del usuario y la robustez de la herramienta.

**Independent Test**: Probar `count_r("")` y `count_r("   ")` y verificar errores de validación apropiados.

**Acceptance Scenarios**:

1. **Given** texto vacío, **When** se llama `count_r`, **Then** retorna error de validación indicando texto requerido.
2. **Given** texto con sólo espacios, **When** se llama `count_r`, **Then** retorna error de validación indicando texto requerido.

---

### Edge Cases

- Texto vacío o sólo espacios.
- Texto con mayúsculas/minúsculas mixtas ('R' y 'r').
- Texto con caracteres Unicode y acentos (p.ej., "Río arriba").
- Texto extremadamente largo (>10k) debe rechazarse.
- Cliente sin Authorization o con token inválido.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: Implementar tool MCP `count_r(texto: string) -> {count: int}` que cuente 'r' y 'R'.
- **FR-002**: Validar entrada: `texto` requerido, longitud máxima 10,000 caracteres; errores con mensajes claros.
- **FR-003**: Servidor FastMCP expuesto sobre HTTP (TCP) en `localhost` con puerto configurable; soporte despliegue remoto (FastMCP) y Auth por Bearer si `MCP_API_KEY` presente.
- **FR-004**: Cliente/orquestador debe poder invocar al modelo OpenAI `gpt-4o-mini` y habilitar tool use para `count_r`.
- **FR-005**: El flujo de OpenAI debe utilizar la tool para responder preguntas de conteo de 'r' y devolver el resultado.
- **FR-006**: Documentación breve (README) de setup `.env` (`OPENAI_API_KEY`, `MCP_URL`, `MCP_API_KEY`) y ejecución.

### Key Entities *(include if feature involves data)*

- **Solicitud count_r**: `texto` (string), validaciones.
- **Respuesta count_r**: `count` (int), posible `explanation` (opcional) para logging.

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: `count_r("perro")` retorna `2` en <200 ms localmente.
- **SC-002**: Una consulta a `gpt-4o-mini` que pida contar 'r' en "Río arriba" usa la tool y devuelve el conteo correcto (2 o 3 según normalización de mayúsculas; objetivo: conteo sensible a mayúsculas → 2 para "R" y "r").
- **SC-003**: Errores de validación y autenticación presentan mensajes claros; respuesta HTTP adecuada (p.ej., 400/401) en el gateway si aplica.
- **SC-004**: Onboarding: configurar `.env` y ejecutar demo en <10 minutos siguiendo README.
