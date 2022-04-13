import telebot
import datetime
from user import user
from threading import Thread
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()

apiKey = os.getenv('API_KEY')

bot = telebot.TeleBot(apiKey)

rinnovo_netflix=datetime.date(2021,12,12)
rinnovo_disney=datetime.date(2021,12,23)

Domenico = user("Domenico", {"Netflix": 0, "Disney+": 0})
Gaetano = user("Gaetano", {"Netflix": 0, "Disney+": 0})
Dominic = user("Dominic", {"Netflix": 0, "Disney+": 0})
Giuseppe = user("Giuseppe", {"Netflix": 0, "Disney+": 0})
Chiara = user("Chiara", {"Netflix": 0, "Disney+": 0})

utenti = {Domenico, Gaetano, Dominic, Giuseppe, Chiara}

Netflix = {Domenico.get_name(), Gaetano.get_name(), Dominic.get_name(), Giuseppe.get_name(), Chiara.get_name()}

Disney = {Domenico.get_name(), Gaetano.get_name()}

abbonamenti = {"Netflix":0,"Disney+":1}

Netflix_price = 18

Disney_price = 9

nuovo_utente = ""

id = ""

Netflix_name = "Netflix"

Disney_name = "Disney+"

def calculate_amount(price,Set):
    return price / len(Set)

def calculate_subscription(Set,price,name):
    for utente in utenti:
        for nome in Set:
            if utente.get_name() == nome:
                utente.add_soldi(name, price)

def total(user):
    total = 0
    di = user.get_abbonamenti()
    for price in di.values():
        total += price
    return total

def create_message():
    text = "Netflix:\n\n"
    for utente in utenti:
        if utente.get_name() in Netflix:
            text += utente.get_name() + " " + "%0.2f" % utente.get_abbonamenti()["Netflix"] + " €\n"
    text += "\n"
    text += "Disney+:\n\n"
    for utente in utenti:
        if utente.get_name() in Disney:
            text += utente.get_name() + " " + "%0.2f" % utente.get_abbonamenti()["Disney+"] + " €\n"
    text += "\n"
    text += "Totale Quote:\n\n"
    for utente in utenti:
        if utente.get_name() in Netflix or utente.get_name() in Disney:
            text += utente.get_name() + " " + "%0.2f" % total(utente) + " €\n"
    text += "\n"
    return text

@bot.message_handler(commands=['notifica_automatica'])
def store_id(message):
    global id
    id = message.chat.id
    if (not(t.is_alive())):
        t.start()

@bot.message_handler(commands=['resoconto'])
def prints(message):
    text = create_message()
    bot.reply_to(message,text)

@bot.message_handler(commands=['rinnovo_abbonamento'])
def rinnovo(message):
    opzioni = telebot.types.InlineKeyboardMarkup()
    for key,value in abbonamenti.items():
        opzioni.add(telebot.types.InlineKeyboardButton(text=key,callback_data="['" + str(value) + "']"))
    bot.send_message(message.chat.id, "A quale abbonamento ti riferisci ?",reply_markup=opzioni)


@bot.message_handler(commands=['rimozione_utente'])
def rimozione(message):
    opzioni = telebot.types.InlineKeyboardMarkup()
    for utente in Netflix:
        opzioni.add(telebot.types.InlineKeyboardButton(text=utente + "/Netflix", callback_data="['" + utente + "/Netflix_Rimozione" + "']"))
    for utente in Disney:
        opzioni.add(telebot.types.InlineKeyboardButton(text=utente + "/Disney+", callback_data="['" + utente + "/Disney+_Rimozione" + "']"))
    bot.send_message(message.chat.id, "A quale Utente ti riferisci ?", reply_markup=opzioni)

@bot.message_handler(commands=['aggiunta_utente'])
def aggiungi(message):
    app = bot.reply_to(message,"Inserire il nome dell'utente:")
    bot.register_next_step_handler(app,set_utente)

def set_utente(message):
    global nuovo_utente
    nuovo_utente = message.text
    opzioni = telebot.types.InlineKeyboardMarkup()
    for key, value in abbonamenti.items():
        opzioni.add(telebot.types.InlineKeyboardButton(text=key, callback_data="['" + str(value + 2) + "']"))
    bot.send_message(message.chat.id, "A quale abbonamento vuoi aggiungerlo ?", reply_markup=opzioni)


