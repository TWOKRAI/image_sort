import os
from PIL import Image

class ImageFlipper:
    def __init__(self, source_dir, direction):
        if not os.path.isdir(source_dir):
            raise ValueError(f"Директория {source_dir} не существует")
        
        self.source_dir = os.path.abspath(source_dir)  # Полный путь к исходной папке
        self.source_parent = os.path.dirname(self.source_dir)  # Родительская директория
        self.source_folder_name = os.path.basename(self.source_dir)  # Имя исходной папки
        
        direction = direction.upper()
        if direction not in ('H', 'V'):
            raise ValueError("Направление должно быть 'H' (горизонтально) или 'V' (вертикально)")
        self.direction = direction
        
        self.allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    def process(self):
        base_folder_name = f"{self.source_folder_name}_turn{self.direction}"
        output_dir = os.path.join(self.source_parent, base_folder_name)
        
        # Создание папки (если существует - перезаписываем)
        os.makedirs(output_dir, exist_ok=True)
        print(f"Создана папка: {output_dir}")
        
        # Обработка изображений
        for filename in os.listdir(self.source_dir):
            # Проверка расширения файла
            ext = os.path.splitext(filename)[1].lower()
            if ext not in self.allowed_extensions:
                continue
                
            file_path = os.path.join(self.source_dir, filename)
            
            try:
                # Открытие изображения
                with Image.open(file_path) as img:
                    # Переворот изображения
                    if self.direction == 'H':
                        flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    else:
                        flipped_img = img.transpose(Image.FLIP_TOP_BOTTOM)
                    
                    # Формирование нового имени
                    name_part = os.path.splitext(filename)[0]
                    new_filename = f"{name_part}_turn{self.direction}{ext}"
                    save_path = os.path.join(output_dir, new_filename)
                    
                    # Сохранение
                    flipped_img.save(save_path)
                    print(f"Сохранено: {os.path.relpath(save_path)}")
                    
            except Exception as e:
                print(f"Ошибка при обработке {filename}: {str(e)}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Переворачивает изображения в папке горизонтально или вертикально")
    parser.add_argument("source_dir", help="Путь к папке с исходными изображениями")
    parser.add_argument("direction", help="Направление переворота: H или V", choices=['H', 'h', 'V', 'v'])
    
    args = parser.parse_args()
    
    try:
        flipper = ImageFlipper(args.source_dir, args.direction)
        flipper.process()
    except Exception as e:
        print(f"Ошибка: {str(e)}")