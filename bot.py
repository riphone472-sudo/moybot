from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image, ImageDraw, ImageFont
import random
import io
import math

TOKEN = "8001601776:AAHZilOQnrb3eWKN3bLIn-3gnqRD-aY7l_E" 

users = {}

# ===== CAPTCHA RASM ======
def generate_code_image(code: str):
    width, height = 600, 300
    # Fon rangi
    bg_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Raqamlar uchun rang
    digit_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    x = 50
    for ch in code:
        angle = random.randint(-25, 25)  # biroz burish
        char_img = Image.new("RGBA", (250, 250), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_img)
        font_size_variation = random.randint(160, 200)  # katta font
        try:
            font_var = ImageFont.truetype("arial.ttf", font_size_variation)
        except:
            font_var = ImageFont.load_default()
        # Qalin raqam
        char_draw.text(
            (10, 20), ch, font=font_var, fill=digit_color,
            stroke_width=4, stroke_fill=(0,0,0)
        )
        rotated = char_img.rotate(angle, expand=1)
        img.paste(rotated, (x, random.randint(50, 100)), rotated)
        x += random.randint(110, 140)  # raqamlar orasidagi masofa

    # Fon chiziqlari (raqamni yashirmasdan)
    for _ in range(25):
        draw.line(
            (
                random.randint(0, width),
                random.randint(0, height),
                random.randint(0, width),
                random.randint(0, height)
            ),
            fill=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
            width=random.randint(2, 4)
        )

    # Tasodifiy nuqtalar
    for _ in range(200):
        draw.point(
            (random.randint(0, width), random.randint(0, height)),
            fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )

    bio = io.BytesIO()
    bio.name = "captcha.png"
    img.save(bio, "PNG")
    bio.seek(0)
    return bio

# ====== TUGMALAR ======
def get_buttons():
    keyboard = [
        [InlineKeyboardButton("⚜️ОПЕРАТОР ТАШКЕНТ⚜️", url="https://t.me/twc29")],
        [InlineKeyboardButton("⚜️ТЕХ Поддержка⚜️", url="https://t.me/evcvcn")],
        [InlineKeyboardButton("🔱ОПЕРАТОР ПРИГОРОД🔱", url="https://t.me/yvczc")],
        [InlineKeyboardButton("🔱ТЕХ Поддержка ПРИГОРОД🔱", url="https://t.me/ycbzb")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== START ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    name = user.first_name or "User"

    # Yangi kod yaratish
    code = str(random.randint(10000, 99999))
    users[user_id] = {"verified": False, "code": code, "name": name}

    image = generate_code_image(code)

    # Tugmalar tepasidagi matn
    message_text = f"Привет, {name}. Пожалуйста, решите капчу с цифрами на этом изображении, чтобы убедиться, что вы человек."

    await update.message.reply_photo(photo=image, caption=message_text)

# ====== KOD TEKSHIRISH ======
async def check_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        return

    name = users[user_id]["name"]

    # Kod to'g'ri kiritsa
    if update.message.text == users[user_id]["code"]:
        users[user_id]["verified"] = True

        # Tugmalar tepasidagi matn
        message_text = "⚡️Вас приветствует Tesla Shop⚡️\nЕсли вам нужна помощь с покупкой, пожалуйста, свяжитесь с оператором."
        await update.message.reply_text(message_text, reply_markup=get_buttons())
    else:
        # Kod noto'g'ri bo'lsa yangi kod
        new_code = str(random.randint(10000, 99999))
        users[user_id]["code"] = new_code
        image = generate_code_image(new_code)
        message_text = f"Привет, {name}. Пожалуйста, решите капчу с цифрами на этом изображении, чтобы убедиться, что вы человек."
        await update.message.reply_photo(photo=image, caption=message_text)

# ====== MAIN ======
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_code))
    app.run_polling()

if __name__ == "__main__":
    main()
