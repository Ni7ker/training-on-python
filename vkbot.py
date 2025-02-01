import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# Токен доступа и ID группы
TOKEN = "YOUR_ACCESS_TOKEN"
GROUP_ID = "YOUR_GROUP_ID"

# Авторизация
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)


def send_message(user_id, message, attachment=None):
    """Отправка сообщения пользователю"""
    vk.messages.send(user_id=user_id, message=message, attachment=attachment, random_id=0)


def handle_new_message(event):
    """Обработка входящих сообщений"""
    user_id = event.object.message['from_id']
    message_text = event.object.message.get('text', '')
    attachments = event.object.message.get('attachments', [])

    # Если пользователь пишет впервые, отправляем приветственное сообщение
    if message_text.lower() == "начать" or message_text.lower() == "привет":
        send_message(user_id, "Добро пожаловать! Отправьте мне изображение.")

    # Проверяем, есть ли в сообщении изображение
    elif attachments and attachments[0]['type'] == 'photo':
        photo = attachments[0]['photo']
        largest_photo = max(photo['sizes'], key=lambda size: size['height'])  # Берем фото лучшего качества
        photo_url = largest_photo['url']

        send_message(user_id, "Вот ваше изображение обратно:", attachment=photo_url)

    # Игнорируем все другие сообщения
    else:
        pass


# Основной цикл
print("Бот запущен...")
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        handle_new_message(event)
