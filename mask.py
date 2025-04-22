# import os
# import cv2
# import numpy as np
# import tkinter as tk
# from tkinter import filedialog
# from PIL import Image, ImageTk

# class ColorSelectorApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Color Selector Tool")
        
#         # Переменные для изображений
#         self.image_folder = ""
#         self.image_files = []
#         self.current_image_index = 0
#         self.original_image = None
#         self.mask_image = None
#         self.display_image = None
        
#         # Переменные для HSV фильтра
#         self.hue_min = tk.IntVar(value=0)
#         self.hue_max = tk.IntVar(value=179)
#         self.sat_min = tk.IntVar(value=0)
#         self.sat_max = tk.IntVar(value=255)
#         self.val_min = tk.IntVar(value=0)
#         self.val_max = tk.IntVar(value=255)
        
#         # Создание интерфейса
#         self.create_widgets()
        
#     def create_widgets(self):
#         # Фрейм для изображений
#         self.image_frame = tk.Frame(self.root)
#         self.image_frame.pack(pady=10)
        
#         # Оригинальное изображение
#         self.original_label = tk.Label(self.image_frame)
#         self.original_label.pack(side=tk.LEFT, padx=10)
        
#         # Маска
#         self.mask_label = tk.Label(self.image_frame)
#         self.mask_label.pack(side=tk.LEFT, padx=10)
        
#         # Фрейм для управления
#         self.control_frame = tk.Frame(self.root)
#         self.control_frame.pack(pady=10)
        
#         # Кнопки навигации
#         self.prev_btn = tk.Button(self.control_frame, text="<< Previous", command=self.prev_image)
#         self.prev_btn.pack(side=tk.LEFT, padx=5)
        
#         self.next_btn = tk.Button(self.control_frame, text="Next >>", command=self.next_image)
#         self.next_btn.pack(side=tk.LEFT, padx=5)
        
#         self.load_btn = tk.Button(self.control_frame, text="Load Folder", command=self.load_folder)
#         self.load_btn.pack(side=tk.LEFT, padx=5)
        
#         # Фрейм для регуляторов HSV
#         self.hsv_frame = tk.LabelFrame(self.root, text="HSV Filter")
#         self.hsv_frame.pack(pady=10, padx=10, fill=tk.X)
        
#         # Регуляторы Hue
#         tk.Label(self.hsv_frame, text="Hue Min:").grid(row=0, column=0, padx=5, pady=2)
#         tk.Scale(self.hsv_frame, from_=0, to=179, orient=tk.HORIZONTAL, variable=self.hue_min, command=self.update_mask).grid(row=0, column=1, padx=5, pady=2)
        
#         tk.Label(self.hsv_frame, text="Hue Max:").grid(row=0, column=2, padx=5, pady=2)
#         tk.Scale(self.hsv_frame, from_=0, to=179, orient=tk.HORIZONTAL, variable=self.hue_max, command=self.update_mask).grid(row=0, column=3, padx=5, pady=2)
        
#         # Регуляторы Saturation
#         tk.Label(self.hsv_frame, text="Sat Min:").grid(row=1, column=0, padx=5, pady=2)
#         tk.Scale(self.hsv_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.sat_min, command=self.update_mask).grid(row=1, column=1, padx=5, pady=2)
        
#         tk.Label(self.hsv_frame, text="Sat Max:").grid(row=1, column=2, padx=5, pady=2)
#         tk.Scale(self.hsv_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.sat_max, command=self.update_mask).grid(row=1, column=3, padx=5, pady=2)
        
#         # Регуляторы Value
#         tk.Label(self.hsv_frame, text="Val Min:").grid(row=2, column=0, padx=5, pady=2)
#         tk.Scale(self.hsv_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.val_min, command=self.update_mask).grid(row=2, column=1, padx=5, pady=2)
        
#         tk.Label(self.hsv_frame, text="Val Max:").grid(row=2, column=2, padx=5, pady=2)
#         tk.Scale(self.hsv_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.val_max, command=self.update_mask).grid(row=2, column=3, padx=5, pady=2)
    
#     def load_folder(self):
#         self.image_folder = filedialog.askdirectory()
#         if not self.image_folder:
#             return
            
#         self.image_files = [f for f in os.listdir(self.image_folder) 
#                           if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
#         self.current_image_index = 0
        
#         if self.image_files:
#             self.load_current_image()
#         else:
#             print("No images found in the selected folder")
    
#     def load_current_image(self):
#         if not self.image_files:
#             return
            
#         image_path = os.path.join(self.image_folder, self.image_files[self.current_image_index])
#         self.original_image = cv2.imread(image_path)
#         self.update_mask()
    
#     def update_mask(self, *args):
#         if self.original_image is None:
#             return
            
