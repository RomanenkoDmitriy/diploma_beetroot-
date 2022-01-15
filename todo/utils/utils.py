import os
import json
from random import randint, choice

from PIL import Image

from todo import logger, app


def avatar_img(file, path):
    size = (80, 100)
    with Image.open(file) as f:
        f.thumbnail(size)
        f.save(path)

def answer_bal():
    dict_answ = None
    path = os.path.abspath('ball_answers/answers.json')
    with open(path, 'r') as file:
        dict_answ = json.load(file)
    rand_val = randint(1, 100)
    answer = None
    if 1 <= rand_val <= 40:
        answer = dict_answ['positive']
        return choice(dict_answ['positive'])
    elif 41 <= rand_val <= 70:
        answer = dict_answ['neutral']
        return choice(dict_answ['neutral'])
    else:
        answer = dict_answ['negative']
        return choice(dict_answ['negative'])


def my_login_decorator(func):
    try:
        def wrapper(*args):
            return func(*args)
        app.logger.info(f'{func.__name__} OK')
    except Exception as e:
        app.logger.error(str(e))
    return wrapper


if __name__ == '__main__':
    path = os.path.join(os.getcwd(), '..', 'static', 'ava.jpg')
    avatar_img('/home/dimon/Загрузки/1586360554_youloveit_ru_dipper_gravity_falls_na_avu01.jpg', path)