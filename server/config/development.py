import os

import dotenv
from autogen_core.models import ModelFamily
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load environment variables from .env
dotenv.load_dotenv('./.env')

# API Keys and other constants
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
PERSON_URN_KEY = os.getenv('PERSON_URN_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

# LinkedIn Application Credentials
LINKEDIN_CLIENT_ID = "86ezq5ouuhyg4r"
LINKEDIN_CLIENT_SECRET = "WPL_AP1.wQzH7qNav8MRvd55.0yA2tQ=="

# API URLs
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
LINKEDIN_API_URL = "https://api.linkedin.com/v2"

# Headers for API requests
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
}

headers2 = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
}

def get_headers(content_type=None):
    updated_headers = headers2.copy()
    if content_type:
        updated_headers["Content-Type"] = content_type
    return updated_headers

# LLM Configuration
model_client = OpenAIChatCompletionClient(
    model="llama3-70b-8192", 
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
    model_info={
        "vision": False,
        "function_calling": False,
        "json_output": False,
        "family": ModelFamily.is_openai,  
    },
)
