# Data Model: count_r

## Entities

- Request
  - texto: string (required, 1..10,000 chars, UTF-8)

- Response
  - count: integer (>=0)

## Validation Rules

- texto must not be empty or whitespace-only
- texto length <= 10,000
- Unicode supported; counting is case-sensitive and counts both 'r' and 'R'

## Notes

- No persistence required
- Errors return validation messages suitable for users
