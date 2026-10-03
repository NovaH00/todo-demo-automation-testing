# A simple todo app for demonstrating robotcode testing framework

# Usage
The project is managed entirely with `uv` (`npm` is also needed but just for the frontend build)

To build the project: `uv run build`
To build and run the project: `uv run app`
To test the project: `uv run test all` (or run `uv run test` and follow instructions on how to test diffrent suites)
To clean thing up: `uv run clean`

# Stacks
- backend: fastapi
- frontend: Nextjs
- unit tests: pytest
- regression + smoke + e2e + integration tests : robotcode
- test case document file: openpyxl (python) (Not needed for now)
