
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QComboBox, 
                            QPushButton, QLabel, QFrame, QLineEdit)
from PyQt5.QtGui import QFont

class LeftPanelView(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # Label с количеством выбранных элементов
        self.select_label = self._create_label("Выбрано элементов: 0")
        select_layout = self._create_label_layout(self.select_label)
        layout.addLayout(select_layout)
        layout.addSpacing(20)

        # ComboBox с папками
        self.folder_combo = QComboBox()
        self.folder_combo.setMinimumSize(120, 50)
        layout.addWidget(self.folder_combo)
        layout.addSpacing(20)

        # Label с информацией о страницах
        self.page_label = self._create_label("0/0")
        page_layout = self._create_label_layout(self.page_label)
        layout.addLayout(page_layout)
        layout.addSpacing(20)

        # Кнопка очистки
        self.clear_btn = QPushButton("Очистить папку")
        self.clear_btn.setMinimumSize(100, 50)
        layout.addWidget(self.clear_btn)

        # Поля ввода и кнопка добавления
        self.input_field_category = QLineEdit()
        self.input_field_folder = QLineEdit()
        self.add_btn = QPushButton("Добавить")
        
        layout.addWidget(self.input_field_category)
        layout.addWidget(self.input_field_folder)
        layout.addWidget(self.add_btn)

        layout.addStretch()
        self.setLayout(layout)

    def _create_label(self, text):
        label = QLabel(text)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        label.setFont(font)
        return label

    def _create_label_layout(self, label):
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        return layout

    def update_available_folders(self, items):
        self.folder_combo.blockSignals(True)
        self.folder_combo.clear()
        self.folder_combo.addItems(items)
        if items:
            self.folder_combo.setCurrentIndex(0)
        self.folder_combo.blockSignals(False)

    def update_select_label(self, count):
        self.select_label.setText(f"Выбрано элементов: {count}")

    def update_page_label(self, current, total):
        self.page_label.setText(f"{current}/{total}")