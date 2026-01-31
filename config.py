"""
Configuration settings for AI Vision Recipe Generator
"""

import os
from typing import Dict, List


class Config:
    """Application configuration"""
    
    # App Settings
    APP_NAME = "AI Vision Recipe Generator"
    APP_VERSION = "1.0.0"
    APP_ICON = "🍽️"
    
    # Model Settings
    BLIP_MODEL = "Salesforce/blip-image-captioning-base"
    VIT_MODEL = "nateraw/food"
    FLAN_MODEL = "google/flan-t5-large"
    
    # Image Constraints
    MIN_IMAGE_SIZE = (50, 50)  # pixels
    MAX_IMAGE_SIZE = (4096, 4096)  # pixels
    MAX_FILE_SIZE_MB = 10
    ALLOWED_FORMATS = ["jpg", "jpeg", "png"]
    
    # Generation Parameters
    MAX_CAPTION_LENGTH = 50
    MAX_RECIPE_LENGTH = 600
    MIN_RECIPE_LENGTH = 200
    NUM_BEAMS = 5
    TEMPERATURE = 0.8
    TOP_P = 0.95
    REPETITION_PENALTY = 1.2
    
    # UI Settings
    DEFAULT_SERVINGS = 4
    MIN_SERVINGS = 1
    MAX_SERVINGS = 12
    DEFAULT_DIFFICULTY = "Medium"
    
    # Dietary Options
    DIETARY_PREFERENCES: List[str] = [
        "None",
        "Vegetarian",
        "Vegan",
        "Gluten-Free",
        "Keto",
        "Low-Carb",
        "Dairy-Free",
        "Paleo",
        "Halal",
        "Kosher"
    ]
    
    # Difficulty Levels
    DIFFICULTY_LEVELS: List[str] = [
        "Easy",
        "Medium",
        "Hard"
    ]
    
    # Theme Colors
    PRIMARY_COLOR = "#FF6B6B"
    SECONDARY_COLOR = "#FFE66D"
    BACKGROUND_COLOR = "#0E1117"
    SECONDARY_BG_COLOR = "#262730"
    TEXT_COLOR = "#FAFAFA"
    
    # Cache Settings
    CACHE_TTL = 3600  # 1 hour
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Feature Flags
    ENABLE_TOP_K_PREDICTIONS = True
    ENABLE_NUTRITION_ESTIMATES = True
    ENABLE_RECIPE_EXPORT = True
    ENABLE_STATISTICS = True
    
    @classmethod
    def get_device(cls) -> str:
        """Get computation device"""
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    
    @classmethod
    def get_model_config(cls) -> Dict[str, str]:
        """Get model configuration"""
        return {
            "blip": cls.BLIP_MODEL,
            "vit": cls.VIT_MODEL,
            "flan": cls.FLAN_MODEL
        }


# Create singleton instance
config = Config()