#         # Конвертируем в HSV
#         hsv_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2HSV)
        
#         # Создаем маску на основе текущих значений HSV
#         lower_bound = np.array([self.hue_min.get(), self.sat_min.get(), self.val_min.get()])
#         upper_bound = np.array([self.hue_max.get(), self.sat_max.get(), self.val_max.get()])
#         mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
        
#         # Создаем белый фон
#         result = np.full(self.original_image.shape, 255, dtype=np.uint8)
        
#         # Копируем только выделенные области на белый фон
#         result[mask != 0] = self.original_image[mask != 0]
        
#         # Отображаем изображения
#         self.display_images(self.original_image, result)
    

#     def display_images(self, original, mask):
#         # Конвертируем изображения для отображения в Tkinter
#         original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
#         mask_rgb = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
        
#         # Масштабируем изображения для отображения (если нужно)
#         max_height = 500
#         scale = max_height / original.shape[0]
#         width = int(original.shape[1] * scale)
#         height = int(original.shape[0] * scale)
        
#         original_resized = cv2.resize(original_rgb, (width, height))
#         mask_resized = cv2.resize(mask_rgb, (width, height))
        
#         # Конвертируем в ImageTk
#         original_tk = ImageTk.PhotoImage(image=Image.fromarray(original_resized))
#         mask_tk = ImageTk.PhotoImage(image=Image.fromarray(mask_resized))
        
#         # Обновляем метки
#         self.original_label.config(image=original_tk)
#         self.original_label.image = original_tk
        
#         self.mask_label.config(image=mask_tk)
#         self.mask_label.image = mask_tk
    
#     def next_image(self):
#         if not self.image_files:
#             return
            
#         self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
#         self.load_current_image()
    
#     def prev_image(self):
#         if not self.image_files:
#             return
            
#         self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
#         self.load_current_image()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ColorSelectorApp(root)
#     root.mainloop()


