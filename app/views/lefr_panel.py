from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, 
            QComboBox, QPushButton, QLabel, QFrame, QLineEdit)
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont


class LeftPanel(QFrame):
    folder_changed = pyqtSignal(str)
    clear_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        
        self.init_ui()
        self.setup_connections()


    # def init_ui(self):
    #     layout = QVBoxLayout()

    #     self.folder_combo = self.create_folder_combo()
    #     layout.addWidget(self.folder_combo, 1)
    #     layout.addSpacing(20)

    #     self.page_label = self.create_page_label()
    #     layout.addWidget(self.page_label)
    #     layout.addSpacing(20)

    #     self.clear_btn = self.create_clear_button()
    #     layout.addWidget(self.clear_btn)

    #     layout.addStretch()

    #     self.setLayout(layout)

    def init_ui(self):
        layout = QVBoxLayout()

        self.folder_combo = self.create_folder_combo()
        layout.addWidget(self.folder_combo, 1)
        layout.addSpacing(20)

        # Создаем горизонтальный макет для self.page_label
        page_label_layout = QHBoxLayout()
        page_label_layout.addStretch()  # Гибкое пространство слева
        self.page_label = self.create_page_label()
        page_label_layout.addWidget(self.page_label)
        page_label_layout.addStretch()  # Гибкое пространство справа

        # Добавляем горизонтальный макет в вертикальный макет
        layout.addLayout(page_label_layout)
        layout.addSpacing(20)

        self.clear_btn = self.create_clear_button()
        layout.addWidget(self.clear_btn)

        # Добавляем окно ввода и кнопку "Добавить"
        self.input_field_category = QLineEdit()
        layout.addWidget(self.input_field_category)

        self.input_field_folder = QLineEdit()
        layout.addWidget(self.input_field_folder)

        self.add_btn = QPushButton("Добавить")
        layout.addWidget(self.add_btn)

        layout.addStretch()

        self.setLayout(layout)

    def create_folder_combo(self):
        folder_combo = QComboBox()
        folder_combo.setMinimumSize(120, 50)
        return folder_combo
    

    def load_available_items(self, items):
        self.folder_combo.blockSignals(True)

        self.folder_combo.clear()
        self.folder_combo.addItems(items)
        self.folder_combo.setCurrentIndex(0)
        
        self.folder_combo.blockSignals(False)


    def create_page_label(self):
        page_label = QLabel("0/0")

        font = QFont()
        font.setFamily("Arial") 
        font.setPointSize(12)    
        page_label.setFont(font)

        return page_label
    
    
    def update_page_label(self, current_page, total_pages):
        self.page_label.setText(f"{current_page}/{total_pages}")


    def create_clear_button(self):
        clear_btn = QPushButton("Очистить папку")
        clear_btn.setMinimumSize(100, 50)
        return clear_btn


    def setup_connections(self):
        self.folder_combo.currentTextChanged.connect(self.folder_changed)
        self.clear_btn.clicked.connect(self.clear_requested)
