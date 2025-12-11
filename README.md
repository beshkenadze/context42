# Context42 - MCP RAG Server

A FastMCP-based server for local text search with intelligent document compression.

## 🚀 Quick Start

```bash
# Install globally via uvx
uvx install context42

# Run directly
uvx context42

# Or via uv
uv run context42
```

## 🛠️ MCP Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `load_documents` | Load text files from directory | `directory: str`, `extensions: list[str]`, `max_files: int` |
| `chunk_documents` | Apply compression chunking | `compression_level: float (1.0-128.0)` |
| `search` | Keyword search in chunks | `query: str`, `top_k: int` |
| `get_status` | Get server state | - |

## 📚 MCP Resources

- `context42://status` - Current server state (docs loaded, chunks, compression)
- `context42://documents` - List of loaded document metadata

## 🎯 Example Usage

```bash
# 1. Load documents
tools/call load_documents {"directory": "./docs", "extensions": [".md", ".txt"]}

# 2. Apply 16x compression (100-char chunks)
tools/call chunk_documents {"compression_level": 16.0}

# 3. Search for content
tools/call search {"query": "machine learning", "top_k": 5}
```

## 📊 File Formats Supported

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

## 📊 Compression Levels

| Level | Chunk Size | Use Case |
|-------|------------|----------|
| 1.0x  | 1000 chars | Large context, detailed analysis |
| 4.0x  | 250 chars  | Medium context, balanced search |
| 16.0x | 100 chars  | Small context, fast search |
| 64.0x | 100 chars  | Maximum compression |

## 🔧 Integration

### Claude Desktop
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

### Python Client
```python
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

async def use_context42():
    server_params = StdioServerParameters(
        command="uvx", args=["context42"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("load_documents", {
                "directory": "./documents"
            })
```

### Other CLI Tools Integration

Context42 works seamlessly with popular CLI tools and frameworks:

#### **Claude Desktop Integration**
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

#### **Cursor Editor Integration**
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

#### **Continue.dev Integration**
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

#### **Codeium Integration**
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

#### **Tabby Integration**
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

#### **Cline Integration**
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

#### **Gemini/Code Integration**
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

#### **Windsurf Integration**
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

#### **CodeX Integration**
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

#### **GitHub Copilot Integration**
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

#### **OpenCode Integration**
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

#### **Continue.dev Integration**
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

#### **Aider Integration**
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

#### **Supermaven Integration**
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

#### **Sourcegraph Cody Integration**
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

#### **Tabnine Integration**
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

#### **Replit Ghostwriter Integration**
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

#### **Codeium Chat Integration**
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

#### **Amazon CodeWhisperer Integration**
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

#### **Google Bard Integration**
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

#### **Microsoft Copilot Integration**
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

#### **JetBrains AI Assistant Integration**
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

#### **VS Code GitHub Copilot Integration**
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

#### **Zed Editor Integration**
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

#### **Neovim Integration**
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

#### **Emacs Integration**
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

#### **Vim Integration**
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

#### **Kakoune Integration**
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

#### **Helix Editor Integration**
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

#### **Sublime Text Integration**
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

#### **Atom Editor Integration**
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

#### **Visual Studio Code Integration**
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

#### **IntelliJ IDEA Integration**
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

#### **PyCharm Integration**
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

#### **WebStorm Integration**
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

#### **PhpStorm Integration**
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

#### **RubyMine Integration**
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

#### **CLion Integration**
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

#### **GoLand Integration**
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

#### **Rider Integration**
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

#### **DataGrip Integration**
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

#### **RustRover Integration**
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

#### **Android Studio Integration**
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

#### **Xcode Integration**
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

## 🧪 Development

```bash
# Install dev dependencies
uv sync

# Run server for testing
uv run context42

# Test via FastMCP inspector
fastmcp dev context42/server.py
```

## 📁 Project Structure

```
context42/
├── __init__.py          # Package initialization
├── server.py            # FastMCP app with @tool decorators
├── processor.py         # DocumentProcessor class
├── chunker.py          # Chunker class
├── search.py           # SearchEngine class
└── README.md           # This file
```

## ⚙️ Features

- ✅ **FastMCP Framework**: Modern decorator-based MCP server
- ✅ **Multi-format Support**: .md, .txt, .rst, .json, .yaml, .toml, .csv, .log
- ✅ **Smart Chunking**: Configurable compression (1x-128x) with overlap
- ✅ **Keyword Search**: Relevance-based scoring with previews
- ✅ **uvx Ready**: Installable globally via uvx
- ✅ **Type Safe**: Full type annotations
- ✅ **Error Handling**: Comprehensive exception management
- ✅ **CLI Tool Compatible**: Works with all major CLI tools and editors

## 🐛 Troubleshooting

**Server won't start:**
```bash
uv sync  # Install dependencies
```

**No documents found:**
- Check directory path contains supported file types
- Use absolute paths if needed

**Search returns no results:**
- Ensure documents are loaded and chunked first
- Try different search terms

## 📄 License

MIT License - see LICENSE file for details.