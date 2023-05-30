import telebot
import openai
import fluent.sender

bot_token = '6120279690:AAGNpxrremUE-sQFQV9V9_jo19LI3aY3hpM'

openai_token = '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'

fluentd_host = '127.0.0.1'
fluentd_port = 24224

openai.api_key = openai_token

bot = telebot.TeleBot(bot_token)

logger = fluent.sender.FluentSender('telegram_bot', host=fluentd_host, port=fluentd_port)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=user_input,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )

    generated_text = response.choices[0].text.strip()

    log_message(user_input, generated_text)

    bot.send_message(message.chat.id, generated_text)

def log_message(user_input, generated_text):
    log_data = {
        'user_input': user_input,
        'generated_text': generated_text
    }
    logger.emit('telegram_message', log_data)

bot.polling()