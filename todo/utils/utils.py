import os
import json
from os.path import join, dirname, realpath
from random import randint, choice

from PIL import Image


def avatar_img(file, path):
    size = (80, 100)
    with Image.open(file) as f:
        f.thumbnail(size)
        f.save(path)

def answer_bal():
    dict_answ = None
    # path = join(dirname(realpath(__file__)), '..', 'ball_answers', 'answers.json')
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
    # return choice(answer)


if __name__ == '__main__':
    path = os.path.join(os.getcwd(), '..', 'static', 'ava.jpg')
    avatar_img('/home/dimon/Загрузки/1586360554_youloveit_ru_dipper_gravity_falls_na_avu01.jpg', path)