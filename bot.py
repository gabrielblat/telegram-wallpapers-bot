import os
import random
import requests

# Secrets from GitHub
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL"]  # @wallpapersxxxx

# סגנונות ל-AI
PROMPTS = [
    "dark aesthetic wallpaper, high quality, 4k, phone wallpaper",
    "cyberpunk city night, neon lights, ultra detailed, vertical",
    "minimalist nature landscape, misty mountains, calm, 4k",
    "abstract dark art, geometric, elegant, phone wallpaper",
    "wild animal close up, tiger or leopard, dramatic lighting, vertical",
    "galaxy space, stars, nebula, dark background, 4k wallpaper",
    "japanese aesthetic, cherry blossoms night, vertical wallpaper",
    "luxury car dark mood, cinematic lighting, vertical",
]

def generate_ai_image():
    prompt = random.choice(PROMPTS)
    # Pollinations - free AI image
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1080&height=1920&nologo=true"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.content

def get_random_local_image():
    folders = [".", "wallpapers"]
    images = []
    for folder in folders:
        if os.path.exists(folder):
            for f in os.listdir(folder):
                if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    images.append(os.path.join(folder, f))
    if not images:
        return None
    return random.choice(images)

def send_telegram_document(chat_id, file_data_or_path, filename, caption, is_file_path=False):
    """שליחת מסמך (ללא דחיסה) ישירות דרך ה-API של טלגרם"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    
    if is_file_path:
        with open(file_data_or_path, "rb") as f:
            files = {"document": (filename, f)}
            data = {"chat_id": chat_id, "caption": caption}
            response = requests.post(url, data=data, files=files, timeout=60)
    else:
        files = {"document": (filename, file_data_or_path)}
        data = {"chat_id": chat_id, "caption": caption}
        response = requests.post(url, data=data, files=files, timeout=60)
        
    response.raise_for_status()
    return response.json()

def main():
    # 1. תמונה מ-AI
    try:
        ai_image = generate_ai_image()
        send_telegram_document(
            chat_id=CHANNEL,
            file_data_or_path=ai_image,
            filename="ai_wallpaper.jpg",
            caption="AI Wallpaper ✨ #wallpaper",
            is_file_path=False
        )
        print("AI image sent successfully")
    except Exception as e:
        print("AI error:", e)

    # 2. תמונה מהמאגר (אופציונלי - אם יש קבצים מקומיים)
    local_path = get_random_local_image()
    if local_path:
        try:
            send_telegram_document(
                chat_id=CHANNEL,
                file_data_or_path=local_path,
                filename=os.path.basename(local_path),
                caption="From the collection 🔥 #wallpaper",
                is_file_path=True
            )
            print("Local image sent:", local_path)
        except Exception as e:
            print("Local image error:", e)
    else:
        print("No local images found, skipping local image.")

if __name__ == "__main__":
    main()
