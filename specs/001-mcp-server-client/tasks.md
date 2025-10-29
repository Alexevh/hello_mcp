# Tasks: MCP server y cliente (say_hello)

Feature: MCP server y cliente básicos (say_hello)
Branch: 001-mcp-server-client

## Phase 1: Setup
- [ ] T001 Create project files baseline per plan (say_hello.py, client.py, README.md)
- [ ] T002 Initialize local env: add C:\Users\Equipo\.local\bin to PATH (done) and ensure Python 3.12+
- [ ] T003 Install dependencies with uv: `uv pip install fastmcp anyio mcp`

## Phase 2: Foundational
- [ ] T004 Define config constants (port default 8765) in say_hello.py
- [ ] T005 [P] Add argument parsing for client.py (`--name`, env MCP_PORT)

## Phase 3: User Story 1 (P1) - Servidor MCP expone herramienta say_hello
- [ ] T006 [US1] Implement FastMCP TCP server skeleton in say_hello.py
- [ ] T007 [P] [US1] Register tool `say_hello(name: str)` with schema and Spanish response
- [ ] T008 [US1] Add input validation: non-empty, max length 256; return proper MCP error
- [ ] T009 [US1] Startup/shutdown handling; log listen address and port
- [ ] T010 [US1] Manual test: run server and verify say_hello("Ana") -> "Hola, Ana"

## Phase 4: User Story 2 (P2) - Cliente MCP consume say_hello y muestra resultado
- [ ] T011 [US2] Implement TCP client connection in client.py to localhost:8765
- [ ] T012 [P] [US2] Invoke tool `say_hello` with provided name and print result
- [ ] T013 [US2] Exit codes: 0 on success; non-zero on error
- [ ] T014 [US2] Manual test: `python client.py --name "Lucía"` prints greeting

## Phase 5: User Story 3 (P3) - Manejo de errores y validaciones
- [ ] T015 [US3] Handle connection errors (server down): clear message and exit 1
- [ ] T016 [P] [US3] Handle validation errors (empty/too long): clear message and exit 1
- [ ] T017 [US3] UTF-8 output handling on Windows console if needed

## Phase 6: Polish & Cross-Cutting
- [ ] T018 [P] Write README.md with quickstart (server, client, env var `MCP_PORT`)
- [ ] T019 [P] Add `.windsurf/` already ignored and document security note
- [ ] T020 Final pass: align with Success Criteria (latency <500ms local, onboarding <5 min)

## Dependencies
- Story order: US1 → US2 → US3
- Parallel examples: T005 with T004; T007 with T009; T012 with T013

## Implementation Strategy
- MVP: Completar US1 (servidor y tool funcional) y verificar llamada con cliente mínimo.
- Iterar: US2 cliente CLI; US3 robustecer errores y DX; luego pulido y README.
