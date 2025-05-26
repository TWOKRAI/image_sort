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


    def init_ui(self):
        layout = QVBoxLayout()   

        select_label_layout, self.select_label = self.create_label_panel(f'Выбрано элементов: 0')     
        layout.addLayout(select_label_layout)
        layout.addSpacing(20)


        self.folder_combo = self.create_folder_combo()
        layout.addWidget(self.folder_combo, 1)
        layout.addSpacing(20)

        # # Создаем горизонтальный макет для self.page_label
        # page_label_layout = QHBoxLayout()
        # page_label_layout.addStretch()  # Гибкое пространство слева
        # self.page_label = self.create_page_label("0/0")
        # page_label_layout.addWidget(self.page_label)
        # page_label_layout.addStretch()  # Гибкое пространство справа

        page_label_layout, self.page_label = self.create_label_panel("0/0")

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


    def create_label(self, text):
        page_label = QLabel(text)

        font = QFont()
        font.setFamily("Arial") 
        font.setPointSize(12)    
        page_label.setFont(font)

        return page_label
    

    def create_label_panel(self, text):
        label_layout = QHBoxLayout()
        label_layout.addStretch()
        label = self.create_label(text)
        label_layout.addWidget(label)
        label_layout.addStretch()

        return label_layout, label
    
    
    def update_page_label(self, current_page, total_pages):
        self.page_label.setText(f"{current_page}/{total_pages}")

    def update_select_label(self, select_count):
        self.select_label.setText(f"Выбрано элементов: {select_count}")

    def create_clear_button(self):
        clear_btn = QPushButton("Очистить папку")
        clear_btn.setMinimumSize(100, 50)
        return clear_btn


    def setup_connections(self):
        self.folder_combo.currentTextChanged.connect(self.folder_changed)
        self.clear_btn.clicked.connect(self.clear_requested)
