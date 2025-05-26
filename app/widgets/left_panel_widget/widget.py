from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSignal

from .view import LeftPanelView
from .controller import LeftPanelController
from .Models.data_model import DataModel
from .Models.file_manager import FileManager


class LeftPanel(QFrame):
    folder_changed = pyqtSignal(str)
    clear_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.data_model = DataModel()
        self.file_manager = FileManager()
        self.view = LeftPanelView()
        self.controller = LeftPanelController(self.view, self.data_model, self.file_manager)

        # Настройка внешних сигналов
        self.data_model.selected_folder_changed.connect(self.folder_changed)
        self.view.clear_btn.clicked.connect(self.clear_requested)

        # Наследование layout из View
        self.setLayout(self.view.layout())