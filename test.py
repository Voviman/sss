import openai
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils import executor
import hashlib
import os

TELEGRAM_BOT_TOKEN = "8192900615:AAGhxocPfibRhqlzZxfzrvfIKN6iG8RGjbw"
OPENAI_API_KEY = "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"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

async def translate_text(text: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a translator that translates English text to Spanish."},
                {"role": "user", "content": text}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Ошибка при переводе: {e}"

@dp.inline_handler()
async def inline_translate(inline_query: InlineQuery):
    query_text = inline_query.query

    if not query_text:
        return

    translated_text = await translate_text(query_text)

    result_id = hashlib.md5(query_text.encode()).hexdigest()

    item = InlineQueryResultArticle(
        id=result_id,
        title="Перевод текста",
        input_message_content=InputTextMessageContent(translated_text),
        description=translated_text
    )

    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

