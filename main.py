# coding=utf-8
import telebot
#pip install pyTelegramBotAPI
#pip install python-dotenv
#from telebot.types import CallbackQuery
import datetime
from user import user
from threading import Thread
from time import sleep
import os
import re
from dotenv import load_dotenv
load_dotenv()

apiKey = os.getenv('API_KEY')

bot = telebot.TeleBot(apiKey)

Domenico = user("Domenico", {"Netflix": 0, "Disney+": 0})
Gaetano = user("Gaetano", {"Netflix": 0, "Disney+": 0})
Dominic = user("Dominic", {"Netflix": 0, "Disney+": 0})
Chiara = user("Chiara", {"Netflix": 0, "Disney+": 0})

utenti = {Domenico, Gaetano, Dominic, Chiara}

Netflix = {Domenico.get_name(), Gaetano.get_name(), Dominic.get_name(), Chiara.get_name()}

Disney = set()

rinnovo_netflix=datetime.date(2021,12,9)
rinnovo_disney=datetime.date(2021,12,23)

abbonamenti = {"Netflix":0,"Disney+":1}

Netflix_price = 20

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
            if utente.get_name() == nome and utente.get_name() != "Domenico":
                utente.add_amount(name, price)

def create_message():
    if bool(Netflix):
        text = "Netflix:\n\n"
    for utente in utenti:
        if utente.get_name() in Netflix:
            text += utente.get_name() + " " + "%0.2f" % utente.get_abbonamenti()["Netflix"] + " €\n"
    text += "\n"
    if bool(Disney):
        text += "Disney+:\n\n"
    for utente in utenti:
        if utente.get_name() in Disney:
            text += utente.get_name() + " " + "%0.2f" % utente.get_abbonamenti()["Disney+"] + " €\n"
    text += "\n"
    if bool(Netflix) and bool(Disney):
        text += "Totale Quote:\n\n"
        for utente in utenti:
            text += utente.__str__()
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

@bot.message_handler(commands=['aggiunta_rimozione_importo'])
def aggiungi(message):
    app = bot.reply_to(message,"Inserire l'importo da aggiungere (positivo) o rimuovere (negativo) all'utente:")
    bot.register_next_step_handler(app,handle_amount)
    
def handle_amount(message):
    try:
        # Try to convert the user input to float
        amount = float(message.text)
        # If successful, go on
        amount = message.text
        opzioni = telebot.types.InlineKeyboardMarkup()
        for utente in Netflix:
            opzioni.add(telebot.types.InlineKeyboardButton(text=utente + "/Netflix", callback_data="['" + utente + "/Netflix_Amount:" + amount + "']"))
        for utente in Disney:
            opzioni.add(telebot.types.InlineKeyboardButton(text=utente + "/Disney+", callback_data="['" + utente + "/Disney+_Amount:" + amount + "']"))
        bot.send_message(message.chat.id, "A quale Utente ti riferisci ?", reply_markup=opzioni)
    except ValueError:
        # If conversion fails, inform the user
        bot.reply_to(message, "Errore: l'importo deve essere un numero.")

@bot.message_handler(commands=['cambio_prezzo_abbonamento'])
def aggiungi(message):
    app = bot.reply_to(message,"Inserire il nuovo importo dell'abbonamento:")
    bot.register_next_step_handler(app,handle_subscription)
    
def handle_subscription(message):
    try:
        # Try to convert the user input to float
        amount = float(message.text)
        if amount <= 0:
            bot.reply_to(message, "Errore: l'importo deve essere maggiore di 0.")
            return
        # If successful, go on
        amount = message.text
        opzioni = telebot.types.InlineKeyboardMarkup()
        opzioni.add(telebot.types.InlineKeyboardButton(text="Netflix", callback_data="['" + "/Netflix_Subscription:" + amount + "']"))
        opzioni.add(telebot.types.InlineKeyboardButton(text="Disney+", callback_data="['" + "/Disney+_Subscription:" + amount + "']"))
        bot.send_message(message.chat.id, "A quale Abbonamento ti riferisci ?", reply_markup=opzioni)
    except ValueError:
        # If conversion fails, inform the user
        bot.reply_to(message, "Errore: l'importo deve essere un numero.")

