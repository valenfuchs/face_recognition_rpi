
# Reemplaza 'YOUR_BOT_TOKEN' con el token de tu bot de Telegram
#BOT_TOKEN = '7398046511:AAHGbc9G1Ud90_z7N0zz9IDEgfLRhLrN5kM'
# Reemplaza 'CHAT_ID' con el ID del chat o grupo donde quieres enviar el mensaje
#CHAT_ID = '1591748215'
from telegram import Bot
import asyncio

# Reemplaza 'YOUR_BOT_TOKEN' con el token de tu bot de Telegram
BOT_TOKEN = '7398046511:AAHGbc9G1Ud90_z7N0zz9IDEgfLRhLrN5kM'
# Reemplaza 'CHAT_ID' con el ID del chat o grupo donde quieres enviar el mensaje
CHAT_ID = '1591748215'
PERSONA = "catalinachab"

async def send_telegram_message(is_success, name):
    """
    Envía un mensaje a Telegram dependiendo del valor del parámetro booleano is_success.

    :param is_success: Booleano, si es True envía un mensaje de éxito, si es False envía un mensaje de fallo.
    """
    bot = Bot(token=BOT_TOKEN)
    if is_success:
        message = name + " ingreso al hogar."
    else:
        message = "Un loco se quiere meter."

    await bot.send_message(chat_id=CHAT_ID, text=message)


def enviarMensaje(succes, nombre):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_telegram_message(succes, nombre))

#CHAT_ID = '1591748215'
    # '7398046511:AAHGbc9G1Ud90_z7N0zz9IDEgfLRhLrN5kM'### implementar
#### debe enviar un mensaje a telegram y prender la luz led 
