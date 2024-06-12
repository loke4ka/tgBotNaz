import telebot
from telebot import types

# Токен вашего бота
TOKEN = '6350949385:AAGcYHouQ0H0nF526ut-CMk1pV_jvmfwTeI'

bot = telebot.TeleBot(TOKEN)

def start_message(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('🇷🇺 Русский', '🇰🇿 Казахский', '🇺🇸 English')
    bot.send_message(chat_id, "Здравствуйте!\nВыберите язык обращения!\n\n"
                              "Сәлеметсіз бе!\nТілді таңдаңыз!\n\n"
                              "Hello!\nChoose language!", reply_markup=markup)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    start_message(message.chat.id)

@bot.message_handler(func=lambda message: message.text.lower() in ['привет', 'здравствуйте'])
def greet(message):
    start_message(message.chat.id)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "Список доступных команд:\n"
    help_text += "/start - начать диалог\n"
    help_text += "/help - помощь по командам\n"
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(func=lambda message: message.text in ['🇷🇺 Русский', '🇰🇿 Казахский', '🇺🇸 English'])
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('Абитуриент/Родитель', 'Иностранный абитуриент')
    markup.row('Студент', 'Номер специалиста')
    markup.row('Назад')
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Назад')
def go_back(message):
    if message.chat.id in previous_menu:
        previous_menu[message.chat.id](message)
    else:
        start_message(message.chat.id)

@bot.message_handler(func=lambda message: message.text in ['Абитуриент/Родитель', 'Иностранный абитуриент'])
def handle_category(message):
    save_previous_menu(message, main_menu)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('Поступление', 'Перевод с другого ВУЗа')
    markup.row('Назад')
    bot.send_message(message.chat.id, "Что Вас интересует?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Студент')
def student_menu(message):
    admission_menu(message)

@bot.message_handler(func=lambda message: message.text == 'Номер специалиста')
def specialist_number(message):
    save_previous_menu(message, main_menu)
    bot.send_message(message.chat.id, "Контактный номер приемной комиссии: +123456789. Вы можете звонить по рабочим дням с 9 до 18.")
    add_back_button(message)

@bot.message_handler(func=lambda message: message.text == 'Поступление')
def admission_menu(message):
    save_previous_menu(message, handle_category)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('Бакалавриат', 'Магистратура', 'Докторантура')
    markup.row('Назад')
    bot.send_message(message.chat.id, "Куда Вы хотите поступить?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Бакалавриат', 'Магистратура', 'Докторантура'])
def degree_selection(message):
    save_previous_menu(message, admission_menu)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('Первое высшее, после школы', 'Второе высшее, после университета')
    markup.row('Первое высшее, после колледжа')
    markup.row('Назад')
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Первое высшее, после школы', 'Второе высшее, после университета', 'Первое высшее, после колледжа'])
def provide_admission_info(message):
    save_previous_menu(message, degree_selection)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('Перечень документов', 'Адрес и график работы')
    markup.row('Важные даты', 'Цены за обучение')
    markup.row('Перечень специальностей', 'Военная кафедра')
    markup.row('Назад')
    bot.send_message(message.chat.id, "Что Вас интересует?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Перечень документов')
def documents_list(message):
    save_previous_menu(message, provide_admission_info)
    bot.send_message(message.chat.id, 
        "Аттестат/диплом с приложением (оригинал)\n"
        "Сертификат ЕНТ (эл.документ. с сайта certificate.testcenter.kz)\n"
        "2 копии удостоверения личности\n"
        "8 фото 3х4 (каждое фото подписать с обратной стороны)\n"
        "Мед. справка 075/У (со снимком флюорографии сроком не более 12 месяцев на дату зачисления 20.08.2021)\n"
        "Карта профилактических прививок (форма 063/У) - находится в Паспорте здоровья ребенка\n"
        "Копия приписного свидетельства (для юношей)\n"
        "Копия грамот и дипломов за последние три года (призовые места в значимых мероприятиях), сертификатов (IELTS 5.0+, TOEFL 35+)"
    )
    add_back_button(message)

@bot.message_handler(func=lambda message: message.text == 'Адрес и график работы')
def working_hours(message):
    save_previous_menu(message, provide_admission_info)
    bot.send_message(message.chat.id, 
        "График работы:\n"
        "Понедельник-пятница\n"
        "с 9:00 до 18:00\n"
        "(Суббота и Воскресенье-Выходные)\n"
        "Адрес:\n"
        "Город Алматы, Манаса 34/1"
    )
    add_back_button(message)

@bot.message_handler(func=lambda message: message.text == 'Важные даты')
def important_dates(message):
    save_previous_menu(message, provide_admission_info)
    bot.send_message(message.chat.id, 
        "- Регистрация на ЕНТ с 28 апреля до 14 мая\n"
        "- Работа Приемной комиссии с 20 июня до 25 августа\n"
        "- Сдача экзамена по Английскому языку с 20 июня до 25 августа\n"
        "- Сдача документов с 20 июня до 20 июля\n"
        "- Регистрация на конкурс грантов с 13 июля по 20 июля\n"
        "- Подписание договора с 15 августа до 25 августа\n"
        "- Прием заявлений на платное отделение с 20 июня до 25 августа."
    )
    add_back_button(message)

@bot.message_handler(func=lambda message: message.text == 'Цены за обучение')
def tuition_fees(message):
    save_previous_menu(message, provide_admission_info)
    bot.send_message(message.chat.id, 
        "Журналистика и репортерское дело\n"
        "1 курс - 1 150 000\n"
        "2 курс - 1 200 000\n"
        "3 курс - 1 250 000\n"
        "4 курс - 1 300 000\n"
        "Итог - 4 900 000"
    )
    add_back_button(message)

def add_back_button(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('Назад')
    bot.send_message(message.chat.id, "Назад", reply_markup=markup)

previous_menu = {}

def save_previous_menu(message, previous_handler):
    previous_menu[message.chat.id] = previous_handler

# Запуск бота
bot.polling(none_stop=True)