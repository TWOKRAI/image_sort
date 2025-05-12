# import os
# import shutil
# import numpy as np
# import matplotlib.pyplot as plt
# from PIL import Image
# from tqdm import tqdm
# import random
# import tensorflow as tf

# import time


# class Timer:
#     def __init__(self, name):
#         self.name = name
#         self.start_time = None


#     def start(self):
#         """Начинает отсчет времени и сохраняет текущее время в атрибут start_time."""
#         self.start_time = time.time()
#         #print(f"Таймер {self.name} запущен")


#     def elapsed_time(self, print_log=False):
#         """Возвращает количество секунд, прошедших с момента запуска таймера."""
#         if self.start_time is None:
#             #print(f"Таймер {self.name} не был запущен.")
#             return 0
        
#         elapsed = time.time() - self.start_time

#         if print_log:
#             print(f"Таймер {self.name} {elapsed * 1000} мс")
        
#         return elapsed

# timer = Timer('time_neuroun')

# # Задаем классы вручную
# CLASS_NAMES = ['Bad', 'Good', 'Neutral']  # Ваши 3 класса
# COLORS = {'Bad': 'red', 'Good': 'green', 'Neutral': 'yellow'}  # Цвета для каждого класса

# def collect_image_paths(source_dir):
#     """
#     Собирает все изображения из source_dir и всех вложенных подпапок
    
#     Args:
#         source_dir (str): Путь к корневой директории с изображениями
        
#     Returns:
#         list: Список словарей с информацией о каждом изображении:
#               - 'path': полный путь к файлу
#               - 'filename': имя файла (без пути)
#               - 'subdir': относительный путь подпапки (относительно source_dir)
#     """
#     image_paths = []
    
#     # Рекурсивно обходим все поддиректории
#     for root, dirs, files in os.walk(source_dir):
#         for file in files:
#             if file.lower().endswith(('.png', '.jpg', '.jpeg')):
#                 # Получаем относительный путь подпапки
#                 rel_path = os.path.relpath(root, source_dir)
                
#                 image_paths.append({
#                     'path': os.path.join(root, file),  # Полный путь к файлу
#                     'filename': file,                  # Имя файла
#                     'subdir': rel_path                # Относительный путь подпапки
#                 })
    
#     print('Количество изображений:', len(image_paths))
#     return image_paths

# def setup_directories(output_dir):
#     """Создает структуру папок для классов и графиков"""
#     for true_class in CLASS_NAMES:
#         os.makedirs(os.path.join(output_dir, true_class), exist_ok=True)
#         # Папки для классификации
#         # for pred_class in CLASS_NAMES:
#         #     os.makedirs(os.path.join(output_dir, true_class, pred_class), exist_ok=True)
#         # Папки для графиков
#         os.makedirs(os.path.join(output_dir, f'graf_{true_class}'), exist_ok=True)

# def load_and_preprocess(image_path, target_size=(72, 72)):
#     """Загрузка и предобработка изображения"""
#     img = Image.open(image_path)
#     img = img.resize(target_size)
#     img_array = np.array(img) / 255.0
#     return img_array

# def create_mini_plot(predictions, filename):
#     """Создает мини-график с предсказаниями"""
#     plt.figure(figsize=(1, 0.7), dpi=300, facecolor='black')
#     ax = plt.gca()
#     ax.set_facecolor('black')
    
#     # Настройки стиля
#     plt.rcParams.update({
#         'text.color': 'white',
#         'axes.labelcolor': 'white',
#         'xtick.color': 'white',
#         'ytick.color': 'white',
#         'font.size': 4
#     })
    
#     # Проверяем соответствие размерностей
#     if len(predictions) != len(CLASS_NAMES):
#         predictions = np.resize(predictions, len(CLASS_NAMES))
    
#     # Создаем график
#     colors = [COLORS[cls] for cls in CLASS_NAMES]
#     bars = plt.bar(CLASS_NAMES, predictions, color=colors)
    
#     plt.ylim(0, 1)
#     plt.xticks(rotation=45, fontsize=4)
#     plt.yticks([0, 0.5, 1], fontsize=4)
#     plt.tight_layout(pad=0.1)
    
#     return plt

# def process_images(model, source_dir, output_dir):
#     """Основная функция обработки изображений"""
#     image_data = collect_image_paths(source_dir)
#     #print(image_data)
#     input('продолжить?')
#     #random.shuffle(image_data)
#     setup_directories(output_dir)
#     input('продолжить?')
    
#     total = len(image_data)
#     pbar = tqdm(total=total)
    
#     while image_data:
#         batch_size = random.randint(1, min(10, len(image_data)))
#         batch = image_data[:batch_size]
#         del image_data[:batch_size]
        
#         # Загрузка изображений
#         images = [load_and_preprocess(item['path']) for item in batch]
#         images = np.array(images)
        
#         timer.start()
#         # Предсказание модели
#         predictions = model.predict(images, verbose=0)

#         timer.elapsed_time(print_log=True)
        
#         for idx, item in enumerate(batch):
#             pred_class_idx = np.argmax(predictions[idx])
#             pred_class = CLASS_NAMES[pred_class_idx]
#             confidence = np.max(predictions[idx])
            
#             # Для теста - считаем что истинный класс = предсказанному
#             # В реальном коде нужно получать true_class из ваших данных
#             true_class = pred_class  # Замените на реальный true_class если есть
            
