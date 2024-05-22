import os
import time
from tkinter import Tk, Label, Button, filedialog, StringVar, Entry

from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
from datetime import datetime


class ImageHandler(FileSystemEventHandler):
    def __init__(self, template_path, update_status, app):
        self.template = Image.open(template_path)
        self.update_status = update_status
        self.app = app

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            self.update_status(f'Обнаружена новая фотография: {event.src_path}')
            try:
                self.app.insert_and_print_image(event.src_path)
            except Exception as e:
                self.update_status(f'Ошибка: {e}')


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Детектор")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 590
        window_height = 510
        window_x = (screen_width - window_width) // 2
        window_y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

        self.status_text = StringVar()
        self.status_text.set("Выберите шаблон...")

        self.label = Label(root, textvariable=self.status_text)
        self.label.pack(pady=20)

        self.template_path = os.path.abspath('example.jpeg')

        self.start_button = Button(root, text="Старт мониторинг", command=self.start_monitoring, state="disabled")
        self.start_button.pack(pady=5)

        self.stop_button = Button(root, text="Стоп мониторинг", command=self.stop_monitoring, state="disabled")
        self.stop_button.pack(pady=5)

        # Добавляем поля ввода для координат
        self.frame_x_label = Label(root, text="Координата X:")
        self.frame_x_label.pack()

        self.frame_x_entry = Entry(root)
        self.frame_x_entry.pack()
        self.frame_x_entry.insert(0, "85")  # значение по умолчанию для frame_x

        self.frame_y_label = Label(root, text="Координата Y:")
        self.frame_y_label.pack()

        self.frame_y_entry = Entry(root)
        self.frame_y_entry.pack()
        self.frame_y_entry.insert(0, "229")  # значение по умолчанию для frame_y

        self.frame_height_label = Label(root, text="Ширина:")
        self.frame_height_label.pack()

        self.frame_width_entry = Entry(root)
        self.frame_width_entry.pack()
        self.frame_width_entry.insert(0, "733")  # значение по умолчанию для frame_width

        self.frame_width_label = Label(root, text="Высота:")
        self.frame_width_label.pack()

        self.frame_height_entry = Entry(root)
        self.frame_height_entry.pack(pady=10)
        self.frame_height_entry.insert(0, "489")  # значение по умолчанию для frame_height

        self.photos_path = os.path.abspath('/Users/Kiti/Desktop/1357/photos/')
        self.template_inserted_path = os.path.abspath('/Users/Kiti/Desktop/1357/template_inserted/')

        self.select_template_button = Button(root, text="Выберите шаблон", command=self.select_template)
        self.select_template_button.pack(pady=5)

        self.select_photos_button = Button(root, text="Выберите папку для фотографий", command=self.select_photos)
        self.select_photos_button.pack(pady=5)

        self.select_template_inserted_button = Button(root, text="Выберите папку для вставленных изображений", command=self.select_template_inserted)
        self.select_template_inserted_button.pack(pady=5)

        self.observer = None

    def select_template(self):
        file_path = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpeg"), ("JPG files", "*.jpg")])
        if file_path:
            self.template_path = os.path.abspath(file_path)
            self.status_text.set(f"Шаблон выбран: {file_path}")
            self.start_button.config(state="normal")  # Активируем кнопку Start Monitoring
            self.select_template_button.config(text=f"Шаблон выбран: {file_path}")

    def select_photos(self):
        folder_path = filedialog.askdirectory(initialdir=self.photos_path, title="Выберите папку для фотографий")
        if folder_path:
            self.photos_path = folder_path
            self.status_text.set(f"Выбрана папка для фотографий: {folder_path}")
            self.select_photos_button.config(text=f"Папка выбрана: {folder_path}")

    def select_template_inserted(self):
        folder_path = filedialog.askdirectory(initialdir=self.template_inserted_path, title="Выберите папку для вставленных изображений")
        if folder_path:
            self.template_inserted_path = folder_path
            self.status_text.set(f"Выбрана папка для вставленных изображений: {folder_path}")
            self.select_template_inserted_button.config(text=f"Папка выбрана: {folder_path}")

    def start_monitoring(self):
        self.start_button.config(state="disabled")  # Отключаем кнопку Start Monitoring
        path_to_watch = os.path.join(self.photos_path, datetime.now().strftime("%Y_%m_%d"))

        if not os.path.exists(path_to_watch):
            os.makedirs(path_to_watch)
            self.status_text.set(f"Папка создана {path_to_watch}")
        event_handler = ImageHandler(self.template_path, self.update_status, self)
        self.observer = Observer()
        self.observer.schedule(event_handler, path_to_watch, recursive=False)
        self.observer.start()
        self.status_text.set("Мониторинг включен...")
        self.stop_button.config(state="normal")  # Включаем кнопку Stop Monitoring

    def stop_monitoring(self):
        self.stop_button.config(state="disabled")  # Отключаем кнопку Stop Monitoring
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.status_text.set("Мониторинг выключен.")
            self.start_button.config(state="normal")  # Включаем кнопку Start Monitoring

    def update_status(self, message):
        self.status_text.set(message)

    def insert_and_print_image(self, image_path):
        base_image = Image.open(self.template_path)
        self.update_status('Вставка фото в шаблон')
        with Image.open(image_path) as new_image:
            frame_x = int(self.frame_x_entry.get()) if self.frame_x_entry.get() else 85
            frame_y = int(self.frame_y_entry.get()) if self.frame_y_entry.get() else 229
            frame_width = int(self.frame_width_entry.get()) if self.frame_width_entry.get() else 733
            frame_height = int(self.frame_height_entry.get()) if self.frame_height_entry.get() else 489

            img_resized = new_image.resize((frame_width, frame_height), Image.Resampling.LANCZOS)
            base_image.paste(img_resized, (frame_x, frame_y))

            output_dir = self.template_inserted_path
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            output_path = os.path.join(output_dir, os.path.basename(image_path).split('.')[0] + '_printed.jpg')
            base_image.save(output_path)
            self.print_image(output_path)

    def print_image(self, file_path):
        self.update_status('Отправка в принтер')
        subprocess.call(['lp', file_path])


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
