import os
import shutil
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QColor


class SortingModel(QObject):
    data_changed = pyqtSignal()
    error_occurred = pyqtSignal(str, str)

    def __init__(self, base_path, default_category='neutral'):
        super().__init__()
        self.base_path = os.path.normpath(base_path)
        self.current_folder = ""
        self.current_category = default_category
        
        self.list_model = []
        self.image_paths = []
        self.name_all_folders = []

        self.category_config = {
            'good': {'category': 'good',
                    'folder': 'Data_good', 
                     'counter': 0, 
                     'color': QColor('#67e967')
                     },

            'neutral': {'category': 'neutral',
                        'folder': 'Data_neutral', 
                        'counter': 0, 
                        'color': QColor('#fff385')
                        },

            'bad': {'category': 'bad',
                    'folder': 'Data_bad', 
                    'counter': 0, 
                    'color': QColor('#ff5770')
                    }
        }

        self.select_category = {}

        #self.all_rename()
        self.init_folders()
        self.init_sequence_counters()
        self.get_names_folders()

        #print(self.category_config)


    def init_folders(self):
        """
        Инициализирует папки для каждой категории, указанной в конфигурации.
        Для каждой категории создается папка в базовом пути, если она еще не существует.
        """
        for category in self.category_config.values():
            path = os.path.join(self.base_path, category['folder'])
            os.makedirs(path, exist_ok=True)


    def init_sequence_counters(self):
        """
        Инициализирует счетчики последовательностей для каждой категории.

        Для каждой категории определяется максимальный номер последовательности
        на основе существующих файлов в соответствующей папке.
        """
        for category, config in self.category_config.items():
            config['counter'] = self.get_max_sequence_number(category)


    def get_max_sequence_number(self, category):
        """
        Возвращает максимальный номер последовательности для файлов в папке категории.
        Просматривает все файлы в папке категории, начинающиеся с "image_" и заканчивающиеся на ".jpg",
        и определяет максимальный номер последовательности.
        """
        folder = self.get_category_path(category)
        max_num = 0
        if os.path.exists(folder):
            for f in os.listdir(folder):
                if f.startswith("image_") and f.endswith(".jpg"):
                    try:
                        num = int(f[6:-4])
                        max_num = max(max_num, num)
                    except ValueError:
                        continue
        return max_num


    def get_category_path(self, category):
        """
        Возвращает полный путь к папке категории.
        Соединяет базовый путь с путем папки категории, указанным в конфигурации.
        """
        return os.path.join(self.base_path, self.category_config[category]['folder'])


    def load_folder(self, folder_name):
        """
        Загружает содерж
        имое указанной папки в модель.

        Принцип работы:
        1. Формирует полный путь к целевой папке.
        2. Собирает список всех файлов в папке.
        3. Сохраняет пути к файлам в image_paths.
        4. Уведомляет подписчиков об изменении данных.

        :param folder_name: Название папки внутри базового пути (base_path).
        """
        
        # Формирование абсолютного пути к целевой папке
        self.current_folder = os.path.join(self.base_path, folder_name)

        # Сбор всех файлов в папке (исключая подпапки)
        self.image_paths = [
            os.path.join(self.current_folder, f)
            for f in os.listdir(self.current_folder)
            if os.path.isfile(os.path.join(self.current_folder, f))
        ]

        #print('self.image_paths', self.image_paths)

        # Отправка сигнала об изменении данных
        #self.data_changed.emit()

    
    def create_list_model(self):
        for id, image_path in enumerate(self.image_paths):
            image_properties = {'id': id,
                                'image_path': image_path,
                                'category': None
                    }

            
            self.list_model.append(image_properties)

        print(self.list_model)



    def move_image(self, src_path, category):
        """
        Перемещает изображение в соответствующую категорию с уникальным именем.

        Принцип работы:
        1. Определяет целевую папку для категории.
        2. Генерирует уникальное имя файла на основе счетчика.
        3. Перемещает файл с сохранением уникального имени.
        4. Обновляет счетчик последовательности.
        5. Уведомляет об изменениях.

        :param src_path: Исходный путь к файлу.
        :param category: Категория для перемещения (good/neutral/bad).
        """
        # Получение пути целевой папки для категории
        dest_folder = self.get_category_path(category)

        # Инкремент счетчика и генерация нового имени
        self.category_config[category]['counter'] += 1
        new_name = f"image_{self.category_config[category]['counter']:05d}.jpg"

        # Формирование полного пути назначения
        dest_path = os.path.join(dest_folder, new_name)

        # Выполнение перемещения файла
        shutil.move(src_path, dest_path)

        # Уведомление подписчиков об изменении данных
        #self.data_changed.emit()


    def delete_image(self, path):
        """
        Удаляет указанный файл изображения.

        Принцип работы:
        1. Удаляет файл по указанному пути.
        2. Уведомляет об изменениях в данных.

        :param path: Полный путь к удаляемому файлу.
        """
        if os.path.exists(path):
            os.remove(path)
            self.data_changed.emit()
        else:
            self.error_occurred.emit("DELETE_ERROR", "File not found")


    def clear_current_folder(self):
        """Очистка текущей папки"""
        if self.current_folder:
            for file in os.listdir(self.current_folder):
                os.remove(os.path.join(self.current_folder, file))
            self.load_folder(os.path.basename(self.current_folder))


    def rename_files_in_directory(self, directory, start_index=1, start_file=None, end_file=None):
        """
        Переименовывает все файлы в указанной папке в формат image_i.

        :param directory: Путь к папке с файлами.
        :param start_index: Начальное значение для индекса.
        :param start_file: Начальный файл (если None, начинаем с первого файла).
        :param end_file: Конечный файл (если None, заканчиваем на последнем файле).
        """
        # Получаем список всех файлов в папке
        files = sorted(os.listdir(directory))

        # Определяем начальный и конечный индексы файлов
        start_file_index = files.index(start_file) if start_file else 0
        end_file_index = files.index(end_file) if end_file else len(files)

        current_index = start_index

        for i in range(start_file_index, end_file_index):
            file_name = files[i]
            file_extension = os.path.splitext(file_name)[1]
            new_file_name = f"image_{current_index}{file_extension}"
            new_file_path = os.path.join(directory, new_file_name)
            old_file_path = os.path.join(directory, file_name)

            os.rename(old_file_path, new_file_path)
            current_index += 1


    def all_rename(self):
        for category in self.category_config.values():
            path = os.path.join(self.base_path, category['folder'])
            self.rename_files_in_directory(path)

        
    def get_name_folder(self):
        return self.category_config[self.current_category]['folders']


    def get_names_folders(self):
        self.name_all_folders = []

        for category in self.category_config.values():
            self.name_all_folders.append(category['folder'])
        
        return self.name_all_folders
    

    def get_category(self):
        return list(self.category_config.keys())
    

    def find_key_by_folder(self, folder_name):
        for key, value in self.category_config.items():
            if value['folder'] == folder_name:
                return key
        return None 
    

    def get_category_color(self, category_folder):
        for cat in self.category_config.values():
            if cat['folder'] == category_folder:
                return cat['color']
        return QColor(Qt.transparent)
    
    
    def get_category_color(self, category_folder):
        for cat in self.category_config.values():
            if cat['folder'] == category_folder:
                return cat['color']
        return QColor(Qt.transparent)