import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from app.models.image_model import SortingModel
from app.views.main_view import MainView
from app.controllers.main_controller import SortingController


class ImageSortingWidget(QWidget):
    def __init__(self, window_manager=None, base_path=None, parent=None):
        super().__init__(parent)

        self.window_manager = window_manager

        if not window_manager is None:
            self.queue_manager = self.window_manager.queue_manager
            self.fullscreen = self.window_manager.fullscreen
        
        # Конфигурируем базовый путь
        self.base_path = base_path or os.path.normpath("Data_image")
        
        # Инициализация компонентов MVC
        self.model = SortingModel(self.base_path)
        self.view = MainView()
        self.controller = SortingController(self.model, self.view)
        
        # Настройка интерфейса
        self.init_ui()
        

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.view)
        self.setLayout(main_layout)
        

    def set_base_path(self, new_path):
        """Метод для динамического изменения базового пути"""
        self.model.update_base_path(new_path)
        
        
    def get_current_images(self):
        return self.model.get_image_paths()
    

    def connect_close_event(self, handler):
        self.view.closed.connect(handler)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    import qdarkstyle

    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()

    app = QApplication(sys.argv)
    app.setStyleSheet(dark_stylesheet)
    widget = ImageSortingWidget()
    widget.setWindowTitle("Image Sorter")
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec_())
