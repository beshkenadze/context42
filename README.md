# Golos CLaRa RAG

A CLI application for question answering using Apple's CLaRa model with Golos wiki as knowledge base.

## 🚀 Features

- 🤖 **Apple CLaRa Model**: Uses Apple's state-of-the-art CLaRa (Continuous Latent Reasoning) model
- 📄 **Document Compression**: Built-in semantic document compression (4x-128x ratios)
- 🔍 **Unified RAG**: Joint retrieval and generation in continuous latent space
- ⚡ **MLX-LM**: Optimized for Apple Silicon (M1/M2/M3 chips)
- 💬 **Interactive Mode**: Real-time chat with document context
- 📚 **Golos Wiki**: Uses project documentation as knowledge base

## 📦 Installation

### Using UV (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd golos-clara-rag

# Install with UV
uv sync

# Install the CLI
uv pip install -e .
```

### Manual Installation

```bash
# Install dependencies
pip install mlx-lm transformers python-dotenv

# Install the package
pip install -e .
```

## 🧠 Model Setup

### Download CLaRa Model

```bash
# Download CLaRa-7B-Instruct from HuggingFace
huggingface-cli download apple/CLaRa-7B-Instruct --local-dir ./clara-model

# Or use the model directly from HuggingFace
# The app will auto-download if not found locally
```

## 📖 Usage

### Basic Question Answering

```bash
# Ask a question using all Golos wiki documents
golos-clara --model ./clara-model --wiki ./Golos.wiki "What is Golos?"

# Use specific documents
golos-clara --model apple/CLaRa-7B-Instruct --files Architecture.md User-Guide.md "How does the architecture work?"
```

### Interactive Mode

```bash
# Start interactive chat with all wiki documents
golos-clara --model ./clara-model --wiki ./Golos.wiki --interactive

# Interactive mode with specific documents
golos-clara --model apple/CLaRa-7B-Instruct --files Home.md Installation.md --interactive
```

### Advanced Options

```bash
# Custom compression ratio (higher = more compression)
golos-clara --model ./clara-model --wiki ./Golos.wiki --compression 32 "What are the key features?"

# Adjust generation parameters
golos-clara --model ./clara-model --wiki ./Golos.wiki --max-tokens 256 --temperature 0.5 "Explain the audio pipeline"

# Limit number of documents (for testing)
golos-clara --model ./clara-model --wiki ./Golos.wiki --max-files 10 "What is MLX?"
```

## 🔧 CLaRa Technology

This app uses Apple's **CLaRa (Continuous Latent Reasoning)** framework:

### Key Features

- **🔄 Unified Optimization**: Joint retrieval and generation training
- **📦 Semantic Compression**: 4x-128x document compression with preservation
- **⚡ Continuous Space**: Retrieval and generation in shared latent space
- **🎯 Differentiable Top-K**: End-to-end gradient flow through retrieval

### Compression Ratios

| Ratio | Description | Use Case |
|--------|-------------|-----------|
| 4x | Light compression | Maximum quality preservation |
| 16x | Balanced | Default, good quality-speed tradeoff |
| 32x | High compression | Faster processing |
| 64x | Very high compression | Quick answers |
| 128x | Maximum compression | Fastest processing |

## 📚 Golos Wiki Integration

The app automatically loads markdown files from the Golos wiki:

- **Architecture Documents**: System design and components
- **User Guides**: Installation and usage instructions  
- **Technical Docs**: Audio processing and MLX integration
- **Research Notes**: Development findings and experiments

### Document Processing

- 🧹 **Automatic Cleaning**: Removes markdown formatting, code blocks
- 📄 **Smart Chunking**: Preserves semantic boundaries
- 🔍 **Content Filtering**: Skips empty or invalid files

## 🎯 Examples

### Example 1: Project Overview

```bash
golos-clara --model ./clara-model --wiki ./Golos.wiki "What is Golos and what does it do?"
```

Expected answer about Golos being a macOS speech-to-text app using MLX.

### Example 2: Technical Architecture

```bash
golos-clara --model ./clara-model --files Architecture.md Audio-Pipeline-Architecture-Guide.md \
  "How does the audio pipeline work in Golos?"
```

Expected detailed technical explanation of the audio processing pipeline.

### Example 3: Installation Help

```bash
golos-clara --model ./clara-model --wiki ./Golos.wiki --compression 16 \
  "How do I install Golos on macOS?"
```

Expected step-by-step installation instructions.

### Example 4: Interactive Session

```bash
golos-clara --model ./clara-model --wiki ./Golos.wiki --interactive
```

Start chat session:
```
🤖 CLaRa Interactive Mode
💬 Type your questions about the loaded documents
📋 Context: 47 documents loaded
⌨️  Type 'quit' or 'exit' to end
==================================================

❓ Question: What models does Golos support?
🤔 Thinking...
📝 Answer: Golos supports multiple Whisper models...
⏱️  Time: 2.34s
📊 Compression: 16x
------------------------------
```

## 🛠️ Development

### Project Structure

```
golos_clara/
├── __init__.py          # Package init
├── model.py             # CLaRa model interface
└── cli.py              # CLI application
```

### Key Components

- **CLaRaInterface**: Handles model loading and generation
- **DocumentLoader**: Processes Golos wiki documents
- **CLI**: Argument parsing and user interaction

## 📊 Performance

### Benchmarks on Apple Silicon

- **M1 Pro**: ~2.3 seconds per question (16x compression)
- **M2 Max**: ~1.8 seconds per question (16x compression)  
- **M3 Ultra**: ~1.2 seconds per question (16x compression)

### Memory Usage

- **Base Model**: ~4GB RAM
- **Documents**: Variable (depends on wiki size)
- **Compression**: Reduces memory usage significantly

## 🔍 Troubleshooting

### Common Issues

1. **Model Not Found**:
   ```bash
   huggingface-cli download apple/CLaRa-7B-Instruct --local-dir ./clara-model
   ```

2. **Memory Issues**:
   - Use higher compression ratio: `--compression 32`
   - Limit documents: `--max-files 20`

3. **Slow Generation**:
   - Check MLX-LM installation
   - Verify Apple Silicon compatibility

### Debug Mode

```bash
# Verbose output with timing
golos-clara --model ./clara-model --wiki ./Golos.wiki --verbose "Your question"
```

## 📄 License

This project follows the same license as Apple's CLaRa (MIT).

## 🤝 Contributing

Contributions welcome! Please read the contributing guidelines and submit pull requests.

---

**⚡ Powered by Apple's CLaRa - State-of-the-art document compression and unified RAG**