from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QFrame, QHBoxLayout
from PyQt5.QtCore import pyqtSignal


class RightPanel(QFrame):
    prev_btn_requested = pyqtSignal()
    next_btn_requested = pyqtSignal()
    apply_requested = pyqtSignal()
    delete_requested = pyqtSignal()
    select_all_requested = pyqtSignal()
    reset_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        
        self.init_ui()
        self.setup_connections()


    def init_ui(self):
        layout = QVBoxLayout()

        button_navigation_layout = self.create_navigation_panel()
        layout.addLayout(button_navigation_layout)
        layout.addSpacing(20)

        apply_btn = self.create_apply_button()
        layout.addWidget(apply_btn)
        layout.addSpacing(20)

        reset_btn = self.create_reset_button()
        layout.addWidget(reset_btn)
        layout.addSpacing(20)

        select_all_btn = self.create_select_all_button()
        layout.addWidget(select_all_btn)
        layout.addSpacing(20)

        delete_btn = self.create_delete_button()
        layout.addWidget(delete_btn)
        layout.addStretch()

        self.setLayout(layout)


    def create_navigation_panel(self):
        self.prev_btn = QPushButton("◀")
        self.prev_btn.setMinimumSize(60, 60)

        self.next_btn = QPushButton("▶")
        self.next_btn.setMinimumSize(60, 60)

        button_prev_next_layout = QHBoxLayout()
        button_prev_next_layout.addWidget(self.prev_btn)
        button_prev_next_layout.addStretch()
        button_prev_next_layout.addWidget(self.next_btn)

        return button_prev_next_layout


    def create_apply_button(self):
        self.apply_btn = QPushButton("Применить")
        self.apply_btn.setMinimumSize(100, 50)
        return self.apply_btn


    def create_reset_button(self):
        self.reset_btn = QPushButton("Сбросить")
        self.reset_btn.setMinimumSize(100, 50)
        return self.reset_btn


    def create_select_all_button(self):
        self.select_all_btn = QPushButton("Выбрать все")
        self.select_all_btn.setMinimumSize(100, 50)
        return self.select_all_btn


    def create_delete_button(self):
        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.setMinimumSize(100, 50)
        return self.delete_btn
    

    def setup_connections(self):
        self.prev_btn.clicked.connect(self.prev_btn_requested)
        self.next_btn.clicked.connect(self.next_btn_requested)
        self.apply_btn.clicked.connect(self.apply_requested)
        self.reset_btn.clicked.connect(self.reset_requested)
        self.select_all_btn.clicked.connect(self.select_all_requested)
        self.delete_btn.clicked.connect(self.delete_requested)