from PyQt5.QtWidgets import (QFrame, QProgressBar, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import pyqtSignal

class ProgressBarWidget(QFrame):
    progress_completed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.default_style = """
            QProgressBar {
                border: 2px solid #808080;
                border-radius: 5px;
                text-align: center;
                background: #FFFFFF;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                width: 20px;
            }
        """
        self.complete_style = """
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(self.default_style)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def set_minimum(self, value):
        self.progress_bar.setMinimum(value)

    def set_maximum(self, value):
        self.progress_bar.setMaximum(value)

    def add_progress(self, value):
        new_value = self.progress_bar.value() + value
        max_value = self.progress_bar.maximum()
        
        if new_value >= max_value:
            self.progress_bar.setValue(max_value)
            self.progress_bar.setStyleSheet(self.default_style + self.complete_style)
            self.progress_completed.emit()
        else:
            self.progress_bar.setValue(new_value)

    def reset(self):
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(self.default_style)

        