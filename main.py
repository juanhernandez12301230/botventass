import telebot
import random
import json
import os

# Tomar token desde variable de entorno (para Railway)
TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Archivo para guardar datos de usuarios
DATA_FILE = "data.json"

# Cargar datos si existen
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

# Guardar datos
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

# Generar Key aleatoria
def generar_key():
    return str(random.randint(1000000000, 9999999999))

# /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.chat.id)
    if user_id not in users:
        users[user_id] = {"saldo": 0}
        save_data()
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Ver Productos")
    markup.add("Mi Perfil")
    markup.add("Recargar Saldo")
    
    bot.send_message(message.chat.id, "Bienvenido a TEMO STORE", reply_markup=markup)

# Ver productos
@bot.message_handler(func=lambda message: message.text == "Ver Productos")
def productos(message):
    bot.send_message(message.chat.id, "Producto disponible:\n\n1 Día - $3\n\nEscribe: comprar 1")

# Comprar producto
@bot.message_handler(func=lambda message: message.text.lower().startswith("comprar"))
def comprar(message):
    user_id = str(message.chat.id)
    precio = 3
    if users[user_id]["saldo"] >= precio:
        users[user_id]["saldo"] -= precio
        key = generar_key()
        save_data()
        bot.send_message(message.chat.id,
        f"¡COMPRA EXITOSA!\n\nCompraste:\n1 día\n\nKey: {key}\n\nTu nuevo saldo es: ${users[user_id]['saldo']}")
    else:
        bot.send_message(message.chat.id, "Saldo insuficiente. Recarga saldo para comprar.")

# Ver perfil
@bot.message_handler(func=lambda message: message.text == "Mi Perfil")
def perfil(message):
    user_id = str(message.chat.id)
    saldo = users[user_id]["saldo"]
    bot.send_message(message.chat.id, f"Tu saldo actual es: ${saldo}")

# Recargar saldo
@bot.message_handler(func=lambda message: message.text == "Recargar Saldo")
def recargar(message):
    user_id = str(message.chat.id)
    users[user_id]["saldo"] += 1000
    save_data()
    bot.send_message(message.chat.id, "¡Te han recargado $1000 de saldo!")

# Iniciar bot
bot.polling()
