"""
Configuration for the idea processor.
"""

import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config(BaseModel):
    """Configuration settings for idea processor."""
    
    # Repository paths
    repo_root: Path = Path(__file__).parent.parent.parent
    ideas_file: Path = repo_root / "IDEAS.md"
    backlog_file: Path = repo_root / "BACKLOG.md"
    backlog_template_file: Path = repo_root / "docs" / "backlog-template.md"
    
    # AI Provider selection
    ai_provider: str = os.getenv("AI_PROVIDER", "openai")  # "openai" or "gemini"
    
    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"
    
    # Gemini settings
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    
    # Similarity threshold (0.0 - 1.0)
    similarity_threshold: float = 0.80  # Ideas with similarity > 80% are marked as duplicates
    
    # Output settings
    verbose: bool = True
    dry_run: bool = False  # If True, don't modify files
    
    class Config:
        arbitrary_types_allowed = True


# Global config instance
config = Config()
