# RAG Project — Updated

This repository started as a simple **RAG (Retrieval-Augmented Generation)** pipeline for resume screening, built with ChromaDB, sentence-transformers, and Ollama. It has since been **extended into an agentic system**: instead of a fixed retrieve-then-generate flow, the model now decides on its own which tool to call, with what arguments, and how many times — following the **ReAct** (Reason + Act) pattern.

## What changed from the original RAG version

| Before (RAG) | Now (Agent) |
|---|---|
| Fixed pipeline: embed query → retrieve top-k → generate answer | Model decides *which* action to take at each step |
| One retrieval method only | 4 tools: semantic search, scoring, comparison, filtering |
| No decision-making — always retrieves, always generates | Model chooses tools based on the question type (open-ended vs. specific criteria) |

The underlying vector database (ChromaDB + `all-MiniLM-L6-v2`) and Ollama model (`llama3.2:3b`) are unchanged — the addition is the **tool-calling / agent layer** on top.

## How it works

The model is given a list of tools it can call. On each turn, it either:
1. Requests a tool call (with arguments it decides on its own), or
2. Returns a final natural-language answer

When it requests a tool, the Python code executes the real function, sends the result back to the model, and the loop continues until the model has enough information to answer.

## Tools

| Tool | Description |
|---|---|
| `search_resumes` | Semantic search over resumes based on a natural language query |
| `get_candidate_score` | Scores a specific candidate against a list of required skills |
| `compare_candidates` | Compares multiple candidates and ranks them by score |
| `filter_by_criteria` | Filters all resumes by minimum years of experience and/or a required skill |

## Known limitations

- `llama3.2:3b` doesn't always respect the declared JSON types in tool schemas (e.g. sending `"5"` instead of `5` for integer parameters) — tool functions defensively cast inputs with `int()` where needed.
- Years-of-experience extraction relies on a regex pattern (`\d+\+?\s*years?`) and may miss resumes that phrase experience differently.


## Running with Docker

The FastAPI service can be containerized. Ollama itself runs on the host machine (not inside the container) — the container connects to it via `host.docker.internal`.

### Build the image

```bash
docker build -t my-agent .
```

### Run the container

```bash
docker run -d -p 8000:8000 \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  -v "/path/to/chroma_db:/app/chroma_db" \
  -v "/path/to/data:/app/data" \
  --name recruiting-agent my-agent
```

The API will be available at `http://localhost:8000/docs`.

### Notes
- I changed the LLM model to llama3.1:8b due to some lack of light model's ability
- Ollama must be running on the host before starting the container.
- `chroma_db/` and `data/` are mounted as volumes rather than baked into the image, so the database can be updated without rebuilding.
- Running the containerized agent alongside Ollama requires sufficient system RAM, since Docker Desktop (via WSL2) and Ollama both compete for memory on the same machine. On resource-constrained systems, consider using a smaller model (e.g. `llama3.2:3b`) or increasing available RAM / adjusting the WSL2 memory limit via `.wslconfig`.
