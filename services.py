# -*- coding: utf-8 -*-

from os import listdir as os_list_dir
from os import stat as os_stat

from typing import Dict

from multiprocessing import Queue

from datetime import datetime

from config import PATH_IMG
from config import NAME_DB_SQLITE

from logging_ import Storage
from logging_ import DBSQLite3
from logging_ import save_data
from logging_ import read_data

# Словарь с данным о изображениях
DictImgs = Dict[str, Dict]
# Формат даты и времени
DateAndTime = str


def get_dict_images() -> DictImgs:
    """ Получаем словарь с данным о изображениях (название, размер, дата) """
    images = {}
    for name in os_list_dir(PATH_IMG):
        images[name] = {
            # Размер изображения в байтах
            "bsize": os_stat(PATH_IMG+name).st_size,
            # Дата сохранения изображения
            "datetime": get_datetime_now()
        }
    return images


def get_datetime_now() -> DateAndTime:
    """ Получаем текущую дату и время в формате <<20.04.2023 01:52:00>> """
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")


def create_db(length: int, queue: Queue):
    # Создаём хранилище
    db_sqlite3 = DBSQLite3(NAME_DB_SQLITE)
    # Достаём данные из очереди и записываем в БД
    image_in_db(length, db_sqlite3, queue)


def image_in_queue(length: int, images: DictImgs, queue: Queue):
    # Счётчик изображений
    next_img = 0
    # Список ключей (названия изображений)
    list_names = list(images.keys())
    # Запускаем цикл для добавления данных в очередь
    while next_img < length:
        # Название изображения
        name = list_names[next_img]
        # Загружаем данные по изображению в очередь
        queue.put((name, images[name]))
        next_img += 1
    # print("End.")


def image_in_db(length: int, db: Storage, queue: Queue):
    for i in range(length):
        # Достаём данные из очереди
        data = [i] + list(queue.get()[1].values())
        # Формируем данные для записи в БД
        save_data(data, db)
    # Чтение данных из хранилища
    print(read_data(db))
