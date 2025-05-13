from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout
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

        # Создаем вертикальный макет
        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0, 0, 0, 0)

        # Создаем горизонтальный макет для добавления гибкого пространства слева и справа
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)

        self.grid = QGridLayout()
        self.grid.setSpacing(15)

        # Добавляем QGridLayout в горизонтальный макет
        horizontal_layout.addLayout(self.grid)

        # Добавляем гибкое пространство справа
        horizontal_layout.addStretch()

        # Добавляем горизонтальный макет в вертикальный макет
        vertical_layout.addLayout(horizontal_layout)

        # Добавляем гибкое пространство снизу
        vertical_layout.addStretch()

        # Устанавливаем вертикальный макет в окно
        self.setLayout(vertical_layout)



    def update_grid(self, image_list, category_config, name_all_folders):
        self.clear_grid()

        for i,  image_properties in enumerate(image_list):
            row = i // 4
            col = i % 4

            item = ImageItemWidget(image_properties, category_config, name_all_folders)
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
    