import telebot
import pyowm

owm = pyowm.OWM('37656453f70fc458f65d30166b29610d')
mgr = owm.weather_manager()

bot = telebot.TeleBot("1866454392:AAEEKjhLRsYxH-fA7PLby3QJRGjDwQY1lu8")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Ну начнём, если хочешь узнать список комманди пиши "/help"')

@bot.message_handler(content_types=['text'])
def send_text(message):
    f = open('fails_log.txt', 'a')

    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    if str(l_name) == "None":
    	l_name = ''

    text = message.text
    text = text.lower()
    
    if text == 'привет':
        bot.send_message(message.chat.id, 'Привет!')
    elif text == 'пока':
        bot.send_message(message.chat.id, 'Пока')
    elif text == 'погода':
    	bot.send_message(message.chat.id, 'В каком городе?')
    	bot.register_next_step_handler(message, weather)

    elif message.text == '/help' or message.text == "help" or message.text == "помощь":
        bot.send_message(message.chat.id, 
        'Список доступных комманд (регистр не имеет значение):\n'
        'Привет\n'
        'Пока\n'
        'Погода\n')
    else:
        answer = 'Я тебя не понял!'
        bot.send_message(message.chat.id, answer)
        if len(text) < 100:
            f.write(str(f_name) + " " + str(l_name) + " | " + text + "\n")
        f.close()

def weather(message):
	try:
		text = message.text
		text = text.title()

		observation = mgr.weather_at_place(message.text)
		w = observation.weather

		#температура
		t = w.temperature("celsius")
		t_middle = t['temp']
		t_feels = t['feels_like']
		#скорость ветра
		wind = w.wind()['speed']
		#влажность
		h = w.humidity
		#время
		weather_time = w.reference_time('iso')

		answer = ('На момент ' + weather_time + '\nВ городе ' + text + ' сейчас ' + str(abs(int(t_middle))) + 
			'°C, ощущается как ' + str(abs(int(t_feels))) + '°C\nСкорость ветра ' + str(wind) + 
			'м/c, относительная влажность ' + str(h) + '%')
		
		bot.send_message(message.chat.id, answer)
	except pyowm.commons.exceptions.NotFoundError:
		bot.send_message(message.chat.id, 'Ошибка, город не найден')


bot.polling(none_stop=True)