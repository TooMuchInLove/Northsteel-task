# -*- coding: utf-8 -*-

from sqlite3 import connect
from sqlite3 import Error as SQLiteError

from config import NAME_TABLE_IMAGES

# Строковые данные
StrData = str
# Данные в виде списка
ListData = list


class Storage:
    """ Интерфейс для любого хранилища """
    def connection(self) -> None:
        pass

    def save(self, _data: ListData) -> None:
        pass

    def read(self) -> ListData:
        pass


class StorageSQL(Storage):
    """ Хранилище данных в табличном формате """
    def create_table(self) -> None:
        pass


class DBSQLite3(StorageSQL):
    """ База данных SQLite3 (временное хранилище) """
    def __init__(self, _name_db: StrData) -> None:
        # Название хранилища
        self.__name_db = _name_db
        # Подключение к базе
        self.connection()
        # Создание таблиц
        self.create_table()

    def connection(self) -> None:
        try:
            # Подключение к базе
            self.__connect = connect(self.__name_db)
            # Создание курсора для запросов в базу
            self.__cursor = self.__connect.cursor()
        except SQLiteError as error:
            print(error)

    def create_table(self) -> None:
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS %s(
                id INTEGER PRIMARY KEY,
                bsize INTEGER,
                datetime TEXT
            );
        """ % (NAME_TABLE_IMAGES))

    def save(self, _data: ListData) -> None:
        self.__cursor.execute(
            "INSERT or IGNORE INTO %s VALUES (?, ?, ?);" % (NAME_TABLE_IMAGES), (_data)
        )

    def read(self) -> ListData:
        data = []
        self.__cursor.execute("SELECT bsize, datetime FROM %s;" % (NAME_TABLE_IMAGES))
        for item in self.__cursor.fetchall():
            data.append(item)
        return data

    def __del__(self):
        # Разрываем соединение с базой
        self.__connect.close()


def save_data(_data: ListData, _storage: Storage) -> None:
    _storage.save(_data)


def read_data(_storage: Storage) -> ListData:
    return _storage.read()
