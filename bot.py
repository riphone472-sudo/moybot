from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image, ImageDraw, ImageFont
import random
import io

TOKEN = "8001601776:AAHZilOQnrb3eWKN3bLIn-3gnqRD-aY7l_E"  # <-- bu yerga tokeningizni qo'ying

users = {}

# ===== CAPTCHA RASM ======
def generate_code_image(code: str):
    width, height = 800, 250  # rasm kattaligi
    bg_color = (0, 0, 0)  # qora fon
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    x = 20
    for ch in code:
        angle = random.randint(-15, 15)
        char_img = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
        char_draw = ImageDraw.Draw(char_img)
        font_size = random.randint(160, 180)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        digit_color = (255, 182, 193)  # pushti rang
        char_draw.text(
            (0, 0),
            ch,
            font=font,
            fill=digit_color,
            stroke_width=3,
            stroke_fill=(128, 0, 128)  # qalin kontur
        )

        rotated = char_img.rotate(angle, expand=1)
        img.paste(rotated, (x, random.randint(20, 50)), rotated)
        x += rotated.size[0] - 20

    # Fon chiziqlari
    for _ in range(40):
        draw.line(
            (random.randint(0, width), random.randint(0, height),
             random.randint(0, width), random.randint(0, height)),
            fill=(0, 255, 0),
            width=random.randint(1, 2)
        )

    # Tasodifiy nuqtalar
    for _ in range(300):
        draw.point(
            (random.randint(0, width), random.randint(0, height)),
            fill=(255, 255, 255)
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

    message_text = f"Привет, {name}. Пожалуйста, решите капчу с цифрами на этом изображении, чтобы убедиться, что вы человек."

    await update.message.reply_photo(photo=image, caption=message_text)

# ====== KOD TEKSHIRISH ======
async def check_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        return

    name = users[user_id]["name"]

    if update.message.text == users[user_id]["code"]:
        users[user_id]["verified"] = True
        message_text = "⚡️Вас приветствует Tesla Shop⚡️\nЕсли вам нужна помощь с покупкой, пожалуйста, свяжитесь с оператором."
        await update.message.reply_text(message_text, reply_markup=get_buttons())
    else:
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
