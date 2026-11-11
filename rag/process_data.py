import pandas as pd
import os

def load_and_process_data(file_path):
    # 1. בדיקה אם הקובץ קיים
    if not os.path.exists(file_path):
        print(f"❌ שגיאה: הקובץ {file_path} לא נמצא!")
        return []

    # 2. קריאת הקובץ - תמיכה גם ב-CSV וגם באקסל
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    df = df.dropna(how='all')
    processed_docs = []

    for index, row in df.iterrows():
        # בניית הטקסט
        text_parts = [
            f"מספר ספר: {row.get('מספר ספר', 'N/A')}",
            f"שם הספר: {row.get('שם ספר', 'N/A')}",
            f"שם המחבר: {row.get('שם מחבר', 'N/A')}",
            f"מקום הדפוס: {row.get('מקום הדפוס', 'N/A')}",
            f"שנת הדפוס: {row.get('שנת הדפוס', 'N/A')}",
            f"נושאים: {row.get('נושאים', 'N/A')}"
        ]
        
        full_text = " | ".join(text_parts)
        
        metadata = {
            "link": row.get('LINK', 'אין קישור'),
            "row_id": index
        }
        
        processed_docs.append({"text": full_text, "metadata": metadata})

    return processed_docs

# --- בדיקת דופק מעודכנת ---
if __name__ == "__main__":
    # תיקון הנתיב: הקובץ נמצא בתוך תיקיית rag
    FILENAME = os.path.join("rag", "otzar_books.csv") 
    
    documents = load_and_process_data(FILENAME)
    
    if documents:
        print(f"✅ הצלחנו לעבד {50} שורות.")
        print(f"דוגמה: {documents[0]['text']}")