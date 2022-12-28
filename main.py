# -*- coding: utf-8 -*-
# Главный модуль бота

import telebot
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot("TOKEN")

bot_name = 'Курсобот'

url = 'https://www.cbr-xml-daily.ru/daily_utf8.xml'

response = requests.get(url)

response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, 'xml')

curlist = str(soup.find_all('CharCode')).replace('<CharCode>', '').replace('</CharCode>', '').replace('[', '').replace(']', '')

curlist = list(curlist.split(', '))

exchlist = str(soup.find_all('Value')).replace('<Value>', '').replace('</Value>', '').replace('[', '').replace(']', '')

exchlist = list(exchlist.split(', '))
    
namelist = str(soup.find_all('Name')).replace('<Name>', '').replace('</Name>', '').replace('[', '').replace(']', '')

namelist = list(namelist.split(', '))

reslist = [(x,y,z) for x,y,z in zip(curlist, exchlist, namelist)]

def command_handler(message):

    """Функция обрабатывает ввод пользователя"""

    global currency, curlist

    if currency == False:

        return False

    if currency == True:

        if any(obj == message.text for obj in curlist):

                return True

        else:
            
            bot.send_message(message.chat.id,f'{message.from_user.first_name}, в списке нет такой валюты, попробуй еще раз!')
            
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

@bot.message_handler(commands=['currency'])
def help_command(message) -> str:

    """Запуск поиска курса обмена"""

    global currency, curlist

    info = ', '.join(curlist)

    bot.send_message(message.chat.id,f'Для отображения курса валюты напиши боту код валюты. На данный момент доступны следующие коды валют: {info}.')

    currency = True

@bot.message_handler(func=command_handler)
def course_currency(message):
    
    """Обработчик команд пользователя"""

    global currency, reslist

    course = list(filter(lambda k: message.text in k, reslist))[0]

    name = str(course[2])

    course = round(float(str(course[1]).replace(',', '.')), 2)

    bot.send_message(message.chat.id,f'Курс {name} составляет {course} ₽.')

    bot.send_message(message.chat.id,f'Для повторного запроса, выполни команду /currency.')
 
    currency = False

print('Telegram bot server is in running state...')

bot.infinity_polling()