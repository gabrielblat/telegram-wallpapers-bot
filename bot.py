import os
import json
import random
import requests

# Secrets from GitHub
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL"]  # @wallpapersxxxx

HISTORY_FILE = "sent_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_new_local_image():
    """מחפש תמונות מקומיות ובוחר תמונה אחת בלבד שטרם נשלחה מעולם"""
    folders = [".", "wallpapers"]
    all_images = []
    
    for folder in folders:
        if os.path.exists(folder):
            for f in os.listdir(folder):
                if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    full_path = os.path.join(folder, f)
                    all_images.append(full_path)
    
    if not all_images:
        return None

    sent_images = load_history()
    available_images = [img for img in all_images if img not in sent_images]
    
    # אם כל התמונות נשלחו בעבר, מאפסים את ההיסטוריה כדי להתחיל סיבוב חדש
    if not available_images:
        print("All local images have been sent already! Resetting history...")
        sent_images = []
        save_history(sent_images)
        available_images = all_images

    # בוחר תמונה אחת אקראית ממה שעוד לא נשלח
    return random.choice(available_images)

def send_telegram_document(chat_id, file_path, filename, caption):
    """שליחת תמונה מקומית כקובץ מקורי ללא דחיסה וללא AI"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    
    with open(file_path, "rb") as f:
        files = {"document": (filename, f)}
        data = {"chat_id": chat_id, "caption": caption}
        response = requests.post(url, data=data, files=files, timeout=60)
        
    response.raise_for_status()
    return response.json()

def main():
    # שולף תמונה אחת בלבד שלא נשלחה מעולם
    image_path = get_new_local_image()
    
    if not image_path:
        print("No local images found in the repository!")
        return

    sent_images = load_history()

    try:
        filename = os.path.basename(image_path)
        send_telegram_document(
            chat_id=CHANNEL,
            file_path=image_path,
            filename=filename,
            caption="🔥 #wallpaper"
        )
        print(f"Local image sent successfully: {image_path}")
        
        # הוספת התמונה להיסטוריה ושמירה בגיטהאב
        if image_path not in sent_images:
            sent_images.append(image_path)
            save_history(sent_images)
            
            os.system(f'git config --global user.name "Wallpaper Bot"')
            os.system(f'git config --global user.email "bot@users.noreply.github.com"')
            os.system(f'git add {HISTORY_FILE}')
            os.system(f'git commit -m "Update sent images history (1 wallpaper) [skip ci]"')
            os.system('git push')
            print("History updated and pushed to GitHub successfully.")

    except Exception as e:
        print("Error sending image:", e)

if __name__ == "__main__":
    main()


