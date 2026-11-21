import os
from dotenv import load_dotenv

load_dotenv()

class AIConfig:
    """Central configuration for LLM providers, model parameters, and timeouts."""
    
    # Provider selection: 'gemini', 'openai', or 'auto' (detects available key, falls back to mock)
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "auto").lower()
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Model names
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Hyperparameters
    TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))  # Low temperature for deterministic, factual outputs
    MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2048"))
    REQUEST_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "20"))      # Timeout in seconds
    
    # Retry policy
    MAX_RETRIES = 2
    RETRY_DELAY = 1.0
