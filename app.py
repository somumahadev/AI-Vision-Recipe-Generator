import streamlit as st
import torch
from PIL import Image
import io
from typing import Dict, List, Tuple, Optional
import json

from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration,
    ViTImageProcessor,
    ViTForImageClassification,
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Vision Recipe Generator",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FF6B6B 0%, #FFE66D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    
    .subtitle {
        text-align: center;
        color: #B0B0B0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .prediction-card {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #FF6B6B;
    }
    
    .confidence-bar {
        background-color: #2E2E2E;
        border-radius: 5px;
        height: 10px;
        margin-top: 0.5rem;
        overflow: hidden;
    }
    
    .confidence-fill {
        background: linear-gradient(90deg, #FF6B6B 0%, #FFE66D 100%);
        height: 100%;
        transition: width 0.3s ease;
    }
    
    .recipe-section {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .ingredient-item {
        padding: 0.5rem;
        margin: 0.3rem 0;
        background-color: #2E2E2E;
        border-radius: 5px;
    }
    
    .nutrition-card {
        background-color: #2E2E2E;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem;
    }
    
    .step-number {
        display: inline-block;
        background-color: #FF6B6B;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        text-align: center;
        line-height: 30px;
        margin-right: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown('<h1 class="main-header">🍽️ AI Vision Recipe Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload a food image and get personalized recipes with AI-powered analysis</p>', unsafe_allow_html=True)

# -----------------------------
# Device Configuration
# -----------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"

# Display system info in sidebar
with st.sidebar:
    st.header("⚙️ System Information")
    st.info(f"**Device:** {device.upper()}")
    st.info(f"**CUDA Available:** {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        st.info(f"**GPU:** {torch.cuda.get_device_name(0)}")

# -----------------------------
# Model Loading with Enhanced Caching
# -----------------------------
@st.cache_resource(show_spinner=False)
def load_models() -> Tuple:
    """Load all AI models with error handling"""
    try:
        # BLIP for image captioning
        blip_processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        blip_model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        ).to(device)
        
        # ViT for food classification
        food_processor = ViTImageProcessor.from_pretrained(
            "nateraw/food"
        )
        food_model = ViTForImageClassification.from_pretrained(
            "nateraw/food"
        ).to(device)
        
        # FLAN-T5 for recipe generation (using larger model)
        flan_tokenizer = AutoTokenizer.from_pretrained(
            "google/flan-t5-large"
        )
        flan_model = AutoModelForSeq2SeqLM.from_pretrained(
            "google/flan-t5-large"
        ).to(device)
        
        return (
            blip_processor, blip_model,
            food_processor, food_model,
            flan_tokenizer, flan_model
        )
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        st.stop()

# Load models with progress indicator
with st.spinner("🔄 Loading AI models... This may take a moment on first run."):
    try:
        (
            blip_processor, blip_model,
            food_processor, food_model,
            flan_tokenizer, flan_model
        ) = load_models()
        st.sidebar.success("✅ All models loaded successfully!")
    except Exception as e:
        st.error(f"Failed to load models: {str(e)}")
        st.stop()

# -----------------------------
# Helper Functions
# -----------------------------
def validate_image(image: Image.Image) -> bool:
    """Validate uploaded image"""
    try:
        # Check image size
        if image.size[0] < 50 or image.size[1] < 50:
            st.error("❌ Image is too small. Please upload a larger image (at least 50x50 pixels).")
            return False
        
        # Check file size (approximate)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        size_mb = len(img_byte_arr.getvalue()) / (1024 * 1024)
        
        if size_mb > 10:
            st.error("❌ Image is too large. Please upload an image smaller than 10MB.")
            return False
            
        return True
    except Exception as e:
        st.error(f"❌ Error validating image: {str(e)}")
        return False

def generate_caption(image: Image.Image) -> str:
    """Generate image caption using BLIP"""
    try:
        inputs = blip_processor(
            images=image,
            return_tensors="pt"
        ).to(device)
        
        output = blip_model.generate(
            **inputs,
            max_length=50,
            num_beams=5,
            temperature=0.7
        )
        
        caption = blip_processor.decode(
            output[0],
            skip_special_tokens=True
        )
        return caption
    except Exception as e:
        st.error(f"Error generating caption: {str(e)}")
        return "Unable to generate caption"

def classify_food(image: Image.Image, top_k: int = 5) -> List[Tuple[str, float]]:
    """Classify food with top-k predictions"""
    try:
        inputs = food_processor(
            images=image,
            return_tensors="pt"
        ).to(device)
        
        with torch.no_grad():
            outputs = food_model(**inputs)
        
        # Get probabilities
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # Get top-k predictions
        top_probs, top_indices = torch.topk(probs[0], top_k)
        
        results = []
        for prob, idx in zip(top_probs, top_indices):
            label = food_model.config.id2label[idx.item()]
            confidence = prob.item()
            results.append((label, confidence))
        
        return results
    except Exception as e:
        st.error(f"Error classifying food: {str(e)}")
        return [("Unknown", 0.0)]

def estimate_nutrition(dish: str) -> Dict[str, str]:
    """Estimate nutritional information (simplified)"""
    # This is a simplified estimation. In production, use a nutrition API
    nutrition_db = {
        "pizza": {"calories": "285", "protein": "12g", "carbs": "36g", "fat": "10g"},
        "burger": {"calories": "540", "protein": "25g", "carbs": "40g", "fat": "27g"},
        "salad": {"calories": "150", "protein": "5g", "carbs": "15g", "fat": "8g"},
        "pasta": {"calories": "350", "protein": "13g", "carbs": "60g", "fat": "7g"},
        "sushi": {"calories": "200", "protein": "9g", "carbs": "30g", "fat": "6g"},
    }
    
    # Try to match dish with database
    dish_lower = dish.lower()
    for key in nutrition_db:
        if key in dish_lower:
            return nutrition_db[key]
    
    # Default values
    return {"calories": "~300", "protein": "~15g", "carbs": "~40g", "fat": "~12g"}

def generate_recipe(
    dish: str, 
    caption: str, 
    dietary_pref: str = "None",
    servings: int = 4,
    difficulty: str = "Medium"
) -> str:
    """Generate detailed recipe with FLAN-T5"""
    try:
        # Enhanced prompt with dietary preferences
        dietary_clause = f"The recipe must be {dietary_pref}. " if dietary_pref != "None" else ""
        
        prompt = f"""You are a professional chef. Create a detailed recipe.

Dish: {dish}
Description: {caption}
{dietary_clause}Servings: {servings}
Difficulty: {difficulty}

Provide:
1. Ingredients (with exact measurements)
2. Step-by-step instructions (numbered)
3. Prep time and cook time
4. Tips and variations

Format the recipe clearly and professionally."""

        inputs = flan_tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        ).to(device)
        
        outputs = flan_model.generate(
            **inputs,
            max_length=600,
            min_length=200,
            num_beams=5,
            temperature=0.8,
            top_p=0.95,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3
        )
        
        recipe = flan_tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )
        
        return recipe
    except Exception as e:
        st.error(f"Error generating recipe: {str(e)}")
        return "Unable to generate recipe. Please try again."

# -----------------------------
# Sidebar Configuration
# -----------------------------
with st.sidebar:
    st.header("🎛️ Recipe Settings")
    
    dietary_pref = st.selectbox(
        "Dietary Preference",
        ["None", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Low-Carb", "Dairy-Free"],
        help="Select dietary restrictions for recipe generation"
    )
    
    servings = st.slider(
        "Number of Servings",
        min_value=1,
        max_value=12,
        value=4,
        help="Adjust recipe serving size"
    )
    
    difficulty = st.select_slider(
        "Recipe Difficulty",
        options=["Easy", "Medium", "Hard"],
        value="Medium",
        help="Choose your preferred recipe complexity"
    )
    
    show_top_k = st.checkbox(
        "Show Top 5 Predictions",
        value=True,
        help="Display multiple food detection results with confidence scores"
    )
    
    st.markdown("---")
    st.header("📊 Statistics")
    
    # Session state for tracking
    if 'recipes_generated' not in st.session_state:
        st.session_state.recipes_generated = 0
    
    st.metric("Recipes Generated", st.session_state.recipes_generated)

# -----------------------------
# Main UI
# -----------------------------
uploaded_file = st.file_uploader(
    "📤 Upload a food image (JPG, PNG, JPEG)",
    type=["jpg", "png", "jpeg"],
    help="Upload a clear photo of food for best results"
)

if uploaded_file:
    try:
        # Load and validate image
        image = Image.open(uploaded_file).convert("RGB")
        
        if not validate_image(image):
            st.stop()
        
        # Display image and controls
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(image, caption="📷 Uploaded Image", use_container_width=True)
            
            # Image info
            st.caption(f"Image Size: {image.size[0]} x {image.size[1]} pixels")
        
        with col2:
            st.markdown("### 🔍 Analysis Options")
            
            analyze_button = st.button(
                "🍳 Generate Recipe",
                type="primary",
                use_container_width=True
            )
            
            if analyze_button:
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Step 1: Generate caption
                    status_text.text("🔍 Analyzing image...")
                    progress_bar.progress(25)
                    caption = generate_caption(image)
                    
                    # Step 2: Classify food
                    status_text.text("🍽️ Detecting food items...")
                    progress_bar.progress(50)
                    food_predictions = classify_food(image, top_k=5 if show_top_k else 1)
                    
                    # Step 3: Generate recipe
                    status_text.text("📝 Generating recipe...")
                    progress_bar.progress(75)
                    
                    primary_dish = food_predictions[0][0]
                    recipe = generate_recipe(
                        primary_dish,
                        caption,
                        dietary_pref,
                        servings,
                        difficulty
                    )
                    
                    # Step 4: Get nutrition info
                    status_text.text("📊 Estimating nutrition...")
                    progress_bar.progress(90)
                    nutrition = estimate_nutrition(primary_dish)
                    
                    progress_bar.progress(100)
                    status_text.empty()
                    progress_bar.empty()
                    
                    # Update statistics
                    st.session_state.recipes_generated += 1
                    
                    # Display results
                    st.markdown("---")
                    
                    # Food Detection Results
                    st.markdown("### 🎯 Food Detection Results")
                    
                    if show_top_k:
                        for idx, (label, confidence) in enumerate(food_predictions, 1):
                            confidence_pct = confidence * 100
                            
                            st.markdown(f"""
                            <div class="prediction-card">
                                <h4>#{idx} {label}</h4>
                                <p>Confidence: {confidence_pct:.2f}%</p>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: {confidence_pct}%"></div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        label, confidence = food_predictions[0]
                        st.success(f"**Detected:** {label} ({confidence*100:.2f}% confidence)")
                    
                    # Image Description
                    st.markdown("### 📝 Image Description")
                    st.info(caption)
                    
                    # Nutritional Information
                    st.markdown("### 🥗 Estimated Nutrition (per serving)")
                    
                    col_n1, col_n2, col_n3, col_n4 = st.columns(4)
                    
                    with col_n1:
                        st.markdown(f"""
                        <div class="nutrition-card">
                            <h3>{nutrition['calories']}</h3>
                            <p>Calories</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_n2:
                        st.markdown(f"""
                        <div class="nutrition-card">
                            <h3>{nutrition['protein']}</h3>
                            <p>Protein</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_n3:
                        st.markdown(f"""
                        <div class="nutrition-card">
                            <h3>{nutrition['carbs']}</h3>
                            <p>Carbs</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_n4:
                        st.markdown(f"""
                        <div class="nutrition-card">
                            <h3>{nutrition['fat']}</h3>
                            <p>Fat</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Recipe
                    st.markdown("### 📖 Generated Recipe")
                    st.markdown(f"""
                    <div class="recipe-section">
                        <h3>{primary_dish}</h3>
                        <p><strong>Servings:</strong> {servings} | <strong>Difficulty:</strong> {difficulty}</p>
                        {dietary_pref != "None" and f"<p><strong>Dietary:</strong> {dietary_pref}</p>" or ""}
                        <hr>
                        <div style="white-space: pre-wrap;">{recipe}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Export options
                    st.markdown("### 💾 Export Recipe")
                    
                    recipe_text = f"""
{primary_dish}
{"=" * 50}

Servings: {servings}
Difficulty: {difficulty}
{f"Dietary: {dietary_pref}" if dietary_pref != "None" else ""}

Image Description: {caption}

NUTRITIONAL INFORMATION (per serving):
- Calories: {nutrition['calories']}
- Protein: {nutrition['protein']}
- Carbs: {nutrition['carbs']}
- Fat: {nutrition['fat']}

RECIPE:
{recipe}

---
Generated by AI Vision Recipe Generator
"""
                    
                    st.download_button(
                        label="📥 Download Recipe (TXT)",
                        data=recipe_text,
                        file_name=f"{primary_dish.replace(' ', '_')}_recipe.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"❌ An error occurred during processing: {str(e)}")
                    st.info("Please try uploading a different image or check your internet connection.")
    
    except Exception as e:
        st.error(f"❌ Error loading image: {str(e)}")
        st.info("Please upload a valid image file.")

else:
    # Landing state with examples
    st.markdown("### 🌟 How It Works")
    
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h2>1️⃣</h2>
            <h4>Upload Image</h4>
            <p>Take or upload a photo of your food</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h2>2️⃣</h2>
            <h4>AI Analysis</h4>
            <p>Our AI identifies the dish and analyzes ingredients</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_info3:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h2>3️⃣</h2>
            <h4>Get Recipe</h4>
            <p>Receive a complete recipe with instructions</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features
    st.markdown("### ✨ Features")
    
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("""
        - 🎯 **Accurate Food Detection** - Identify 101+ food items
        - 📝 **Detailed Recipes** - Step-by-step cooking instructions
        - 🥗 **Nutrition Estimates** - Calorie and macro information
        - 🌱 **Dietary Options** - Support for various dietary restrictions
        """)
    
    with features_col2:
        st.markdown("""
        - 🔢 **Serving Adjustments** - Scale recipes for any number
        - 📊 **Confidence Scores** - Multiple predictions with probabilities
        - 💾 **Recipe Export** - Download recipes as text files
        - ⚡ **Fast Processing** - Quick AI-powered analysis
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888;">
    <p>Powered by BLIP, ViT, and FLAN-T5 🤖</p>
    <p>Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
