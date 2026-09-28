import os
import random
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("bot_token")

bot = telebot.TeleBot(token)

eleven = [
    "**eleven** choice",
    "**11** choice",
    "**одиннадцать** choice",
    "**onze** choice",
]

@bot.message_handler(content_types=["text"])
def get_text_messages(message):
  random_word = random.choice(eleven)

  markup = InlineKeyboardMarkup()
  btn_api = InlineKeyboardButton("ПРЕДЛОЖИТЬ ИДЕЮ", callback_data="idea")
  btn_edit = InlineKeyboardButton("ПРОДАТЬ ДУШУ ELEVEN", callback_data="sell_soul")
  markup.add(btn_api, btn_edit)

  # Добавили parse_mode='Markdown', чтобы Telegram отрендерил жирный шрифт
  bot.send_message(
      message.chat.id, random_word, reply_markup=markup, parse_mode="Markdown"
  )


# Обработчик нажатий на инлайн-кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
  if call.data == "idea":
    bot.answer_callback_query(call.id, "eleven")
    bot.send_message(call.message.chat.id, "eleven ждёт от тебя новые идеи..")
  elif call.data == "sell_soul":
    bot.answer_callback_query(call.id, "eleven")

    soul_markup = InlineKeyboardMarkup()
    btn_yes = InlineKeyboardButton("Да", callback_data="yes")
    btn_no = InlineKeyboardButton("Нет", callback_data="no")
    soul_markup.add(btn_yes, btn_no)

    bot.send_message(
        call.message.chat.id, "ты уверен в этом?", reply_markup=soul_markup
    )
  elif call.data == "yes":
    bot.answer_callback_query(call.id, "eleven")
    bot.send_message(
        call.message.chat.id, "твоя душа теперь у eleven.. \nты с нами.."
    )
  elif call.data == "no":
    bot.answer_callback_query(call.id, "eleven")
    soul_markup = InlineKeyboardMarkup()
    btn_yes = InlineKeyboardButton("ХОРОШО Я ПРОДАМ ЕЁ..", callback_data="yes")
    btn_no = InlineKeyboardButton("НИ ЗА ЧТО", callback_data="no")
    soul_markup.add(btn_yes, btn_no)
    bot.send_message(call.message.chat.id, "подумай ещё..", reply_markup=soul_markup)


# Запуск бота
bot.polling(none_stop=True, interval=0)