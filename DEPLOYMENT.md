# Deployment Guide

This guide covers various deployment options for the AI Vision Recipe Generator.

## 🚀 Streamlit Cloud (Recommended for beginners)

### Prerequisites
- GitHub account
- Streamlit Cloud account (free)

### Steps

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/ai-vision-recipe-generator.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Your app will be live at:**
   `https://your-app-name.streamlit.app`

### Updating the app
Just push changes to GitHub - Streamlit Cloud auto-deploys!

```bash
git add .
git commit -m "Update features"
git push
```

---

## 🐳 Docker Deployment

### Build and Run

```bash
# Build image
docker build -t ai-recipe-generator .

# Run container
docker run -p 8501:8501 ai-recipe-generator

# Or use docker-compose
docker-compose up -d
```

### Access the app
`http://localhost:8501`

### Stop container
```bash
docker-compose down
```

---

## ☁️ Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Setup files

Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

### Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# Open app
heroku open
```

---

## 🌐 AWS EC2 Deployment

### Launch EC2 Instance

1. Launch Ubuntu 22.04 LTS instance
2. Configure security group (allow port 8501)
3. SSH into instance

### Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.10
sudo apt install python3.10 python3-pip -y

# Clone repository
git clone https://github.com/yourusername/ai-vision-recipe-generator.git
cd ai-vision-recipe-generator

# Install dependencies
pip3 install -r requirements.txt

# Run with nohup
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
```

### Access
`http://your-ec2-public-ip:8501`

### Keep running (systemd service)

Create `/etc/systemd/system/streamlit-app.service`:
```ini
[Unit]
Description=Streamlit App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-vision-recipe-generator
ExecStart=/usr/bin/python3 -m streamlit run app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl enable streamlit-app
sudo systemctl start streamlit-app
sudo systemctl status streamlit-app
```

---

## 🔵 Azure Web App Deployment

### Using Azure CLI

```bash
# Login
az login

# Create resource group
az group create --name recipe-generator-rg --location eastus

# Create App Service plan
az appservice plan create --name recipe-generator-plan --resource-group recipe-generator-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group recipe-generator-rg --plan recipe-generator-plan --name your-app-name --runtime "PYTHON:3.10"

# Deploy code
az webapp up --name your-app-name --resource-group recipe-generator-rg
```

---

## 🔴 Google Cloud Run Deployment

### Prerequisites
- Google Cloud account
- gcloud CLI installed

### Deploy

```bash
# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Build container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/recipe-generator

# Deploy to Cloud Run
gcloud run deploy recipe-generator \
  --image gcr.io/YOUR_PROJECT_ID/recipe-generator \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2
```

---

## 🔐 Environment Variables & Secrets

### Streamlit Cloud

Add secrets in app settings:
```toml
# .streamlit/secrets.toml (not committed to git)

[api_keys]
nutrition_api_key = "your-key-here"
```

### Docker

```bash
docker run -p 8501:8501 \
  -e NUTRITION_API_KEY=your-key \
  ai-recipe-generator
```

### Heroku

```bash
heroku config:set NUTRITION_API_KEY=your-key
```

---

## 📊 Monitoring & Logging

### Streamlit Cloud
- Built-in logs in dashboard
- View real-time metrics

### Custom Monitoring

Add to `app.py`:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("App started")
```

---

## ⚡ Performance Optimization

### Model Caching
Already implemented with `@st.cache_resource`

### CDN for Static Assets
Use services like Cloudflare or AWS CloudFront

### Database for Recipes
Add PostgreSQL or MongoDB for saving recipes

---

## 🔒 Security Best Practices

1. **Never commit secrets**
   - Use `.gitignore`
   - Use environment variables

2. **Enable HTTPS**
   - Streamlit Cloud: automatic
   - Custom domain: use Let's Encrypt

3. **Rate limiting**
   ```python
   from streamlit_rate_limiter import rate_limiter
   
   @rate_limiter(max_calls=10, period=60)
   def generate_recipe():
       # Function code
   ```

4. **Input validation**
   - Already implemented in `utils.py`

---

## 🆘 Troubleshooting

### Out of Memory
Increase container memory or use smaller models

### Slow Loading
- Enable model caching
- Use CDN for assets
- Optimize image preprocessing

### Connection Timeout
Increase timeout in deployment settings

---

## 📞 Support

- GitHub Issues: [Report problems](https://github.com/yourusername/ai-vision-recipe-generator/issues)
- Documentation: [Read the docs](https://github.com/yourusername/ai-vision-recipe-generator)

---

**Choose the deployment option that best fits your needs!**