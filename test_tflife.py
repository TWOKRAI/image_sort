import os
import numpy as np
from PIL import Image
from tqdm import tqdm
import random
import tensorflow as tf
import time

class Timer:
    def __init__(self, name):
        self.name = name
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def elapsed_time(self, print_log=False):
        if self.start_time is None:
            return 0
        elapsed = time.time() - self.start_time
        if print_log:
            print(f"Таймер {self.name} {elapsed * 1000} мс")
        return elapsed

timer = Timer('time_neuroun')

def collect_image_paths(source_dir):
    """Собирает все изображения из source_dir и всех вложенных подпапок."""
    image_paths = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.join(root, file))
    print('Количество изображений:', len(image_paths))
    return image_paths

def load_and_preprocess(image_path, target_size=(72, 72)):
    """Загрузка и предобработка изображения."""
    img = Image.open(image_path)
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0
    return img_array

def process_images_in_batches(image_paths, max_batch_size=10):
    """Обрабатывает изображения батчами случайного размера от 1 до max_batch_size."""
    total = len(image_paths)
    pbar = tqdm(total=total)

    while image_paths:
        current_max = min(max_batch_size, len(image_paths))
        batch_size = random.randint(1, current_max)
        batch_paths = image_paths[:batch_size]
        del image_paths[:batch_size]

        images = [load_and_preprocess(path) for path in batch_paths]
        images = np.array(images)

        yield images, batch_paths

        pbar.update(len(batch_paths))

    pbar.close()

def validate_tflite_model(model_path, test_dir):
    interpreter = tf.lite.Interpreter(model_path=model_path)
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]

    image_paths = collect_image_paths(test_dir)
    total_correct = 0
    total_samples = 0
    total_inference_time = 0
    total_batches = 0

    for images, batch_paths in process_images_in_batches(image_paths):
        batch_size = len(images)
        # Изменяем размер входного тензора под текущий батч
        interpreter.resize_tensor_input(input_details['index'], (batch_size, 72, 72, 3))
        interpreter.allocate_tensors()

        input_data = images.astype(np.float32)
        interpreter.set_tensor(input_details['index'], input_data)

        start_time = time.time()
        interpreter.invoke()
        batch_time = time.time() - start_time
        total_inference_time += batch_time
        total_batches += 1
        total_samples += batch_size

        # Пример: предполагаем, что все изображения относятся к классу 0
        predictions = interpreter.get_tensor(output_details['index'])
        predicted_labels = np.argmax(predictions, axis=1)
        true_labels = np.zeros(batch_size, dtype=int)
        correct = np.sum(predicted_labels == true_labels)
        total_correct += correct

        print(f"Батч из {batch_size} изображений обработан за {batch_time:.4f} секунд")

    if total_samples == 0:
        accuracy = 0.0
    else:
        accuracy = total_correct / total_samples
    average_inference_time = total_inference_time / total_batches if total_batches > 0 else 0
    print(f'\nТочность: {accuracy:.4f}')
    return accuracy, average_inference_time

def validate_keras_model(model_path, test_dir):
    model = tf.keras.models.load_model(model_path)

    image_paths = collect_image_paths(test_dir)
    total_correct = 0
    total_samples = 0
    total_inference_time = 0
    total_batches = 0

    for images, batch_paths in process_images_in_batches(image_paths):
        batch_size = len(images)
        start_time = time.time()
        predictions = model.predict(images, verbose=0)
        batch_time = time.time() - start_time
        total_inference_time += batch_time
        total_batches += 1
        total_samples += batch_size

        # Пример: предполагаем, что все изображения относятся к классу 0
        predicted_labels = np.argmax(predictions, axis=1)
        true_labels = np.zeros(batch_size, dtype=int)
        correct = np.sum(predicted_labels == true_labels)
        total_correct += correct

        print(f"Батч из {batch_size} изображений обработан за {batch_time:.4f} секунд")

    if total_samples == 0:
        accuracy = 0.0
    else:
        accuracy = total_correct / total_samples
    average_inference_time = total_inference_time / total_batches if total_batches > 0 else 0
    print(f'\nТочность: {accuracy:.4f}')
    return accuracy, average_inference_time

# Пример использования:
model_path = 'waffle_classifier_v1201_big.keras'
test_dir = r'C:\Users\INNOTECH\Downloads\Save_brak2_1704\test'

original_accuracy, original_inference_time = validate_keras_model(model_path, test_dir)
quant_accuracy, quant_inference_time = validate_tflite_model('optimized_float16_model.tflite', test_dir)

print(f'Итоговая точность оригинальной модели: {original_accuracy:.2%}')
print(f'Итоговое время инференса оригинальной модели: {original_inference_time:.4f} секунд')
print(f'Итоговая точность квантованной модели: {quant_accuracy:.2%}')
print(f'Итоговое время инференса квантованной модели: {quant_inference_time:.4f} секунд')