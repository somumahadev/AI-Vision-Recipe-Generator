# 🚀 Quick Start Guide

Get the AI Vision Recipe Generator running in 5 minutes!

## Option 1: Automated Setup (Recommended)

### Linux/macOS
```bash
# Clone repository
git clone https://github.com/yourusername/ai-vision-recipe-generator.git
cd ai-vision-recipe-generator

# Make setup script executable
chmod +x setup-script.sh

# Run setup
./setup-script.sh

# Activate virtual environment
source venv/bin/activate

# Run the app
streamlit run app.py
```

### Windows
```powershell
# Clone repository
git clone https://github.com/yourusername/ai-vision-recipe-generator.git
cd ai-vision-recipe-generator

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## Option 2: Docker (Easiest)

```bash
# Clone repository
git clone https://github.com/yourusername/ai-vision-recipe-generator.git
cd ai-vision-recipe-generator

# Run with Docker Compose
docker-compose up

# Access at http://localhost:8501
```

---

## Option 3: Google Colab (No Installation)

```python
# Install dependencies
!pip install -q streamlit torch torchvision transformers pillow accelerate pyngrok

# Clone repository
!git clone https://github.com/yourusername/ai-vision-recipe-generator.git
%cd ai-vision-recipe-generator

# Setup ngrok
from pyngrok import ngrok
public_url = ngrok.connect(8501)
print(f"Public URL: {public_url}")

# Run app
!streamlit run app.py &
```

---

## Troubleshooting

### "CUDA not found" or "GPU not available"
✅ **Solution**: The app works on CPU too! It will automatically detect and use available hardware.

### "Module not found" errors
✅ **Solution**: Make sure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Models downloading slowly
✅ **Solution**: First run downloads ~2-3GB of models. Be patient! Models are cached for future runs.

### Port 8501 already in use
✅ **Solution**: Use a different port:
```bash
streamlit run app.py --server.port 8502
```

---

## First Run

1. **Upload an image** of food (JPG, PNG)
2. **Adjust settings** in the sidebar:
   - Dietary preferences
   - Number of servings
   - Recipe difficulty
3. **Click "Generate Recipe"**
4. **View results**:
   - Food detection with confidence
   - Nutritional information
   - Complete recipe
5. **Download recipe** as text file

---

## System Requirements

### Minimum
- **CPU**: 2 cores
- **RAM**: 8 GB
- **Storage**: 5 GB free
- **Python**: 3.8+

### Recommended
- **CPU**: 4+ cores
- **RAM**: 16 GB
- **GPU**: CUDA-compatible (optional, for faster processing)
- **Storage**: 10 GB free
- **Python**: 3.10+

---

## Next Steps

- 📖 Read the full [README.md](README.md)
- 🚀 Deploy to [Streamlit Cloud](DEPLOYMENT.md#streamlit-cloud)
- 🤝 [Contribute](CONTRIBUTING.md) to the project
- 🐛 [Report issues](https://github.com/yourusername/ai-vision-recipe-generator/issues)

---

## Need Help?

- 💬 [Open an issue](https://github.com/yourusername/ai-vision-recipe-generator/issues)
- 📧 Email: your.email@example.com
- 📚 [Documentation](https://github.com/yourusername/ai-vision-recipe-generator)

---

**Happy cooking with AI! 🍳**