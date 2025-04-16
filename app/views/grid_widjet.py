from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal

from app.widgets.image_widget import ImageItemWidget


class ImageGridWidget(QWidget):
    page_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.items_per_page = 12
        self.current_page = 0
        self.image_paths = []

        self.grid = QGridLayout()
        self.grid.setSpacing(15)
        self.setLayout(self.grid)


    def update_grid(self, image_paths, category_config, current_category, name_all_folders):
        self.clear_grid()
        
        start = self.current_page * self.items_per_page
        current_images = image_paths[start:start+self.items_per_page]

        for i, image_path in enumerate(current_images):
            row = i // 4
            col = i % 4
            item = ImageItemWidget(image_path, category_config, current_category, name_all_folders)
            self.grid.addWidget(item, row, col, Qt.AlignCenter)


    def clear_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()