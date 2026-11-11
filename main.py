import os
import requests
import json
import urllib3
from dotenv import load_dotenv

# ביטול אזהרות SSL לנטפרי
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def ask_gemini(prompt, history):
    # השתמשתי בגרסה 2.5 פלאש כפי שמופיע ברשימה שלך
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    data = {
        "contents": history + [{"role": "user", "parts": [{"text": prompt}]}],
        "system_instruction": {"parts": [{"text": "ענה בקצרה ובעברית."}]}
    }

    try:
        # verify=False פותר את בעיית נטפרי
        response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"שגיאה מהשרת: {response.status_code} - {response.text}"
    except Exception as e:
        return f"שגיאה טכנית: {str(e)}"

def chat():
    print("🤖 Gemini 2.5 Flash מוכן ומחובר! (הקלד 'יציאה' לסיום)")
    history = []
    
    while True:
        user_input = input("\n> ")
        if user_input.lower() in ['exit', 'יציאה']:
            break
            
        answer = ask_gemini(user_input, history)
        print(f"\n💬 {answer}")
        
        # שמירה בהיסטוריה
        if "שגיאה" not in answer:
            history.append({"role": "user", "parts": [{"text": user_input}]})
            history.append({"role": "model", "parts": [{"text": answer}]})

if __name__ == "__main__":
    chat()