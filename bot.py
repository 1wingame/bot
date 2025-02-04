from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import requests
import time

# API токены
BOT_TOKEN = "7528640850:AAGGWg3Hdiq6pw9Vv88Xi0m_LOfN4zg3Xas"
CHECK_ID_BOT_TOKEN = "7902407052:AAGneakRMC7AuG2F7nt6wpKtv42TKrZhIyg"
CHECK_ID_BOT_CHAT_ID = "@your_channel_or_chat_id"

# Ссылки на изображения
WELCOME_IMAGE = "https://raw.githubusercontent.com/your_repo/images/welcome.jpg"
REGISTRATION_IMAGE = "https://raw.githubusercontent.com/your_repo/images/registration.jpg"
ID_IMAGE = "https://raw.githubusercontent.com/your_repo/images/find_id.jpg"

# Функция для удаления предыдущего сообщения и отправки нового
def send_new_message(update: Update, context: CallbackContext, text, image=None, buttons=None):
    if update.message:
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    elif update.callback_query:
        update.callback_query.message.delete()
    
    keyboard = InlineKeyboardMarkup(buttons) if buttons else None
    
    if image:
        msg = context.bot.send_photo(chat_id=update.effective_chat.id, photo=image, caption=text, reply_markup=keyboard)
    else:
        msg = context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=keyboard)
    
    return msg

# Команда /start
def start(update: Update, context: CallbackContext):
    buttons = [[InlineKeyboardButton("🔹 Registrar no bot 🔹", callback_data="register")]]
    send_new_message(update, context, "🔹 Bem-vindo ao bot de sinais com tecnologia ChatGPT-4! 🔹\n\n🚀 Aqui você receberá **sinais precisos** sobre os jogos da 1win...", WELCOME_IMAGE, buttons)

# Инструкция по регистрации
def registration_instruction(update: Update, context: CallbackContext):
    buttons = [[InlineKeyboardButton("🔹 Registrar 🔹", url="https://1wfwna.life/v3/aggressive-casino?p=0a7e")]]
    send_new_message(update, context, "**Para ativar o bot, siga estes passos:**\n\n✅ Registre uma **nova conta** na **1win**...", REGISTRATION_IMAGE, buttons)

# Проверка ID
def check_id(update: Update, context: CallbackContext):
    user_id = update.message.text.strip()
    
    response = requests.get(f"https://api.telegram.org/bot{CHECK_ID_BOT_TOKEN}/getUpdates")
    messages = response.json().get("result", [])
    
    id_found = any(msg.get("message", {}).get("text") == user_id for msg in messages)
    
    if id_found:
        countdown(update, context)
    else:
        buttons = [
            [InlineKeyboardButton("🔹 Digitar novamente 🔹", callback_data="retry")],
            [InlineKeyboardButton("🔹 Registrar 🔹", callback_data="register")]
        ]
        send_new_message(update, context, "❌ ** Seu ID não foi encontrado no banco de dados.**\nVerifique se digitou o ID corretamente...", None, buttons)

# Обратный отсчет
def countdown(update: Update, context: CallbackContext):
    msg = context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Seu ID foi encontrado no banco de dados.")
    
    for i in range(3, 0, -1):
        time.sleep(1)
        context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=msg.message_id, text=str(i))
    
    time.sleep(1)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=msg.message_id)
    
    buttons = [
        [InlineKeyboardButton("Название игры 1", url="ссылка_на_mini_app")],
        [InlineKeyboardButton("Название игры 2", url="ссылка_на_mini_app")]
    ]
    send_new_message(update, context, "✅ Você obteve acesso ao bot!\n\nEscolha um jogo para receber os sinais: 🎯", None, buttons)

# Обработчик callback'ов
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == "register":
        registration_instruction(update, context)
    elif query.data == "retry":
        send_new_message(update, context, "**Digite seu ID no chat para verificação no banco de dados no seguinte formato: 305810088**", ID_IMAGE)

# Запуск бота
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_id))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
