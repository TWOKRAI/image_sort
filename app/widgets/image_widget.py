
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QCheckBox,QComboBox
from PyQt5.QtGui import QPixmap, QColor, QPainter, QPen
from PyQt5.QtCore import Qt, pyqtSignal


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._border_color = Qt.transparent
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(3)

    def set_border_color(self, color):
        self._border_color = color
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(self._border_color, 6))
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))
    
    
    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


class CategoryComboBox(QComboBox):
    def __init__(self, items:list = [], parent=None):
        super().__init__(parent)
        self.addItems(items)
        self.setStyleSheet("""
            QComboBox {
                background-color: white;
                padding: 3px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)


class ImageItemWidget(QWidget):
    selection_changed = pyqtSignal(str, bool)
    category_changed = pyqtSignal(str, str)

    def __init__(self, image_path, category_config, current_category, name_all_folders, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.name_all_folders = name_all_folders
        self.category_config = category_config
        self.current_category_config = category_config[current_category]
        
        self.init_ui()
        self.setup_connections()


    def init_ui(self):
        self.setFixedSize(138, 188)
        
        self.image_label = ClickableLabel(self)
        self.image_label.setGeometry(10, 10, 128, 128)
        pixmap = QPixmap(self.image_path).scaled(
            128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)

        self.checkbox = QCheckBox(self)
        self.checkbox.setGeometry(113, 15, 20, 20)
        self.checkbox.setStyleSheet("""
                QCheckBox {
                    background-color: transparent;
                    border: none;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                    background-color: transparent;
                    border: 1px solid #666;
                }
                QCheckBox::indicator:checked {
                    background-color: #0078D7;
                }
            """)
        
        
        self.category_combo = CategoryComboBox(self.name_all_folders, self)
        self.category_combo.setGeometry(10, 148, 128, 30)
        self.category_combo.setCurrentText(self.current_category_config ['category'])
        self.image_label.set_border_color(self.current_category_config ['color'])


    def setup_connections(self):
        self.checkbox.stateChanged.connect(
            lambda: self.selection_changed.emit(
                self.image_path, 
                self.checkbox.isChecked()
            )
        )

        self.category_combo.currentTextChanged.connect(
            self.handle_category_change
        )
        
        self.image_label.clicked.connect(
            lambda: self.checkbox.setChecked(
                not self.checkbox.isChecked()
            )
        )


    def set_category_info(self, category_name, color):
        """Обновление категории и цвета"""
        self.current_category = category_name
        self.category_combo.setCurrentText(category_name)
        self.image_label.set_border_color(color)


    def get_state(self):
        """Возвращает текущее состояние для контроллера"""
        return {
            'path': self.image_path,
            'category': self.category_combo.currentText(),
            'selected': self.checkbox.isChecked()
        }


    def handle_category_change(self, selected_folder):
        """Обновляем цвет рамки при изменении категории"""
        # Ищем соответствующую категорию по имени папки
        for category in self.category_config.values():
            if category['folder'] == selected_folder:
                self.image_label.set_border_color(category['color'])
                return
        
        # Если не нашли - устанавливаем цвет по умолчанию
        self.image_label.set_border_color(Qt.transparent)