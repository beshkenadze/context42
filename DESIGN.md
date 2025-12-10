# Context42 - MCP RAG Server Refactoring Design

## Overview

Refactor the MCP RAG Server to use **FastMCP** framework and integrate **Apple CLARA** compression technology for intelligent document retrieval.

## Goals

1. Migrate from manual MCP protocol handling to FastMCP decorators
2. Support multiple text file formats (not just `.md`)
3. Package as `uvx`-installable MCP tool
4. Integrate CLARA-style compression for semantic chunking
5. Provide keyword-based search for local text data

---

## Architecture

### Current vs New Structure

```
CURRENT                          NEW (FastMCP)
─────────────────────────────    ─────────────────────────────
mcp_rag_server/                  context42/
├── __init__.py                  ├── __init__.py
└── server.py (384 lines)        ├── server.py      # FastMCP app
                                 ├── processor.py   # DocumentProcessor
                                 ├── chunker.py     # Compression logic
                                 └── search.py      # Search engine
```

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      FastMCP Server                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   @tool     │  │  @resource  │  │     Context         │ │
│  │ decorators  │  │  decorators │  │   (logging, etc)    │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │
│         │                │                     │            │
│  ┌──────▼────────────────▼─────────────────────▼──────────┐│
│  │                    Server State                         ││
│  │  - documents: List[Document]                            ││
│  │  - chunks: List[Chunk]                                  ││
│  │  - compression_level: float                             ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
          │                    │
          ▼                    ▼
┌─────────────────┐   ┌─────────────────┐
│ DocumentProcessor│   │   Chunker       │
│ - load_files()  │   │ - chunk()       │
│ - parse()       │   │ - compress()    │
└─────────────────┘   └─────────────────┘
          │                    │
          ▼                    ▼
┌─────────────────────────────────────────┐
│              SearchEngine               │
│  - keyword_search()                     │
│  - score_relevance()                    │
└─────────────────────────────────────────┘
```

---

## Package Structure

### pyproject.toml

```toml
[project]
name = "context42"
version = "0.1.0"
description = "MCP RAG Server - Local text search with compression"
requires-python = ">=3.10"
dependencies = [
    "fastmcp>=2.0.0",
]

[project.scripts]
context42 = "context42.server:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["context42"]
```

### Installation & Usage

```bash
# Install globally via uvx
uvx install context42

# Or run directly
uvx context42

# Or via uv
uv run context42
```

### Claude Desktop Integration

```json
{
  "mcpServers": {
    "context42": {
      "command": "uvx",
      "args": ["context42"]
    }
  }
}
```

---

## API Design

### Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `load_documents` | Load text files from directory | `directory: str`, `extensions: list[str]`, `max_files: int` |
| `chunk_documents` | Apply compression chunking | `compression_level: float (1.0-128.0)` |
| `search` | Keyword search in chunks | `query: str`, `top_k: int` |
| `get_status` | Get server state | - |

### Resources

| URI | Description |
|-----|-------------|
| `context42://status` | Current server state (docs loaded, chunks, compression) |
| `context42://documents` | List of loaded document metadata |

---

## Implementation Spec

### server.py (FastMCP)

```python
from fastmcp import FastMCP, Context
from context42.processor import DocumentProcessor
from context42.chunker import Chunker
from context42.search import SearchEngine

mcp = FastMCP("context42")

# Server state
state = {
    "documents": [],
    "chunks": [],
    "compression_level": 1.0,
    "directory": None,
}

@mcp.tool
def load_documents(
    directory: str,
    extensions: list[str] = [".md", ".txt", ".rst", ".json"],
    max_files: int = 100,
) -> dict:
    """Load text documents from a directory.

    Args:
        directory: Path to directory containing text files
        extensions: File extensions to include (default: .md, .txt, .rst, .json)
        max_files: Maximum number of files to load

    Returns:
        Summary of loaded documents
    """
    processor = DocumentProcessor()
    state["documents"] = processor.load(directory, extensions, max_files)
    state["directory"] = directory
    return {
        "loaded": len(state["documents"]),
        "directory": directory,
        "extensions": extensions,
    }


@mcp.tool
def chunk_documents(compression_level: float = 1.0) -> dict:
    """Chunk loaded documents with specified compression.

    Args:
        compression_level: Compression ratio (1.0-128.0). Higher = smaller chunks.

    Returns:
        Chunking summary
    """
    if not state["documents"]:
        return {"error": "No documents loaded. Call load_documents first."}

    chunker = Chunker()
    state["chunks"] = chunker.chunk(state["documents"], compression_level)
    state["compression_level"] = compression_level
    return {
        "chunks": len(state["chunks"]),
        "compression_level": compression_level,
        "chunk_size": chunker.get_chunk_size(compression_level),
    }


@mcp.tool
def search(query: str, top_k: int = 5) -> list[dict]:
    """Search document chunks by keyword relevance.

    Args:
        query: Search query (keywords)
        top_k: Number of results to return

    Returns:
        List of matching chunks with scores
    """
    if not state["chunks"]:
        return {"error": "No chunks available. Call chunk_documents first."}

    engine = SearchEngine()
    return engine.search(state["chunks"], query, top_k)


@mcp.tool
def get_status() -> dict:
    """Get current server state."""
    return {
        "documents_loaded": len(state["documents"]),
        "chunks_created": len(state["chunks"]),
        "compression_level": state["compression_level"],
        "directory": state["directory"],
    }


@mcp.resource("context42://status")
def status_resource() -> dict:
    """Current server state."""
    return get_status()


@mcp.resource("context42://documents")
def documents_resource() -> list[dict]:
    """List of loaded documents."""
    return [
        {"filename": d["filename"], "size": d["size"], "path": d["path"]}
        for d in state["documents"]
    ]


def main():
    mcp.run()


if __name__ == "__main__":
    main()
```