#             # Сохраняем изображение
#             dest_path = os.path.join(output_dir, true_class, item['filename'])
#             shutil.copy(item['path'], dest_path)
            
#             # Сохраняем график
#             plt = create_mini_plot(predictions[idx], item['filename'])
#             graf_path = os.path.join(output_dir, f'graf_{true_class}', f'graf_{item["filename"]}')
#             plt.savefig(graf_path, bbox_inches='tight', pad_inches=0.05)
#             plt.close()
            
#             pbar.update(1)

#             break
    
#     pbar.close()

# # Пример использования:

# model_path = 'waffle_classifier_v1002.keras'
# #model_path = 'waffle_classifier_v1014_big.keras'
# image_path = r'C:\Users\INNOTECH\Documents\Sort_image_Part_2\Sort_image_Part_2\Sorting3\Good'
# image_path_out = r'C:\Users\INNOTECH\Documents\Sort_image_Part_2\Sort_image_Part_2\Sorting3\Good_neuroun'

# model = tf.keras.models.load_model(
#                 model_path,
#                 custom_objects={
#                     'prec': tf.keras.metrics.Precision(name='prec'),
#                     'rec': tf.keras.metrics.Recall(name='rec')
#                 }
#             )

# process_images(model, image_path, image_path_out)


import shutil
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tqdm import tqdm
import random

import time

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1'

import tensorflow as tf
tf.config.threading.set_inter_op_parallelism_threads(4)  # Оптимизация потоков
print(tf.__version__)
print("oneDNN включен:", tf.config.list_physical_devices('CPU')[0].device_type == 'CPU')





class Timer:
    def __init__(self, name):
        self.name = name
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def elapsed_time(self, print_log=False):
        if self.start_time is None:
            return 0
        elapsed = time.time() - self.start_time
        if print_log:
            print(f"Таймер {self.name} {elapsed * 1000} мс")
        return elapsed

timer = Timer('time_neuroun')

CLASS_NAMES = ['Bad', 'Good', 'Neutral']
COLORS = {'Bad': 'red', 'Good': 'green', 'Neutral': 'yellow'}

def collect_image_paths(source_dir):
    image_paths = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                rel_path = os.path.relpath(root, source_dir)
                image_paths.append({
                    'path': os.path.join(root, file),
                    'filename': file,
                    'subdir': rel_path
                })
    print('Количество изображений:', len(image_paths))
    return image_paths

def setup_directories(output_dir):
    for true_class in CLASS_NAMES:
        os.makedirs(os.path.join(output_dir, true_class), exist_ok=True)

def load_and_preprocess(image_path, target_size=(72, 72)):
    img = Image.open(image_path)
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0
    return img_array

def create_mini_plot(predictions, filename):
    plt.figure(figsize=(1, 0.7), dpi=300, facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    plt.rcParams.update({
        'text.color': 'white',
        'axes.labelcolor': 'white',
        'xtick.color': 'white',
        'ytick.color': 'white',
        'font.size': 4
    })
    
    if len(predictions) != len(CLASS_NAMES):
        predictions = np.resize(predictions, len(CLASS_NAMES))
    
    colors = [COLORS[cls] for cls in CLASS_NAMES]
    bars = plt.bar(CLASS_NAMES, predictions, color=colors)
    
    plt.ylim(0, 1)
    plt.xticks(rotation=45, fontsize=4)
    plt.yticks([0, 0.5, 1], fontsize=4)
    plt.tight_layout(pad=0.1)
    return plt

def process_images(model, source_dir, output_dir, batch_size = None):
    image_data = collect_image_paths(source_dir)
    setup_directories(output_dir)
    
    total = len(image_data)
    pbar = tqdm(total=total)
    
    while image_data:
        if batch_size is None:
            batch_size = random.randint(1, min(10, len(image_data)))

        batch = image_data[:batch_size]
        del image_data[:batch_size]
        
        images = [load_and_preprocess(item['path']) for item in batch]
        images = np.array(images)
        
        timer.start()
        predictions = model.predict(images, verbose=0)
        timer.elapsed_time(print_log=True)
        
        for idx, item in enumerate(batch):
            pred_class_idx = np.argmax(predictions[idx])
            pred_class = CLASS_NAMES[pred_class_idx]
            confidence = np.max(predictions[idx])
            
            true_class = pred_class  # Замените на реальный true_class
            
            dest_path = os.path.join(output_dir, true_class, item['filename'])
            shutil.copy(item['path'], dest_path)
            
            base, ext = os.path.splitext(item['filename'])
            graf_filename = f"{base}_graf.png"
            graf_path = os.path.join(output_dir, true_class, graf_filename)
            
            plt = create_mini_plot(predictions[idx], item['filename'])
            plt.savefig(graf_path, bbox_inches='tight', pad_inches=0.05)
            plt.close()
            
            pbar.update(1)
    
    pbar.close()


#model_path = 'waffle_classifier_v1002.keras'
model_path = 'waffle_classifier_v1014_big.keras'
image_path = r'C:\Users\INNOTECH\Downloads\Save_brak2_1704\Save_brak2'
image_path_out = r'C:\Users\INNOTECH\Downloads\Save_brak2_1704\Save_brak2_neuroun'


model = tf.keras.models.load_model(
    model_path,
    custom_objects={
        'prec': tf.keras.metrics.Precision(name='prec'),
        'rec': tf.keras.metrics.Recall(name='rec')
    }
)

process_images(model, image_path, image_path_out, 32)