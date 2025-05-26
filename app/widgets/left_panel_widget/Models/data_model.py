import os
from PyQt5.QtCore import QObject, pyqtSignal, QDir

class DataModel(QObject):
    """
    Модель для левой панели управления, реализующая логику данных по паттерну MVC.
    Отвечает за хранение состояния и уведомление об изменениях через сигналы.
    """
    
    # Сигналы для взаимодействия с другими компонентами системы
    selected_folder_changed = pyqtSignal(str)      # Изменилась выбранная папка
    selected_count_changed = pyqtSignal(int)       # Изменилось количество выбранных элементов
    page_info_changed = pyqtSignal(int, int)       # Обновилась информация о страницах (текущая/всего)
    available_folders_changed = pyqtSignal(list)  # Обновился список доступных папок
    clear_requested = pyqtSignal()                # Запрошена очистка данных

    def __init__(self):
        super().__init__()
        # Инициализация внутреннего состояния
        self._available_folders = []  # Список доступных папок
        self._selected_folder = ""    # Текущая выбранная папка
        self._selected_count = 0      # Количество выбранных элементов
        self._current_page = 0        # Текущая страница
        self._total_pages = 0         # Всего страниц

    @property
    def available_folders(self):
        """Список доступных для выбора папок (только для чтения)"""
        return self._available_folders

    @available_folders.setter
    def available_folders(self, value):
        """
        Установка нового списка папок.
        При изменении списка генерирует сигнал available_folders_changed.
        """
        
        if self._available_folders != value:
            self._available_folders = value

            self.available_folders_changed.emit(value)

    @property
    def selected_folder(self):
        """Текущая выбранная папка (только для чтения)"""
        return self._selected_folder

    @selected_folder.setter
    def selected_folder(self, value):
        """
        Установка новой выбранной папки.
        При изменении значения генерирует сигнал selected_folder_changed.
        """
        if self._selected_folder != value:
            self._selected_folder = value
            self.selected_folder_changed.emit(value)

    @property
    def selected_count(self):
        """Количество выбранных элементов (только для чтения)"""
        return self._selected_count

    @selected_count.setter
    def selected_count(self, value):
        """
        Установка нового количества выбранных элементов.
        При изменении значения генерирует сигнал selected_count_changed.
        """
        if self._selected_count != value:
            self._selected_count = value
            self.selected_count_changed.emit(value)

    @property
    def current_page(self):
        """Текущая страница (только для чтения)"""
        return self._current_page

    @current_page.setter
    def current_page(self, value):
        """
        Установка новой текущей страницы.
        При изменении генерирует сигнал page_info_changed с обновленными данными.
        """
        if self._current_page != value:
            self._current_page = value
            self.page_info_changed.emit(value, self._total_pages)

    @property
    def total_pages(self):
        """Общее количество страниц (только для чтения)"""
        return self._total_pages

    @total_pages.setter
    def total_pages(self, value):
        """
        Установка общего количества страниц.
        При изменении генерирует сигнал page_info_changed с обновленными данными.
        """
        if self._total_pages != value:
            self._total_pages = value
            self.page_info_changed.emit(self._current_page, value)

    def clear(self):
        """
        Инициирует процесс очистки данных.
        Генерирует сигнал clear_requested для уведомления подписчиков.
        """
        self.clear_requested.emit()