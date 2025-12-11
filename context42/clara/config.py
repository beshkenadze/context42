"""CLaRa configuration management."""

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass
class CLaRaConfig:
    """Configuration for CLaRa model management."""

    model_path: Path = Path(
        os.environ.get("CONTEXT42_MODEL_PATH", Path.home() / ".cache/context42/models")
    )
    default_model: str = os.environ.get("CONTEXT42_MODEL", "clara-7b-instruct-16")
    device: str = os.environ.get("CONTEXT42_DEVICE", "auto")
    lazy_load: bool = os.environ.get("CONTEXT42_LAZY_LOAD", "true").lower() == "true"

    # Model registry
    MODELS = {
        "clara-7b-instruct-16": {
            "hf_path": "apple/CLaRa-7B-Instruct",
            "subfolder": "compression-16",
            "compression": 16,
            "size_gb": 14,
        },
        "clara-7b-instruct-128": {
            "hf_path": "apple/CLaRa-7B-Instruct",
            "subfolder": "compression-128",
            "compression": 128,
            "size_gb": 14,
        },
        "clara-7b-base-16": {
            "hf_path": "apple/CLaRa-7B-Base",
            "subfolder": "compression-16",
            "compression": 16,
            "size_gb": 14,
        },
        "clara-7b-e2e-16": {
            "hf_path": "apple/CLaRa-7B-E2E",
            "subfolder": "compression-16",
            "compression": 16,
            "size_gb": 14,
        },
    }