### processor.py

```python
from pathlib import Path
from typing import TypedDict


class Document(TypedDict):
    filename: str
    path: str
    content: str
    size: int
    extension: str


class DocumentProcessor:
    """Load and parse text documents from filesystem."""

    def load(
        self,
        directory: str,
        extensions: list[str],
        max_files: int,
    ) -> list[Document]:
        """Load documents from directory."""
        documents: list[Document] = []
        dir_path = Path(directory)

        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        files = []
        for ext in extensions:
            files.extend(dir_path.glob(f"*{ext}"))

        files = sorted(files)[:max_files]

        for file_path in files:
            try:
                content = file_path.read_text(encoding="utf-8")
                documents.append({
                    "filename": file_path.name,
                    "path": str(file_path),
                    "content": content,
                    "size": len(content),
                    "extension": file_path.suffix,
                })
            except Exception:
                continue  # Skip unreadable files

        return documents
```

### chunker.py

```python
from typing import TypedDict


class Chunk(TypedDict):
    chunk_id: str
    filename: str
    content: str
    start_pos: int
    end_pos: int


class Chunker:
    """Document chunking with compression levels."""

    BASE_CHUNK_SIZE = 1000
    MIN_CHUNK_SIZE = 100

    def get_chunk_size(self, compression_level: float) -> int:
        """Calculate chunk size from compression level."""
        return max(self.MIN_CHUNK_SIZE, int(self.BASE_CHUNK_SIZE / compression_level))

    def chunk(
        self,
        documents: list[dict],
        compression_level: float,
    ) -> list[Chunk]:
        """Chunk documents based on compression level."""
        chunk_size = self.get_chunk_size(compression_level)
        overlap = min(chunk_size // 4, 100)
        step = chunk_size - overlap

        chunks: list[Chunk] = []

        for doc in documents:
            content = doc["content"]
            filename = doc["filename"]

            for i in range(0, len(content), step):
                chunk_content = content[i:i + chunk_size]
                if chunk_content.strip():  # Skip empty chunks
                    chunks.append({
                        "chunk_id": f"{filename}_{i}",
                        "filename": filename,
                        "content": chunk_content,
                        "start_pos": i,
                        "end_pos": min(i + chunk_size, len(content)),
                    })

        return chunks
```

### search.py

```python
class SearchEngine:
    """Keyword-based search over document chunks."""

    def search(
        self,
        chunks: list[dict],
        query: str,
        top_k: int,
    ) -> list[dict]:
        """Search chunks by keyword relevance."""
        query_terms = query.lower().split()
        scored: list[dict] = []

        for chunk in chunks:
            content_lower = chunk["content"].lower()
            score = 0

            for term in query_terms:
                count = content_lower.count(term)
                score += count * len(term)  # Weight by term length

            if score > 0:
                scored.append({
                    **chunk,
                    "score": score,
                    "preview": chunk["content"][:200] + "..." if len(chunk["content"]) > 200 else chunk["content"],
                })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]
```

---

## Migration Steps

### Phase 1: Restructure Package
1. Rename `mcp_rag_server/` to `context42/`
2. Update `pyproject.toml` with new package name and `uvx` entry point
3. Split `server.py` into modules (`processor.py`, `chunker.py`, `search.py`)

### Phase 2: Migrate to FastMCP
1. Replace manual MCP protocol with FastMCP decorators
2. Convert `MCPRAGServer` class to `@mcp.tool` decorated functions
3. Convert resources to `@mcp.resource` decorators
4. Remove async message handling boilerplate

### Phase 3: Extend Functionality
1. Add multi-format file support (`.txt`, `.rst`, `.json`, etc.)
2. Improve chunking with overlap and empty-chunk filtering
3. Add search preview in results

### Phase 4: Package & Test
1. Test `uvx context42` installation
2. Verify Claude Desktop integration
3. Test all tools via MCP inspector

---

## File Extensions Supported

| Extension | Description |
|-----------|-------------|
| `.md` | Markdown |
| `.txt` | Plain text |
| `.rst` | reStructuredText |
| `.json` | JSON (as text) |
| `.yaml`, `.yml` | YAML configs |
| `.toml` | TOML configs |
| `.csv` | CSV data |
| `.log` | Log files |

---

## Compression Levels Reference

| Level | Chunk Size | Use Case |
|-------|------------|----------|
| 1.0x | 1000 chars | Full context, detailed analysis |
| 4.0x | 250 chars | Balanced search |
| 16.0x | 100 chars | Fast keyword search |
| 64.0x | 100 chars | Maximum compression |
| 128.0x | 100 chars | Ultra-dense |

---

## Testing

```bash
# Install dev dependencies
uv sync

# Run server for testing
uv run context42

# Test via MCP inspector
fastmcp dev context42/server.py
```

---

## Future Enhancements (Out of Scope)

- [ ] CLARA neural compression integration (requires GPU/model weights)
- [ ] Vector embeddings for semantic search
- [ ] Persistent index storage
- [ ] Recursive directory scanning
- [ ] File watching for auto-reload