@bot.message_handler(commands=['sconto_utente'])
def sconto(message):
    opzioni = telebot.types.InlineKeyboardMarkup()
    for utente in Netflix:
        opzioni.add(telebot.types.InlineKeyboardButton(text=utente + "/Netflix", callback_data="['" + utente + "/Netflix_Sconto" + "']"))
    for utente in Disney:
        opzioni.add(telebot.types.InlineKeyboardButton(text=utente + "/Disney+", callback_data="['" + utente + "/Disney+_Sconto" + "']"))
    bot.send_message(message.chat.id, "A quale Utente ti riferisci ?", reply_markup=opzioni)

def create_message_automatic(Set,text):
    app = text + ":\n\n"
    for utente in utenti:
        if utente.get_name() in Set:
            app += utente.get_name() + " " + "%0.2f" % utente.get_abbonamenti()[text] + " €\n"
    app += "\n"
    return app

def automatic(activeNetflix,activeDisney):
    while True:
        if (activeNetflix and datetime.date.today().day == rinnovo_netflix.day):
            calculate_subscription(Netflix,calculate_amount(Netflix_price,Netflix),Netflix_name)
            text = "Giorno " + datetime.date.today().strftime("%d/%m/%Y") + " (Rinnovo Netflix) :\n\n" + create_message_automatic(Netflix,Netflix_name)
            bot.send_message(id, text)
        if(activeDisney and datetime.date.today().day == rinnovo_disney.day):
            calculate_subscription(Disney,calculate_amount(Disney_price,Disney),Disney_name)
            text = "Giorno " + datetime.date.today().strftime("%d/%m/%Y") + " (Rinnovo Disney+) :\n\n" + create_message_automatic(Disney,Disney_name)
            bot.send_message(id, text)
        sleep(86400)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global utenti
    global Netflix_price
    global Disney_price
    #Rinnovo Netflix
    if (call.data == "['0']"):
        calculate_subscription(Netflix,calculate_amount(Netflix_price,Netflix),Netflix_name)
        bot.answer_callback_query(call.id,"Abbonamento " + Netflix_name + " Rinnovato")
    #Rinnovo Disney+
    if (call.data == "['1']"):
        calculate_subscription(Disney,calculate_amount(Disney_price,Disney),Disney_name)
        bot.answer_callback_query(call.id,"Abbonamento " + Disney_name + " Rinnovato")
    #Cambio Prezzo Abbomamento Netflix
    matchNetflixSubscription = re.search(r"\['/Netflix_Subscription:([-+]?\d*\.?\d+)\']", call.data)
    if matchNetflixSubscription:
        newNetflixPrice = float(matchNetflixSubscription.group(1))
        Netflix_price = newNetflixPrice
        bot.answer_callback_query(call.id,"Prezzo " + Netflix_name + " Cambiato.")
    #Cambio Prezzo Abbomamento Disney+
    matchDisneySubscription = re.search(r"\['/Disney\+_Subscription:([-+]?\d*\.?\d+)\']", call.data)
    if matchDisneySubscription:
        newDisneyPrice = float(matchDisneySubscription.group(1))
        Disney_price = newDisneyPrice
        bot.answer_callback_query(call.id,"Prezzo " + Disney_name + " Cambiato.")
    #Aggiunta Utente Netflix
    if (call.data == "['2']"):
        user_already_created = False
        for utente in utenti:
            if utente.get_name() == nuovo_utente:
                user_already_created = True
                if "Netflix" not in utente.get_abbonamenti():
                    utente.get_abbonamenti()["Netflix"]=0
                    Netflix.add(nuovo_utente)
        if not user_already_created:
            app = user(nuovo_utente, {"Netflix": 0})
            utenti.add(app)
            Netflix.add(app.get_name())
        bot.answer_callback_query(call.id,"Utente " + nuovo_utente + " Aggiunto a " + Netflix_name)
    #Aggiunta Utente Disney+
    if (call.data == "['3']"):
        user_already_created = False
        for utente in utenti:
            if utente.get_name() == nuovo_utente:
                user_already_created = True
                if "Disney+" not in utente.get_abbonamenti():
                    utente.get_abbonamenti()["Disney+"] = 0
                    Disney.add(nuovo_utente)
        if not user_already_created:
            app = user(nuovo_utente, {"Disney+": 0})
            utenti.add(app)
            Disney.add(app.get_name())
        bot.answer_callback_query(call.id,"Utente " + nuovo_utente + " Aggiunto a " + Disney_name)
    # Rimozione Utente
    for utente in utenti.copy():
        if call.data == "['" + utente.get_name() + "/Disney+_Rimozione" + "']":
            utente.remove_abbonamenti("Disney+")
            Disney.remove(utente.get_name())
            if (utente.empty_abbonamenti()):
                utenti.remove(utente)
            bot.answer_callback_query(call.id,"Utente " + utente.get_name() + " Rimosso da " + Disney_name)
        if call.data == "['" + utente.get_name() + "/Netflix_Rimozione" + "']":
            utente.remove_abbonamenti("Netflix")
            Netflix.remove(utente.get_name())
            if (utente.empty_abbonamenti()):
                utenti.remove(utente)
            bot.answer_callback_query(call.id,"Utente " + utente.get_name() + " Rimosso da " + Netflix_name)
        #ScontoUtente
        if call.data == "['" + utente.get_name() + "/Netflix_Sconto" + "']":
            utente.remove_amount("Netflix",calculate_amount(Netflix_price,Netflix))
            bot.answer_callback_query(call.id,"Abbonamento " + Netflix_name + " Scontato a " + utente.get_name())
        if call.data == "['" + utente.get_name() + "/Disney+_Sconto" + "']":
            utente.remove_amount("Disney+",calculate_amount(Disney_price,Disney))
            bot.answer_callback_query(call.id,"Abbonamento " + Disney_name + " Scontato a " + utente.get_name())
        #Aggiunta/Rimozione Importo
        # Search for user and amount into the reply
        matchNetflix = re.search(r"\['(.+?)/Netflix_Amount:([-+]?\d*\.?\d+)\']", call.data)
        if matchNetflix:
            userName = matchNetflix.group(1)  # The 'utente' part before the slash
            amount = float(matchNetflix.group(2))  # The 'amount' part after Netflix_Amount:
            # check it is the user I want to add the amount to, then call add or remove depending on the sign
            if utente.get_name() == userName:
                if amount >= 0:
                    utente.add_amount("Netflix",float(amount))
                    bot.answer_callback_query(call.id,"Aggiunto " + str(amount) + " € a " + utente.get_name() + " per " + Netflix_name)
                else:
                    utente.remove_amount("Netflix",float(-amount))
                    bot.answer_callback_query(call.id,"Rimosso " + str(amount) + " € a " + utente.get_name() + " per " + Netflix_name)
        # Search for user and amount into the reply for Disney+
        matchDisney = re.search(r"\['(.+?)/Disney\+_Amount:([-+]?\d*\.?\d+)\']", call.data)
        if matchDisney:
            userName = matchDisney.group(1)  # The 'utente' part before the slash
            amount = float(matchDisney.group(2))  # The 'amount' part after Disney+_Amount:
            # check it is the user I want to add the amount to, then call add or remove depending on the sign
            if utente.get_name() == userName:
                if amount >= 0:
                    utente.add_amount("Disney+", float(amount))
                    bot.answer_callback_query(call.id, "Aggiunto " + str(amount) + " € a " + utente.get_name() + " per " + Disney_name)
                else:
                    utente.remove_amount("Disney+", float(-amount))
                    bot.answer_callback_query(call.id, "Rimosso " + str(amount) + " € a " + utente.get_name() + " per " + Disney_name)    

t = Thread(target=automatic, args=(bool(Netflix),bool(Disney)))
bot.infinity_polling(timeout=10, long_polling_timeout = 5)
#bot.polling()