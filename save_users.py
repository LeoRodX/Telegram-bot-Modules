# Собирает user_id и при старте скрипт, после старта скрипт отправляет всем сообщение
# user.json создается сам
import telebot
import json

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
bot = telebot.TeleBot('MY_TOKEN')

# Имя файла для хранения данных
USER_DATA_FILE = 'users.json'

# Загружаем существующие данные о пользователях
try:
    with open(USER_DATA_FILE, 'r', encoding='utf-8') as file:
        users_data = json.load(file)
except FileNotFoundError:
    users_data = {}

# Функция для сохранения данных в JSON
def save_users_data():
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(users_data, file, ensure_ascii=False, indent=4)

# Загружаем данные о пользователях
try:
    with open(USER_DATA_FILE, 'r', encoding='utf-8') as file:
        users_data = json.load(file)
except FileNotFoundError:
    print("Файл с данными о пользователях не найден!")
    users_data = {}

# Функция для отправки сообщения всем пользователям
def send_message_to_all_users(message_text):
    for user_id, user_info in users_data.items():
        try:
            # Отправляем сообщение
            bot.send_message(user_info['chat_id'], message_text)
            print(f"Сообщение отправлено пользователю {user_info['username']} (ID: {user_id})")
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_info['username']} (ID: {user_id}): {e}")

# Обработчик нового участника группы
@bot.message_handler(content_types=['new_chat_members'])
def handle_new_member(message):
    for user in message.new_chat_members:
        user_id = user.id
        username = user.username if user.username else "No username"
        first_name = user.first_name if user.first_name else "No first name"
        last_name = user.last_name if user.last_name else "No last name"

        # Добавляем пользователя в данные, если его еще нет
        if str(user_id) not in users_data:
            users_data[str(user_id)] = {
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'chat_id': message.chat.id
            }
            save_users_data()
            print(f"Новый пользователь добавлен: {username} (ID: {user_id})")

# Обработчик личных сообщений (если пользователь начинает диалог с ботом)
@bot.message_handler(func=lambda message: True)
def handle_private_message(message):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "No username"
    first_name = message.from_user.first_name if message.from_user.first_name else "No first name"
    last_name = message.from_user.last_name if message.from_user.last_name else "No last name"

    # Добавляем пользователя в данные, если его еще нет
    if str(user_id) not in users_data:
        users_data[str(user_id)] = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'chat_id': message.chat.id
        }
        save_users_data()
        print(f"Новый пользователь добавлен: {username} (ID: {user_id})")

# Пример использования
if __name__ == "__main__":
    # Текст сообщения, которое вы хотите отправить
    message_text = "Привет! Это массовая рассылка от бота."

    # Отправляем сообщение всем пользователям
    send_message_to_all_users(message_text)

# Запуск бота
print("Бот запущен...")
bot.polling(none_stop=True)
