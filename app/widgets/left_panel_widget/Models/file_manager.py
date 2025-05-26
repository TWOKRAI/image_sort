import os
from PyQt5.QtCore import QObject, pyqtSignal, QDir


class FileManager(QObject):
    """
    Класс для работы с файловой системой
    """
    folder_scan_started = pyqtSignal()
    folder_scan_finished = pyqtSignal(list)
    folder_creation_success = pyqtSignal(str)
    folder_creation_error = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._base_scan_path = ""

    @property
    def base_scan_path(self):
        """Базовый путь для сканирования (только для чтения)"""
        return self._base_scan_path

    def set_base_scan_path(self, path):
        """
        Установка нового пути для сканирования
        :param path: Путь к директории
        """
        if os.path.isdir(path):
            self._base_scan_path = path
            self.scan_folders()
        else:
            self.folder_creation_error.emit(f"Недопустимый путь: {path}")

    def scan_folders(self):
        """Сканирование директории и обновление списка папок"""
        self.folder_scan_started.emit()
        
        try:
            folders = []
            if os.path.exists(self._base_scan_path):
                dirs = QDir(self._base_scan_path).entryList(
                    QDir.Dirs | QDir.NoDotAndDotDot | QDir.Readable
                )
                folders = list(dirs)
            
            self.folder_scan_finished.emit(folders)
            
        except Exception as e:
            self.folder_creation_error.emit(f"Ошибка сканирования: {str(e)}")

    def create_folder(self, folder_name):
        """
        Создание новой папки
        :param folder_name: Имя новой папки
        :return: True если создание успешно, False в случае ошибки
        """
        if not folder_name:
            self.folder_creation_error.emit("Имя папки не может быть пустым")
            return False
            
        target_path = os.path.join(self._base_scan_path, folder_name)
        
        if os.path.exists(target_path):
            self.folder_creation_error.emit(f"Папка '{folder_name}' уже существует")
            return False
            
        try:
            os.makedirs(target_path, exist_ok=False)
            self.folder_creation_success.emit(folder_name)
            self.scan_folders()  # Обновляем список после создания
            return True
        except OSError as e:
            self.folder_creation_error.emit(f"Ошибка создания: {e.strerror}")
            return False
        except Exception as e:
            self.folder_creation_error.emit(f"Неизвестная ошибка: {str(e)}")
            return False