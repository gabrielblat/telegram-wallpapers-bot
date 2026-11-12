import os
import random
import requests
from telegram import Bot
from telegram.constants import ParseMode

# Secrets from GitHub
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL"]  # @wallpapersxxxx

bot = Bot(token=BOT_TOKEN)

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
    # מחפש תמונות בתיקייה הראשית או ב-wallpapers
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

def main():
    # 1. תמונה מ-AI
    try:
        ai_image = generate_ai_image()
        bot.send_document(
            chat_id=CHANNEL,
            document=ai_image,
            filename="ai_wallpaper.jpg",
            caption="AI Wallpaper ✨"
        )
        print("AI image sent")
    except Exception as e:
        print("AI error:", e)

    # 2. תמונה מהמאגר
    local_path = get_random_local_image()
    if local_path:
        try:
            with open(local_path, "rb") as f:
                bot.send_document(
                    chat_id=CHANNEL,
                    document=f,
                    filename=os.path.basename(local_path),
                    caption="From the collection 🔥"
                )
            print("Local image sent:", local_path)
        except Exception as e:
            print("Local image error:", e)
    else:
        print("No local images found")

if __name__ == "__main__":
    main()
