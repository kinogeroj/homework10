import telebot
import requests
from bs4 import BeautifulSoup
import lxml

bot = telebot.TeleBot("5964599176:AAFMY94KAXcOdBx1d-Xfi_XMMUWq468HyMg")

bot_name = 'Курсобот'

url = 'https://www.cbr-xml-daily.ru/daily_utf8.xml'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'lxml')

curlist = []

currencies = soup.find_all("cube", currency=True)

print(currencies)

for i in currencies:
    
    for x in i('cube'):
        
        for y in x:
            
            if y.name == 'cube':

                curlist.append(y[currencies])

print(curlist)

def command_handler(message):

    """Функция обрабатывает ввод пользователя"""

    global currency, curlist
    
    if currency == False:

        return False

    if currency == True:

        for k in curlist:

            if message.text == curlist[k]:

                return True

    else:
        
        bot.send_message(message.chat.id,f'{message.from_user.first_name}, я не знаю такой валюты, попробуй еще раз!')

        return False

@bot.message_handler(commands=['start'])
def start_message(message) -> str:
    
    """Функция приветствия пользователя"""

    bot.send_message(message.chat.id,f'\nПривет, {message.from_user.first_name}, я {bot_name}!\nПришли команду /help, чтобы узнать справку по меню.')

@bot.message_handler(commands=['help'])
def help_command(message) -> str:

    """Функция помощи по меню"""

    global currency

    bot.send_message(message.chat.id, 'Для отображения всех курсов выполни команду /currency.\n' +
       'После этого введи код валюты, например, USD или EUR.\n' +
       'В ответ отобразится информация по валюте, в виде ее обменного курса покупки в рублях на текущую дату.')

    currency = True

@bot.message_handler(func=command_handler)
def currency(message):
    
    
    
    bot.send_message(message.chat.id,f'{message.from_user.first_name}, чтобы узнать курс другой валюты, снова выполни команду /currency и код валюты.')

    currency = False


print('Telegram bot server is in running state...')

bot.infinity_polling()