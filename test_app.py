"""
Unit tests for AI Vision Recipe Generator
"""

import pytest
from PIL import Image
import numpy as np

from utils import validate_image, estimate_nutrition, format_recipe_text
from config import config


class TestUtils:
    """Test utility functions"""
    
    def test_validate_image_valid(self):
        """Test image validation with valid image"""
        # Create test image
        img = Image.new('RGB', (100, 100), color='red')
        is_valid, message = validate_image(img)
        assert is_valid is True
        assert message == ""
    
    def test_validate_image_too_small(self):
        """Test image validation with small image"""
        img = Image.new('RGB', (30, 30), color='red')
        is_valid, message = validate_image(img)
        assert is_valid is False
        assert "too small" in message.lower()
    
    def test_validate_image_too_large(self):
        """Test image validation with large image"""
        img = Image.new('RGB', (5000, 5000), color='red')
        is_valid, message = validate_image(img)
        assert is_valid is False
        assert "too large" in message.lower()
    
    def test_estimate_nutrition_known_dish(self):
        """Test nutrition estimation for known dish"""
        nutrition = estimate_nutrition("pizza")
        assert "calories" in nutrition
        assert "protein" in nutrition
        assert nutrition["calories"] == "285"
    
    def test_estimate_nutrition_unknown_dish(self):
        """Test nutrition estimation for unknown dish"""
        nutrition = estimate_nutrition("unknown_food_xyz")
        assert "calories" in nutrition
        assert "~" in nutrition["calories"]  # Should have approximate values
    
    def test_format_recipe_text(self):
        """Test recipe text formatting"""
        recipe_text = format_recipe_text(
            dish="Test Dish",
            caption="Test caption",
            recipe="Test recipe instructions",
            nutrition={"calories": "300", "protein": "15g", "carbs": "40g", "fat": "10g"},
            servings=4,
            difficulty="Medium",
            dietary_pref="None"
        )
        assert "Test Dish" in recipe_text
        assert "4" in recipe_text  # Servings
        assert "300" in recipe_text  # Calories


class TestConfig:
    """Test configuration"""
    
    def test_config_values(self):
        """Test config has required values"""
        assert config.APP_NAME is not None
        assert config.MIN_SERVINGS >= 1
        assert config.MAX_SERVINGS > config.MIN_SERVINGS
        assert len(config.DIETARY_PREFERENCES) > 0
    
    def test_model_config(self):
        """Test model configuration"""
        model_config = config.get_model_config()
        assert "blip" in model_config
        assert "vit" in model_config
        assert "flan" in model_config


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
