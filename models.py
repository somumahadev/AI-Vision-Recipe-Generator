"""
Model loading and inference functions
"""

import torch
from PIL import Image
from typing import List, Tuple, Dict
import streamlit as st

from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration,
    ViTImageProcessor,
    ViTForImageClassification,
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)


class ModelManager:
    """Manages all AI models for the application"""
    
    def __init__(self, device: str = None):
        """
        Initialize ModelManager
        
        Args:
            device: 'cuda' or 'cpu'. If None, auto-detect
        """
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.models = {}
        
    @st.cache_resource
    def load_blip_model(_self) -> Tuple:
        """Load BLIP model for image captioning"""
        try:
            processor = BlipProcessor.from_pretrained(
                "Salesforce/blip-image-captioning-base"
            )
            model = BlipForConditionalGeneration.from_pretrained(
                "Salesforce/blip-image-captioning-base"
            ).to(_self.device)
            
            return processor, model
        except Exception as e:
            st.error(f"Error loading BLIP model: {str(e)}")
            raise
    
    @st.cache_resource
    def load_vit_model(_self) -> Tuple:
        """Load ViT model for food classification"""
        try:
            processor = ViTImageProcessor.from_pretrained("nateraw/food")
            model = ViTForImageClassification.from_pretrained(
                "nateraw/food"
            ).to(_self.device)
            
            return processor, model
        except Exception as e:
            st.error(f"Error loading ViT model: {str(e)}")
            raise
    
    @st.cache_resource
    def load_flan_model(_self) -> Tuple:
        """Load FLAN-T5 model for recipe generation"""
        try:
            tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
            model = AutoModelForSeq2SeqLM.from_pretrained(
                "google/flan-t5-large"
            ).to(_self.device)
            
            return tokenizer, model
        except Exception as e:
            st.error(f"Error loading FLAN-T5 model: {str(e)}")
            raise
    
    def load_all_models(self):
        """Load all models and cache them"""
        self.models['blip'] = self.load_blip_model()
        self.models['vit'] = self.load_vit_model()
        self.models['flan'] = self.load_flan_model()
        
        return self.models
    
    def generate_caption(self, image: Image.Image) -> str:
        """
        Generate image caption using BLIP
        
        Args:
            image: PIL Image
            
        Returns:
            Caption text
        """
        try:
            processor, model = self.models['blip']
            
            inputs = processor(images=image, return_tensors="pt").to(self.device)
            
            output = model.generate(
                **inputs,
                max_length=50,
                num_beams=5,
                temperature=0.7,
                do_sample=False
            )
            
            caption = processor.decode(output[0], skip_special_tokens=True)
            return caption
            
        except Exception as e:
            st.error(f"Error generating caption: {str(e)}")
            return "Unable to generate caption"
    
    def classify_food(self, image: Image.Image, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Classify food with top-k predictions
        
        Args:
            image: PIL Image
            top_k: Number of top predictions to return
            
        Returns:
            List of (label, confidence) tuples
        """
        try:
            processor, model = self.models['vit']
            
            inputs = processor(images=image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = model(**inputs)
            
            # Get probabilities
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Get top-k predictions
            top_probs, top_indices = torch.topk(probs[0], top_k)
            
            results = []
            for prob, idx in zip(top_probs, top_indices):
                label = model.config.id2label[idx.item()]
                confidence = prob.item()
                results.append((label, confidence))
            
            return results
            
        except Exception as e:
            st.error(f"Error classifying food: {str(e)}")
            return [("Unknown", 0.0)]
    
    def generate_recipe(
        self,
        dish: str,
        caption: str,
        dietary_pref: str = "None",
        servings: int = 4,
        difficulty: str = "Medium"
    ) -> str:
        """
        Generate detailed recipe using FLAN-T5
        
        Args:
            dish: Name of the dish
            caption: Image description
            dietary_pref: Dietary preference
            servings: Number of servings
            difficulty: Recipe difficulty level
            
        Returns:
            Generated recipe text
        """
        try:
            tokenizer, model = self.models['flan']
            
            # Build enhanced prompt
            dietary_clause = f"The recipe must be {dietary_pref}. " if dietary_pref != "None" else ""
            
            prompt = f"""You are a professional chef. Create a detailed recipe.

Dish: {dish}
Description: {caption}
{dietary_clause}Servings: {servings}
Difficulty: {difficulty}

Provide a complete recipe with:
1. Ingredients list (with exact measurements)
2. Step-by-step cooking instructions (numbered steps)
3. Preparation time and cooking time
4. Helpful tips and possible variations

Format the recipe in a clear, professional manner."""

            inputs = tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            ).to(self.device)
            
            outputs = model.generate(
                **inputs,
                max_length=600,
                min_length=200,
                num_beams=5,
                temperature=0.8,
                top_p=0.95,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3,
                early_stopping=True
            )
            
            recipe = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return recipe
            
        except Exception as e:
            st.error(f"Error generating recipe: {str(e)}")
            return "Unable to generate recipe. Please try again."


def create_model_manager(device: str = None) -> ModelManager:
    """
    Factory function to create and initialize ModelManager
    
    Args:
        device: Device to use ('cuda' or 'cpu')
        
    Returns:
        Initialized ModelManager instance
    """
    manager = ModelManager(device=device)
    manager.load_all_models()
    return manager
