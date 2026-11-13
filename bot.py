import io
import os
import random
import requests
from PIL import Image

# Secrets from GitHub
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL"]  # @wallpapersxxxx

# סגנונות איכותיים ונקיים ל-AI (בלי טקסט ובלי מים)
PROMPTS = [
    "cyberpunk futuristic city street at night, neon lights, highly detailed, vertical wallpaper, 8k, no text, no watermark, photorealistic",
    "serene nature landscape, misty pine forest, cinematic dramatic lighting, vertical wallpaper, 4k, no text, no watermark",
    "abstract dark minimalist art, geometric futuristic design, elegant deep colors, phone wallpaper, 4k, no text, no watermark",
    "majestic wild animal close up, fierce tiger, dramatic studio lighting, vertical, ultra detailed, no text, no watermark",
    "deep space galaxy, vibrant nebula, cosmic dust, stars, dark background, 4k mobile wallpaper, no text, no watermark",
    "japanese aesthetic, traditional pagoda under cherry blossoms at night, glowing lanterns, vertical wallpaper, 4k, no text, no watermark",
    "luxury futuristic supercar, dark cinematic mood, neon reflections, vertical wallpaper, 4k, no text, no watermark",
    "sci-fi futuristic portal, glowing energy beam, dark atmospheric background, vertical wallpaper, 8k, no text, no watermark"
]

def generate_ai_image():
    prompt = random.choice(PROMPTS)
    # נבקש רזולוציה קצת יותר גבוהה כדי שיישאר חד גם אחרי החיתוך
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1080&height=2000&nologo=true"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    
    # פתיחת התמונה וחתך החלק התחתון (שבו בדרך כלל תקוע הלוגו - כ-60 פיקסלים מלמטה)
    img = Image.open(io.BytesIO(response.content))
    width, height = img.getbands() and img.size # רוחב וגובה
    
    # חיתוך: משאירים את כל הרוחב, וחתכים 60 פיקסלים מלמטה
    crop_height = height - 70  
    cropped_img = img.crop((0, 0, width, crop_height))
    
    # שמירת התמונה החתוכה לתוך BytesIO כדי לשלוח לטלגרם
    output = io.BytesIO()
    cropped_img.save(output, format="JPEG", quality=95)
    output.seek(0)
    
    return output.read()

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
    try:
        ai_image = generate_ai_image()
        send_telegram_document(
            chat_id=CHANNEL,
            file_data_or_path=ai_image,
            filename="wallpaper.jpg",
            caption="✨ Wallpaper #wallpaper",
            is_file_path=False
        )
        print("AI image sent successfully (watermark cropped out)")
    except Exception as e:
        print("AI error:", e)

if __name__ == "__main__":
    main()

