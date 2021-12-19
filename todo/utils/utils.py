import os

from PIL import Image


def avatar_img(file, path):
    size = (80, 100)
    with Image.open(file) as f:
        f.thumbnail(size)
        f.save(path)


if __name__ == '__main__':
    path = os.path.join(os.getcwd(), '..', 'static', 'ava.jpg')
    avatar_img('/home/dimon/Загрузки/1586360554_youloveit_ru_dipper_gravity_falls_na_avu01.jpg', path)