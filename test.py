# filepath: /Users/thomas/GitHub/Project-Prometheus-1/test.py
from huggingface_hub import login
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the token from the environment
hf_token = os.getenv("HF_TOKEN")
print(hf_token)
# Log in to Hugging Face
login(token=hf_token)