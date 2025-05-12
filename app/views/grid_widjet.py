from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal

from app.widgets.image_widget import ImageItemWidget


class ImageGridWidget(QWidget):
    page_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.items_per_page = 12
        self.current_page = 1
        self.current_page_max = 1
        self.image_paths = []

        self.grid = QGridLayout()
        self.grid.setSpacing(15)
        self.setLayout(self.grid)


    def update_grid(self, image_list, category_config, current_category, name_all_folders):
        self.clear_grid()

        for i, image_list in enumerate(image_list):
            image_path = image_list['image_path']
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


    def set_all_checkboxes(self, checked=True):
        for i in range(self.grid.count()):
            widget = self.grid.itemAt(i).widget()
            if isinstance(widget, ImageItemWidget):
                widget.checkbox.setChecked(checked)
    