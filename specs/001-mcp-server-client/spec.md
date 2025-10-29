# Feature Specification: MCP server y cliente básicos (say_hello)

**Feature Branch**: `[001-mcp-server-client]`  
**Created**: 2025-10-29  
**Status**: Draft  
**Input**: User description: "@[/speckit.specify] 1. Creación de un servidor y cliente MCP básico Tu tarea es crear: Un servidor MCP que exponga una herramienta llamada say_hello que reciba un nombre y devuelva un saludo personalizado. Un cliente MCP que se conecte a este servidor, llame a la herramienta say_hello y muestre el resultado en pantalla. algunas librerrias que podemos instalar es  Para la totalidad de los ejercicios se sugieren las siguientes dependencias (no todas son necesarias en todos los casos): fastmcp>=0.3.0 anyio>=4.0.0 httpx>=0.27.0 mcp openai"

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

### User Story 1 - Servidor MCP expone herramienta say_hello (Priority: P1)

Como desarrollador, quiero iniciar un servidor MCP que exponga la herramienta `say_hello(nombre)` para devolver un saludo personalizado, de modo que otros clientes MCP puedan consumirla.

**Why this priority**: Sin el servidor y su herramienta no hay funcionalidad útil para probar o integrar.

**Independent Test**: Iniciar el servidor de forma aislada y ejecutar una llamada a `say_hello("Mundo")` mediante un cliente de prueba, verificando que responde con un saludo en menos de 500 ms.

**Acceptance Scenarios**:

1. **Given** el servidor MCP está en ejecución, **When** se invoca `say_hello("Ana")`, **Then** responde con un mensaje que contiene "Hola, Ana".
2. **Given** el servidor MCP, **When** se invoca `say_hello("")`, **Then** responde con un error de validación indicando que el nombre es requerido.

---

### User Story 2 - Cliente MCP consume say_hello y muestra resultado (Priority: P2)

Como usuario/desarrollador, quiero un cliente MCP que se conecte al servidor, llame `say_hello(nombre)` y muestre el resultado en consola, para comprobar la integración extremo a extremo.

**Why this priority**: Habilita validación end-to-end y demuestra el valor real para el usuario final.

**Independent Test**: Ejecutar el cliente apuntando al servidor en ejecución con `nombre="Lucía"` y verificar que imprime el saludo y retorna código de salida 0.

**Acceptance Scenarios**:

1. **Given** el servidor operativo, **When** el cliente solicita `say_hello("Lucía")`, **Then** se imprime un saludo con el nombre provisto.

---

### User Story 3 - Manejo de errores y validaciones (Priority: P3)

Como consumidor de la herramienta, quiero mensajes de error claros para entradas inválidas o desconexiones, para entender qué ocurrió y cómo resolverlo.

**Why this priority**: Mejora la DX y evita ambigüedad en casos no felices.

**Independent Test**: Enviar nombre inválido y simular servidor no disponible; verificar mensajes y códigos de salida adecuados.

**Acceptance Scenarios**:

1. **Given** el servidor no está disponible, **When** el cliente intenta conectarse, **Then** el cliente termina con código distinto de 0 y mensaje indicando que no pudo conectarse.
2. **Given** el parámetro `nombre` es demasiado largo (>256), **When** se solicita `say_hello`, **Then** se devuelve error de validación con causa.

---

### Edge Cases

- Nombre vacío o sólo espacios.
- Nombre con caracteres Unicode/acentos y emojis.
- Nombre extremadamente largo (>256 caracteres).
- Cliente pierde la conexión durante la llamada.
- Servidor arrancado en puerto ocupado o permisos insuficientes.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: El servidor DEBE exponer una herramienta `say_hello(nombre: string)` que retorne un saludo personalizado como texto.
- **FR-002**: El servidor DEBE validar que `nombre` no sea vacío y que su longitud máxima sea 256 caracteres; si no, responder con error claro.
- **FR-003**: El cliente DEBE poder conectarse al servidor, invocar `say_hello` con un nombre provisto por el usuario y mostrar el resultado por pantalla.
- **FR-004**: El sistema DEBE manejar errores de conexión y tiempo de espera con mensajes entendibles y códigos de salida adecuados (no 0 en error).
- **FR-005**: El servidor y cliente DEBEN ser ejecutables desde la línea de comandos con instrucciones simples.
- **FR-006**: La comunicación DEBE cumplir el protocolo MCP a un nivel mínimo para exponer/consumir la herramienta.
- **FR-007**: La ejecución DEBE estar documentada en un README breve con comandos básicos.
- **FR-008**: El transporte MCP para el PoC SERÁ TCP en `localhost`, con puerto configurable (por defecto 8765).
- **FR-009**: El idioma por defecto del saludo SERÁ español; el formato de respuesta base será `"Hola, {nombre}"` con codificación UTF-8.

### Key Entities *(include if feature involves data)*

- **Solicitud say_hello**: parámetros de entrada (`nombre`), reglas de validación.
- **Respuesta say_hello**: mensaje de salida (texto), estructura de error (código, mensaje).

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Ejecutar `say_hello` con un nombre válido retorna en <500 ms en entorno local.
- **SC-002**: El cliente imprime exactamente el saludo retornado por el servidor y finaliza con código 0.
- **SC-003**: Errores de validación y de conexión muestran mensajes claros y finalizan con código != 0.
- **SC-004**: La guía de ejecución permite levantar servidor y cliente en <5 minutos por un nuevo desarrollador.
