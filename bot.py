import vk_api
import os
import signal
from dotenv import load_dotenv

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def f(*args):
    print(args)
    print('hello')

signal.signal(signal.SIGINT, f)

signal.signal(signal.SIGINT, signal.default_int_handler)

load_dotenv()
token = os.getenv("ACCESS_TOKEN")
manager_id = os.getenv("USER_ID")
session = vk_api.VkApi(token=token)

def send_message(user_id, message, keyboard = None):
    post = {
        "user_id": user_id,
        "message": message,
        "random_id": 0
    }

    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    else:
        post = post

    session.method("messages.send", post)

for event in VkLongPoll(session).listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        text = event.text.lower()
        user_id = event.user_id

        keyboard = VkKeyboard()
        keyboard.add_button("%", VkKeyboardColor.NEGATIVE)
        keyboard.add_button("Индивидуальный пошив", VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_openlink_button("FAQ", link="https://vk.com/topic-221151816_49193909")

        if text == "начать":
            send_message(user_id, "Добро пожаловать в нашу группу, где искусство встречается с модой, а вдохновение берется из различных уголков эстетики. Мы предлагаем эксклюзивные вещи как из готовой линейки, вдохновленные такими направлениями, как Goblincore, Dark Academia, Cottagecore и многими другими, так и вещи сделанные на заказ по вашим требованиям. Здесь каждая вещь - это не просто предмет гардероба, это отражение вашего уникального 'я '. Погрузитесь в мир, где стиль говорит громче слов.", keyboard)
            send_message(user_id, "Есть какие-то вопросы? Без стеснений пишите в личные сообщения группы.", keyboard)

        elif text == "индивидуальный пошив":
            send_message(user_id, "Хотите что-то поистине уникальное, что-то? Что-то, что будет олицетворять вашу Вселенную? \n Вы обратились по адресу! Опишите, что выхотите изменить в готовой продукции и мы с радостью поможем вам воплотить в жизнь ваши фантазии!", keyboard)
            send_message(user_id, "Подождите, с вами свяжеться менеджер, чтобы уточнить все детали", keyboard)
            send_message(manager_id, "Заявка на индивидуальный пошив", keyboard)
        elif text == "%":
            send_message(user_id, "Скидка 10% по промокоду NEWUNIVERSE для новых покупателей", keyboard)
