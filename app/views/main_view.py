from PyQt5.QtWidgets import QWidget, QHBoxLayout

from app.views.lefr_panel import LeftPanel
from app.views.grid_widjet import ImageGridWidget
from app.views.right_panel import RightPanel


class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.left_panel = LeftPanel()
        self.right_panel = RightPanel()
        self.grid_widget = ImageGridWidget()
        
        self.init_ui()
        self.setup_connections()


    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_panel)
        main_layout.addWidget(self.grid_widget, 1)
        main_layout.addWidget(self.right_panel)
        self.setLayout(main_layout)


    def setup_connections(self):
        # self.right_panel.prev_btn.clicked.connect(
        #     lambda: self.grid_widget.page_changed.emit(-1))
        # self.right_panel.next_btn.clicked.connect(
        #     lambda: self.grid_widget.page_changed.emit(1))
        pass