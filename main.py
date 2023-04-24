# -*- coding: utf-8 -*-

from multiprocessing import Process
from multiprocessing import Queue

from services import get_dict_images
from services import image_in_queue
from services import create_db


if __name__ == "__main__":
    # Получаем информацию о изображениях
    images = get_dict_images()
    # Количество данных о каждом изображении
    length = len(images)
    # Создаём очередь
    queue = Queue()
    # Создаём процессы
    p1 = Process(target=image_in_queue, args=(length, images, queue))
    p2 = Process(target=create_db, args=(length, queue))
    # Запуск процесса 1 & 2
    p1.start()
    p2.start()
    # try:
    #     for _ in range(10):
    #         print(queue.get(timeout=1))
    # except Empty as err:
    #     print("Empty queue.")
    # except EOFError as err:
    #     print("Закончились входные данные.")
    p1.join()
    p2.join()

# Многопоточность
# GIL (Global Interpreter Lock) Глобальная блокировка интерпретатора
#
#   Теперь мы говорим, что сколько бы у нас не было потоков в нашей программе,
# но выполняться в конкретный момент времени будет только один из них!
#
# [Поток : Процесс]
#   Поток - это более легковесный процесс.
# 1. Потоки живут внутри процессов;
# 2. Потоки пораждаются процессами;
# 3. Потоки выгодны с точки зрения ресурсов и затрат;
#