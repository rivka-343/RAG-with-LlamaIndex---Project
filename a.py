import os
import requests
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
response = requests.get(url, verify=False)

if response.status_code == 200:
    models = response.json()
    print("--- מודלים זמינים עבור המפתח שלך: ---")
    for m in models.get('models', []):
        print(m['name'])
else:
    print(f"שגיאה בבדיקה: {response.status_code} - {response.text}")
