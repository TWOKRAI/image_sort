import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTabBar, QStackedWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from app.models.image_model import SortingModel
from app.views.main_view import MainView
from app.controllers.main_controller import SortingController


class ImageSortingWidget(QWidget):
    def __init__(self, window_manager=None, base_path=None, parent=None):
        super().__init__(parent)
        self.window_manager = window_manager

        if window_manager is not None:
            self.queue_manager = self.window_manager.queue_manager
            self.fullscreen = self.window_manager.fullscreen
        
        self.base_path = base_path or os.path.normpath("Data_image")
        
        self.model = SortingModel(self.base_path)
        self.view = MainView()
        self.controller = SortingController(self.model, self.view)
    
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.view)
        self.setLayout(main_layout)
        
    def set_base_path(self, new_path):
        self.model.update_base_path(new_path)
        
    def get_current_images(self):
        return self.model.get_image_paths()
    
    def connect_close_event(self, handler):
        self.view.closed.connect(handler)

    def get_folders(self):
        return self.model.get_names_folders()
    
    def set_folders(self, folders):
        self.model.name_all_folders = folders.copy()
        self.controller.update_combobox_category()
        self.controller.update_model()
        self.controller.update_view()


class TabManagerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(2)
        
        control_panel = QHBoxLayout()
        control_panel.setContentsMargins(0, 0, 0, 0)
        control_panel.setSpacing(4)
        
        self.btn_add = QPushButton("+")
        self.btn_add.setFixedSize(50, 70)
        self.btn_add.setStyleSheet("""
            QPushButton {
                font-size: 21px;
                font-weight: bold;
                border-radius: 4px;
            }
        """)
        
        self.btn_remove = QPushButton("-")
        self.btn_remove.setFixedSize(50, 70)
        self.btn_remove.setStyleSheet("""
            QPushButton {
                font-size: 33px;
                border-radius: 4px;
            }
        """)
        
        self.tab_bar = QTabBar()
        self.tab_bar.setExpanding(False)
        self.tab_bar.setStyleSheet("""
            QTabBar {
                background: transparent;
                border: none;
            }
            QTabBar::tab {
                min-width: 120px;
                max-width: 200px;
                height: 28px;
                padding: 4px 8px;
                background: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #ffffff;
                border-color: #aaa;
            }
        """)
        
        control_panel.addWidget(self.btn_add, alignment=Qt.AlignLeft)
        control_panel.addWidget(self.tab_bar, stretch=1)
        control_panel.addWidget(self.btn_remove, alignment=Qt.AlignRight)
        
        self.stack = QStackedWidget()
        
        self.layout().addLayout(control_panel)
        self.layout().addWidget(self.stack, stretch=1)
        
        self.btn_add.clicked.connect(self.add_tab)
        self.btn_remove.clicked.connect(self.remove_tab)
        self.tab_bar.currentChanged.connect(self.change_tab)

        self.add_tab()

    def add_tab(self):
        # Получаем текущую активную вкладку
        current_idx = self.tab_bar.currentIndex()
        current_widget = None
        if current_idx != -1:
            current_widget = self.stack.widget(current_idx)
        
        # Создаем новый виджет
        new_sorting_widget = ImageSortingWidget()
        
        # Копируем папки из текущей вкладки, если она существует
        if current_widget and isinstance(current_widget, ImageSortingWidget):
            folders = current_widget.get_folders()
            new_sorting_widget.set_folders(folders)

        
        # Добавляем новую вкладку
        tab_index = self.tab_bar.addTab("Новая вкладка")
        self.stack.addWidget(new_sorting_widget)
        self.update_tab_names()
        self.tab_bar.setCurrentIndex(tab_index)

    def remove_tab(self):
        current_idx = self.tab_bar.currentIndex()
        if current_idx == -1:
            return
            
        self.tab_bar.removeTab(current_idx)
        widget = self.stack.widget(current_idx)
        self.stack.removeWidget(widget)
        widget.deleteLater()
        self.update_tab_names()

    def change_tab(self, index):
        if index != -1:
            self.stack.setCurrentIndex(index)

    def update_tab_names(self):
        for index in range(self.tab_bar.count()):
            self.tab_bar.setTabText(index, f"Вкладка {index + 1}")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = TabManagerWidget()
    window.setWindowTitle("Multi Workspace Image Sorter")
    window.resize(1024, 768)
    window.show()
    sys.exit(app.exec_())