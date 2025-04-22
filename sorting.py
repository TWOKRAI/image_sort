import random

import time


class Timer:
    def __init__(self, name):
        self.name = name
        self.start_time = None


    def start(self):
        """Начинает отсчет времени и сохраняет текущее время в атрибут start_time."""
        self.start_time = time.time()
        #print(f"Таймер {self.name} запущен")


    def elapsed_time(self, print_log=False):
        """Возвращает количество секунд, прошедших с момента запуска таймера."""
        if self.start_time is None:
            #print(f"Таймер {self.name} не был запущен.")
            return 0
        
        elapsed = time.time() - self.start_time

        if print_log:
            print(f"Таймер {self.name} {elapsed * 1000} мс")
        
        return elapsed



def generate_and_shuffle(start, end):
    # Генерация списка чисел от start до end
    numbers = list(range(start, end + 1))
    # Перемешивание списка
    random.shuffle(numbers)
    return numbers


shuffled_numbers = generate_and_shuffle(10, 300)
shuffled_numbers_2 = generate_and_shuffle(10, 300)

def sort(list_original:list):
    sort_list = []

    while len(list_original) != 0:
        min_value = min(list_original)
        max_value = max(list_original)

        middle = abs(max_value - min_value) / 2

        print(list_original)

        for id, value in enumerate(list_original):
            if abs(value - min_value) <= 0:
                sort_list.append(value)
                list_original.pop(id)
                break

    return sort_list

timer = Timer('sort')
timer_2 = Timer('sort_2')

timer.start()
sort_list = sort(shuffled_numbers)
timer.elapsed_time(print_log=True)

timer_2.start()
sort_list_2 = shuffled_numbers_2.sort()
timer_2.elapsed_time(print_log=True)

#print(sort_list)