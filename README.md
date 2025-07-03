# Float MCP Server

A FastAPI-based server for integrating with the Float API and providing Model Context Protocol (MCP) endpoints for time logging and project management.

## Features
- RESTful API for logging time entries to Float
- Health check endpoint
- Dockerized for easy deployment
- Configurable via environment variables

## Requirements
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (for dependency management)
- Docker (for containerized deployment)

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-org/float-mcp-server.git
   cd float-mcp-server
   ```
2. **Install dependencies:**
   ```sh
   uv pip install -r requirements.txt
   ```
   Or use the provided `pyproject.toml` with uv:
   ```sh
   uv pip install -r pyproject.toml
   ```

## Usage

### Local Development

- **Format & Lint:**
  ```sh
  make ruff
  ```
- **Clean build artifacts:**
  ```sh
  make clean
  ```
- **Run locally:**
  ```sh
  uv run uvicorn src.main:api_app --reload --port 8000
  ```

### Docker

- **Build and run with Docker Compose:**
  ```sh
  make run
  ```

## Configuration

Set the following environment variable:
- `FLOAT_ACCESS_TOKEN`: Your Float API access token

## API Endpoints

- `GET /health` — Health check
- `POST /v1/logged_time` — Log time entry
- `GET /v1/logged_time` — Retrieve logged time entries

## Project Structure

```
float-mcp-server/
├── src/
│   ├── main.py
│   ├── float/
│   ├── routers/
│   └── utils/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yaml
├── Makefile
├── pyproject.toml
├── uv.lock
└── README.md
```

## License

MIT License