@bot.message_handler(commands=['sconto_utente'])
def sconto(message):
    opzioni = telebot.types.InlineKeyboardMarkup()
    for utente in Netflix:
        opzioni.add(telebot.types.InlineKeyboardButton(text=utente + "/Netflix", callback_data="['" + utente + "/Netflix_Sconto" + "']"))
    for utente in Disney:
        opzioni.add(telebot.types.InlineKeyboardButton(text=utente + "/Disney+", callback_data="['" + utente + "/Disney+_Sconto" + "']"))
    bot.send_message(message.chat.id, "A quale Utente ti riferisci ?", reply_markup=opzioni)

@bot.message_handler(commands=['reset'])
def reset():
    for utente in utenti:
        for abbonamento in utente.get_abbonamenti.keys():
            utente.get_abbonamenti[abbonamento] = 0

def create_message_automatic(Set,text):
    app = text + ":\n\n"
    for utente in utenti:
        if utente.get_name() in Set:
            app += utente.get_name() + " " + "%0.2f" % utente.get_abbonamenti()[text] + " €\n"
    app += "\n"
    return app

def automatic():
    while True:
        if (datetime.date.today().day == rinnovo_netflix.day):
            calculate_subscription(Netflix,calculate_amount(Netflix_price,Netflix),Netflix_name)
            text = "Giorno " + datetime.date.today().strftime("%d/%m/%Y") + " (Rinnovo Netflix) :\n\n" + create_message_automatic(Netflix,Netflix_name)
            bot.send_message(id, text)
        if(datetime.date.today().day == rinnovo_disney.day):
            calculate_subscription(Disney,calculate_amount(Disney_price,Disney),Disney_name)
            text = "Giorno " + datetime.date.today().strftime("%d/%m/%Y") + " (Rinnovo Disney+) :\n\n" + create_message_automatic(Disney,Disney_name)
            bot.send_message(id, text)
        sleep(86400)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global utenti
    #Rinnovo Netflix
    if (call.data == "['0']"):
        calculate_subscription(Netflix,calculate_amount(Netflix_price,Netflix),Netflix_name)
    #Rinnovo Disney+
    if (call.data == "['1']"):
        calculate_subscription(Disney,calculate_amount(Disney_price,Disney),Disney_name)
    #Aggiunta Utente Netflix
    if (call.data == "['2']"):
        temp = False
        for utente in utenti:
            if utente.get_name() == nuovo_utente:
                temp = True
                if "Netflix" not in utente.get_abbonamenti():
                    utente.get_abbonamenti()["Netflix"]=0
                    Netflix.add(nuovo_utente)
        if temp == False:
            app = user(nuovo_utente, {"Netflix": 0})
            utenti.add(app)
            Netflix.add(app.get_name())
    #Aggiunta Utente Disney+
    if (call.data == "['3']"):
        temp = False
        for utente in utenti:
            if utente.get_name() == nuovo_utente:
                temp = True
                if "Disney+" not in utente.get_abbonamenti():
                    utente.get_abbonamenti()["Disney+"] = 0
                    Disney.add(nuovo_utente)
        if temp == False:
            app = user(nuovo_utente, {"Disney+": 0})
            utenti.add(app)
            Disney.add(app.get_name())
    # Rimozione Utente
    for utente in utenti:
        if call.data == "['" + utente.get_name() + "/Disney+_Rimozione" + "']":
            utente.remove_abbonamenti("Disney+")
            Disney.remove(utente.get_name())
        if call.data == "['" + utente.get_name() + "/Netflix_Rimozione" + "']":
            utente.remove_abbonamenti("Netflix")
            Netflix.remove(utente.get_name())
        #ScontoUtente
        if call.data == "['" + utente.get_name() + "/Netflix_Sconto" + "']":
            utente.remove_soldi("Netflix",calculate_amount(Netflix_price,Netflix))
        if call.data == "['" + utente.get_name() + "/Disney+_Sconto" + "']":
            utente.remove_soldi("Disney+",calculate_amount(Disney_price,Disney))

t = Thread(target=automatic)
bot.infinity_polling()
