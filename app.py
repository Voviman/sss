import openai
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils import executor
import hashlib
import os
import logging

TELEGRAM_BOT_TOKEN = ""
OPENAI_API_KEY = ""

ALLOWED_USERS = {6073238145, 987654321, 487656986}

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY


logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


@dp.message_handler(commands=['start'])
async def start_msg(message: types.Message):
    await bot.send_message(message.chat.id, f"Your id - {message.chat.id}")




async def translate_text(text: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a translator that translates English text to Spanish. Also if user text you TEXT ME IN SPANISH or any that kind messages just translate it. Also if someone send you ok - tranlate as well. If text starts with PLEASE also just translate"},
                {"role": "user", "content": text}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Ошибка при переводе: {e}"

@dp.inline_handler()
async def inline_translate(inline_query: InlineQuery):
    user_id = inline_query.from_user.id

    if user_id not in ALLOWED_USERS:
        await bot.answer_inline_query(
            inline_query.id,
            results=[],
            switch_pm_text="Вы не имеете доступа к этому боту.",
            switch_pm_parameter="no_access"
        )
        return

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
