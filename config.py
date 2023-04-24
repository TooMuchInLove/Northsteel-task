# -*- coding: utf-8 -*-

from os import getcwd as os_get_cwd

# Место хранения изображений (название директории)
FOLDER_IMG = "imgs"

# Путь до рабочей директории
MAIN_PATH = os_get_cwd() + "\\"

# Путь до директории с изображениями
PATH_IMG = MAIN_PATH + FOLDER_IMG + "\\"

# Название хранилища данных (SQLite3 БД)
NAME_DB_SQLITE = "image_data.db"

# Название таблицы в хранилище (SQLite3 БД)
NAME_TABLE_IMAGES = "image"
