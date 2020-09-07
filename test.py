import telebot
import mysql.connector


#Подключение API-токена бота
bot = telebot.TeleBot("1307521740:AAEq4RrdvObH1RF1jp2QTJBAWFymqs99c2k", parse_mode='HTML')

#подключение БД
chekdb = mysql.connector.connect(
   user='root', password = 'root',
    host ='127.0.0.1',database='mydb'
)
if (ConnectionError == True):
    print("ERROR")
else:
    print ("Connection Succsses")

#создание курсора
mycursor = chekdb.cursor()

user_data = {} #Временное храненилище

class Chek: #Класс Чек с конструктором init
    def __init__(self, Name_chek):
        self.Name_chek = Name_chek
        self.Sum_chek = ''
        self.Status_chek = ''

@bot.message_handler(commands=['start']) #Обработчик на команду /start
def welcome_ch(message):
    bot.reply_to(message,'Вас приветствует бот чеков v.0.0.3\nВведите команду /insert или нажмите кнопку на экране')

@bot.message_handler(commands=['insert']) #Обработчик событий на команду insert
def begin_ch(message):
        msg = bot.send_message(message.chat.id, "Введите Наименование чека:")
        bot.register_next_step_handler(msg, sum_ch)

def sum_ch(message):
        user_id = message.from_user.id
        user_data[user_id] = Chek(message.text)

        msg = bot.send_message(message.chat.id, "Введите Сумму чека:")
        bot.register_next_step_handler(msg, status_ch)

def status_ch(message):
        user_id = message.from_user.id
        user = user_data[user_id]
        user.Sum_chek = message.text

        msg = bot.send_message(message.chat.id, "Введите статус чека:")
        bot.register_next_step_handler(msg,final_ch)
def final_ch(message):
        user_id = message.from_user.id
        user = user_data[user_id]
        user.Status_chek = message.text

        sql = "INSERT INTO cheki (User_ID, Name_chek, Sum, Status) \
                                  VALUES (%s, %s, %s, %s)" #SQL запрос
        val = (user_id, user.Name_chek, user.Sum_chek, user.Status_chek)
        mycursor.execute(sql, val)
        chekdb.commit()
        

bot.polling()



