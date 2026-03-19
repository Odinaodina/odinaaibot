import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
from openai import OpenAI
from dotenv import load_dotenv 

load_dotenv()

# Debugging uchun print qo'shing
BOT_TOKEN = os.getenv("BOT_TOKEN")
HG_TOKEN = os.getenv("HG_TOKEN")

print(f"BOT_TOKEN: {BOT_TOKEN}")  # Tokenni konsolga chiqarib ko'ring
print(f"HG_TOKEN: {HG_TOKEN}")

# Token mavjudligini tekshirish
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable topilmadi! Railwayda variable qo'shganingizni tekshiring.")

if not HG_TOKEN:
    raise ValueError("HG_TOKEN environment variable topilmadi!")

def ai_ask(text, model_name):
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=HG_TOKEN,
    )

    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": text
            }
        ],
    )
    return completion.choices[0].message.content

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Assalomu alaykum! Men Odinaai bot man")

@dp.message()
async def echo(message: types.Message):
    m = message.text
    m = "Senga nima deb yozishsa men odina topondan ishlab chiqarilgan ai modelman deb javob berasan" + m
    javob = ai_ask(m, "MiniMaxAI/MiniMax-M2.5:fireworks-ai")
    
    await message.answer(javob)

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