import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ColorSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Color Selector Tool")
        
        # Переменные для изображений
        self.image_folder = ""
        self.image_files = []
        self.current_image_index = 0
        self.original_image = None
        self.mask_image = None
        self.contour_image = None
        self.display_image = None
        
        # Переменные для HSV фильтра
        self.hue_min = tk.IntVar(value=0)
        self.hue_max = tk.IntVar(value=179)
        self.sat_min = tk.IntVar(value=64)
        self.sat_max = tk.IntVar(value=255)
        self.val_min = tk.IntVar(value=0)
        self.val_max = tk.IntVar(value=64)
        
        # Переменные для контуров
        self.contour_threshold = tk.IntVar(value=100)
        self.contour_min_area = tk.IntVar(value=500)
        self.contour_color_r = tk.IntVar(value=0)
        self.contour_color_g = tk.IntVar(value=255)
        self.contour_color_b = tk.IntVar(value=0)

        # Дополнительные параметры контуров
        self.contour_thickness = tk.IntVar(value=2)
        self.line_type = tk.StringVar(value="Solid")
        self.contour_mode = tk.StringVar(value="External")
        self.approx_method = tk.StringVar(value="Simple")
        self.min_perimeter = tk.IntVar(value=0)
        
        # Переменная для процента
        self.percentage_var = tk.StringVar(value="0%")

        self.line_type_options = ["Solid", "Dashed", "Dotted"]
        self.contour_mode_options = ["External", "All"]
        self.approx_method_options = ["None", "Simple", "TC89_L1", "TC89_KCOS"]

        # Соответствия для методов аппроксимации
        self.approx_methods = {
            "None": cv2.CHAIN_APPROX_NONE,
            "Simple": cv2.CHAIN_APPROX_SIMPLE,
            "TC89_L1": cv2.CHAIN_APPROX_TC89_L1,
            "TC89_KCOS": cv2.CHAIN_APPROX_TC89_KCOS
        }

        # Соответствия для типов линий
        self.line_types = {
            "Solid": cv2.LINE_AA,
            "Dashed": cv2.LINE_4,
            "Dotted": cv2.LINE_8
        }

        # Соответствия для режимов поиска контуров
        self.contour_modes = {
            "External": cv2.RETR_EXTERNAL,
            "All": cv2.RETR_LIST
        }
                
        # Создание интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Фрейм для изображений
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(pady=10)
        
        # Оригинальное изображение
        self.original_label = tk.Label(self.image_frame)
        self.original_label.pack(side=tk.LEFT, padx=10)
        
        # Маска
        self.mask_label = tk.Label(self.image_frame)
        self.mask_label.pack(side=tk.LEFT, padx=10)
        
        # Контуры
        self.contour_label = tk.Label(self.image_frame)
        self.contour_label.pack(side=tk.LEFT, padx=10)
        
        # Фрейм для управления
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)
        
        # Кнопки навигации
        self.prev_btn = tk.Button(self.control_frame, text="<< Previous", command=self.prev_image)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = tk.Button(self.control_frame, text="Next >>", command=self.next_image)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        self.load_btn = tk.Button(self.control_frame, text="Load Folder", command=self.load_folder)
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        # Индикатор процента
        tk.Label(self.control_frame, text="Selected area:").pack(side=tk.LEFT, padx=5)
        tk.Label(self.control_frame, textvariable=self.percentage_var).pack(side=tk.LEFT, padx=5)
        
        # Фрейм для регуляторов HSV
        self.hsv_frame = tk.LabelFrame(self.root, text="HSV Filter")
        self.hsv_frame.pack(pady=10, padx=10, fill=tk.X)
        
        # Регуляторы Hue
        tk.Label(self.hsv_frame, text="Hue Min:").grid(row=0, column=0, padx=5, pady=2)
        tk.Scale(self.hsv_frame, from_=0, to=179, orient=tk.HORIZONTAL, variable=self.hue_min, command=self.update_display).grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(self.hsv_frame, text="Hue Max:").grid(row=0, column=2, padx=5, pady=2)
        tk.Scale(self.hsv_frame, from_=0, to=179, orient=tk.HORIZONTAL, variable=self.hue_max, command=self.update_display).grid(row=0, column=3, padx=5, pady=2)
        
        # Регуляторы Saturation
        tk.Label(self.hsv_frame, text="Sat Min:").grid(row=1, column=0, padx=5, pady=2)
        tk.Scale(self.hsv_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.sat_min, command=self.update_display).grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(self.hsv_frame, text="Sat Max:").grid(row=1, column=2, padx=5, pady=2)
        tk.Scale(self.hsv_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.sat_max, command=self.update_display).grid(row=1, column=3, padx=5, pady=2)
        
        # Регуляторы Value
        tk.Label(self.hsv_frame, text="Val Min:").grid(row=2, column=0, padx=5, pady=2)
        tk.Scale(self.hsv_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.val_min, command=self.update_display).grid(row=2, column=1, padx=5, pady=2)
        
        tk.Label(self.hsv_frame, text="Val Max:").grid(row=2, column=2, padx=5, pady=2)
        tk.Scale(self.hsv_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.val_max, command=self.update_display).grid(row=2, column=3, padx=5, pady=2)
        
        # Фрейм для регуляторов контуров
        self.contour_frame = tk.LabelFrame(self.root, text="Contour Settings")
        self.contour_frame.pack(pady=10, padx=10, fill=tk.X)
        
        # Регуляторы для контуров
        tk.Label(self.contour_frame, text="Threshold:").grid(row=0, column=0, padx=5, pady=2)
        tk.Scale(self.contour_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.contour_threshold, command=self.update_display).grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(self.contour_frame, text="Min Area:").grid(row=0, column=2, padx=5, pady=2)
        tk.Scale(self.contour_frame, from_=0, to=2000, orient=tk.HORIZONTAL, variable=self.contour_min_area, command=self.update_display).grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(self.contour_frame, text="Color R:").grid(row=1, column=0, padx=5, pady=2)
        tk.Scale(self.contour_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.contour_color_r, command=self.update_display).grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(self.contour_frame, text="Color G:").grid(row=1, column=2, padx=5, pady=2)
        tk.Scale(self.contour_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.contour_color_g, command=self.update_display).grid(row=1, column=3, padx=5, pady=2)
        
        tk.Label(self.contour_frame, text="Color B:").grid(row=1, column=4, padx=5, pady=2)
        tk.Scale(self.contour_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.contour_color_b, command=self.update_display).grid(row=1, column=5, padx=5, pady=2)

        # Дополнительные регуляторы для контуров
        tk.Label(self.contour_frame, text="Thickness:").grid(row=2, column=0, padx=5, pady=2)
        tk.Scale(self.contour_frame, from_=1, to=10, orient=tk.HORIZONTAL, variable=self.contour_thickness, command=self.update_display).grid(row=2, column=1, padx=5, pady=2)

        tk.Label(self.contour_frame, text="Line Type:").grid(row=2, column=2, padx=5, pady=2)
        tk.OptionMenu(self.contour_frame, self.line_type, *self.line_type_options, command=self.update_display).grid(row=2, column=3, padx=5, pady=2)

        tk.Label(self.contour_frame, text="Contour Mode:").grid(row=3, column=0, padx=5, pady=2)
        tk.OptionMenu(self.contour_frame, self.contour_mode, *self.contour_mode_options, command=self.update_display).grid(row=3, column=1, padx=5, pady=2)

        tk.Label(self.contour_frame, text="Approx Method:").grid(row=3, column=2, padx=5, pady=2)
        tk.OptionMenu(self.contour_frame, self.approx_method, *self.approx_method_options, command=self.update_display).grid(row=3, column=3, padx=5, pady=2)

        tk.Label(self.contour_frame, text="Min Perimeter:").grid(row=4, column=0, padx=5, pady=2)
        tk.Scale(self.contour_frame, from_=0, to=1000, orient=tk.HORIZONTAL, variable=self.min_perimeter, command=self.update_display).grid(row=4, column=1, padx=5, pady=2)

            
    def load_folder(self):
        self.image_folder = filedialog.askdirectory()
        if not self.image_folder:
            return
            
        self.image_files = [f for f in os.listdir(self.image_folder) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        self.current_image_index = 0
        
        if self.image_files:
            self.load_current_image()
        else:
            print("No images found in the selected folder")
    
    def load_current_image(self):
        if not self.image_files:
            return
            
        image_path = os.path.join(self.image_folder, self.image_files[self.current_image_index])
        self.original_image = cv2.imread(image_path)
        self.update_display()
    
    def update_display(self, *args):
        if self.original_image is None:
            return
            
        # Конвертируем в HSV
        hsv_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2HSV)
        
        # Создаем маску на основе текущих значений HSV
        lower_bound = np.array([self.hue_min.get(), self.sat_min.get(), self.val_min.get()])
        upper_bound = np.array([self.hue_max.get(), self.sat_max.get(), self.val_max.get()])
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
        
        # Подсчет процента найденных пикселей
        total_pixels = mask.size
        selected_pixels = cv2.countNonZero(mask)
        percentage = (selected_pixels / total_pixels) * 100
        self.percentage_var.set(f"{percentage:.2f}%")
        
        # Создаем маскированное изображение на белом фоне
        white_background = np.full_like(self.original_image, 255)
        masked_image = cv2.bitwise_or(
            cv2.bitwise_and(white_background, white_background, mask=cv2.bitwise_not(mask)),
            cv2.bitwise_and(self.original_image, self.original_image, mask=mask)
        )
        
        # Создаем изображение с контурами
        contour_img = self.original_image.copy()
        
        # Находим контуры с учетом выбранного режима
        contours, _ = cv2.findContours(
            mask, 
            self.contour_modes[self.contour_mode.get()], 
            self.approx_methods[self.approx_method.get()]
        )

        # Фильтруем контуры по минимальной площади и периметру
        min_area = self.contour_min_area.get()
        min_perimeter = self.min_perimeter.get()
        filtered_contours = [
            cnt for cnt in contours 
            if cv2.contourArea(cnt) > min_area and cv2.arcLength(cnt, True) > min_perimeter
        ]

        # Рисуем контуры с выбранными параметрами
        contour_color = (
            self.contour_color_b.get(),
            self.contour_color_g.get(),
            self.contour_color_r.get()
        )
        thickness = self.contour_thickness.get()
        line_type = self.line_types[self.line_type.get()]

        cv2.drawContours(
            contour_img, 
            filtered_contours, 
            -1, 
            contour_color, 
            thickness,
            lineType=line_type
        )
        # Отображаем все три изображения
        self.display_images(self.original_image, masked_image, contour_img)
        
    
    def display_images(self, original, mask, contours):
        # Конвертируем изображения для отображения в Tkinter
        original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        mask_rgb = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
        contours_rgb = cv2.cvtColor(contours, cv2.COLOR_BGR2RGB)
        
        # Масштабируем изображения для отображения
        max_height = 400
        scale = max_height / original.shape[0]
        width = int(original.shape[1] * scale)
        height = int(original.shape[0] * scale)
        
        original_resized = cv2.resize(original_rgb, (width, height))
        mask_resized = cv2.resize(mask_rgb, (width, height))
        contours_resized = cv2.resize(contours_rgb, (width, height))
        
        # Конвертируем в ImageTk
        original_tk = ImageTk.PhotoImage(image=Image.fromarray(original_resized))
        mask_tk = ImageTk.PhotoImage(image=Image.fromarray(mask_resized))
        contours_tk = ImageTk.PhotoImage(image=Image.fromarray(contours_resized))
        
        # Обновляем метки
        self.original_label.config(image=original_tk)
        self.original_label.image = original_tk
        
        self.mask_label.config(image=mask_tk)
        self.mask_label.image = mask_tk
        
        self.contour_label.config(image=contours_tk)
        self.contour_label.image = contours_tk
    
    def next_image(self):
        if not self.image_files:
            return
            
        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
        self.load_current_image()
    
    def prev_image(self):
        if not self.image_files:
            return
            
        self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
        self.load_current_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorSelectorApp(root)
    root.mainloop()