from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

#from app.views.lefr_panel import LeftPanel
from app.widgets.left_panel_widget import LeftPanel
from app.views.grid_widjet import ImageGridWidget
from app.views.right_panel import RightPanel
from app.views.progress_bar import ProgressBarWidget

class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.left_panel = LeftPanel()
        self.right_panel = RightPanel()
        self.grid_widget = ImageGridWidget()
        self.progress_bar_widget = ProgressBarWidget()  # Новый виджет
        
        self.init_ui()


    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Верхняя часть с существующими элементами
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.left_panel)
        top_layout.addWidget(self.grid_widget, 1)
        top_layout.addWidget(self.right_panel)
        
        # Добавляем все элементы в главный макет
        main_layout.addLayout(top_layout, 90)  # 90% места
        main_layout.addWidget(self.progress_bar_widget, 10)  # 10% места
        
        self.setLayout(main_layout)


    def show_message(self, error, message):
        pass
        
