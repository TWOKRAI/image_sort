import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QMessageBox,
                             QPushButton, QVBoxLayout, QHBoxLayout, QFrame)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import os

class ImageSwitcher(QWidget):
    def __init__(self):
        super().__init__()
        self.current_index = 0
        
        # Список путей к изображениям и соответствующих подписей
        self.images = [
            r"images/image000.png",
            r"images/image0.png",
            r"images/image1.png",
            r"images/image2.png",
            r"images/image3.png",
            r"images/image4.png",
            r"images/image5.png",
            r"images/image6.png",
            r"images/image7.png",
            r"images/image8.png",
            r"images/image9.png",
            r"images/image10.png",
            r"images/image11.png",
            r"images/image12.png"
        ]
        self.captions = [
            "Включите панель",
            "Загрузка",
            " ",
            "Саня, поздравляю тебя с Днём Рождения",
            "Саня, поздравляю тебя с Днём Рождения",
            "Желаю тебе хороших командировок",
            "Желаю тебе хороших командировок",
            "Желаю тебе хороших командировок",
            "Желаю тебе хороших командировок",
            "Восьмое изображение",
            "Девятое изображение",
            "Десятое изображение",
            "Одиннадцатое изображение",
            "Двенадцатое изображение"
        ]

        # Проверка существования файлов
        self.verify_images()
        self.initUI()

    def initUI(self):
        # Настройка интерфейса
        self.setWindowTitle('Панель Siemens')
        self.setGeometry(100, 100, 1300, 1000)
        
        # Создание элементов интерфейса
        # self.caption_label = QLabel("", self)
        # self.caption_label.setAlignment(Qt.AlignCenter)
        # self.caption_label.setStyleSheet("""
        #     font-size: 24px; 
        #     font-weight: bold; 
        #     color: white;
        #     background-color: rgba(0, 0, 0, 150);
        #     padding: 10px;
        #     border-radius: 5px;
        # """)
        
        # Основной контейнер для изображения
        self.image_container = QLabel(self)
        self.image_container.setAlignment(Qt.AlignCenter)
        self.image_container.setFixedSize(1280, 900)
        self.image_container.setStyleSheet("background-color: black;")
        
        # Кнопка на изображении
        self.button = QPushButton("", self.image_container)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                min-width: 300px;
                min-height: 80px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 20);
                border: 2px solid rgba(255, 255, 255, 50);
                border-radius: 5px;
            }
        """)
        self.button.clicked.connect(self.switch_content)
        
        # Позиционирование кнопки внизу изображения
        self.button.move(
            self.image_container.width() // 2 - self.button.width() // 2 - 150,
            self.image_container.height() - self.button.height() - 20 - 50
        )
        
        # Настройка лейаута
        layout = QVBoxLayout()
        #layout.addWidget(self.caption_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.image_container, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        
        # Показать первое изображение при запуске
        self.update_content()

    def switch_content(self):
        # Переключение на следующий индекс
        self.current_index = (self.current_index + 1) % len(self.images)
        self.update_content()

    def update_content(self):
        # Обновление изображения и текста
        try:
            # Загрузка изображения
            pixmap = QPixmap(self.images[self.current_index])
            
            if not pixmap.isNull():
                # Обрезка изображения (120 пикселей сверху и снизу)
                image = pixmap.toImage()
                height = image.height()
                
                if height > 240:  # 120 сверху + 120 снизу
                    cropped_image = image.copy(0, 120, image.width(), height - 210)
                    pixmap = QPixmap.fromImage(cropped_image)
                
                # Масштабирование с сохранением пропорций
                pixmap = pixmap.scaled(
                    self.image_container.width(),
                    self.image_container.height(),
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation
                )
                
                # Установка изображения в контейнер
                self.image_container.setPixmap(pixmap)
                #self.caption_label.setText(self.captions[self.current_index])
                
                # Обновление позиции кнопки (на случай изменения размера)
                self.button.move(
                    self.image_container.width() // 2 - self.button.width() // 2 - 150,
                    self.image_container.height() - self.button.height() - 20 - 50
                )
            else:
                raise Exception("Не удалось загрузить изображение")
                
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить изображение: {e}")

    def verify_images(self):
        """Проверяет существование всех изображений в списке"""
        missing_images = []
        for img_path in self.images:
            if not os.path.exists(img_path):
                missing_images.append(img_path)
        
        if missing_images:
            msg = "Следующие изображения не найдены:\n" + "\n".join(missing_images)
            QMessageBox.critical(self, "Ошибка", msg)
            sys.exit(1)

    def resizeEvent(self, event):
        """Обработчик изменения размера окна"""
        # Обновление размеров контейнера
        new_width = min(self.width() - 20, 1280)
        new_height = min(self.height() - 100, 900)
        self.image_container.setFixedSize(new_width, new_height)
        
        # Обновление позиции кнопки
        self.button.move(
            self.image_container.width() // 2 - self.button.width() // 2,
            self.image_container.height() - self.button.height() - 20
        )
        
        # Перерисовка изображения
        self.update_content()
        super().resizeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Проверяем существование папки images
    if not os.path.exists("images"):
        os.makedirs("images")
        QMessageBox.information(
            None, 
            "Информация", 
            "Была создана папка 'images'. Пожалуйста, добавьте в неё изображения."
        )
        sys.exit(0)
    
    ex = ImageSwitcher()
    ex.show()
    sys.exit(app.exec_())