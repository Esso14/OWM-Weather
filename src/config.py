from dotenv import load_dotenv
import os   

load_dotenv()

API_KEY = os.getenv("API_Key")
API_URL = os.getenv("API_URL")