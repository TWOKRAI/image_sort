# controller.py

from .Models.data_model import DataModel
from .Models.file_manager import FileManager

from .view import LeftPanelView


class LeftPanelController:
    def __init__(self, view:LeftPanelView, DataModel:DataModel, FileManager:FileManager):
        self.data_model = DataModel
        self.file_manager = FileManager
        self.view = view

        # Подключение сигналов View
        #self.view.folder_combo.currentTextChanged.connect(self.update_selected_folder)
        self.view.clear_btn.clicked.connect(self.handle_clear_request)
        self.view.add_btn.clicked.connect(self.handle_add_request)

        # Подключение сигналов Model
        self.data_model.available_folders_changed.connect(self.view.update_available_folders)
        self.data_model.selected_count_changed.connect(self.view.update_select_label)
        self.data_model.page_info_changed.connect(self.view.update_page_label)
        self.data_model.selected_folder_changed.connect(self.sync_folder_combo)

        self.file_manager.folder_scan_finished.connect(
            self.handle_scan_finished
        )

        self.file_manager.set_base_scan_path('app\DataImage')


    def update_selected_folder(self, folder):
        self.data_model.selected_folder = folder

    def handle_clear_request(self):
        self.data_model.clear()

    def handle_add_request(self):
        category = self.view.input_field_category.text()
        folder_name = self.view.input_field_folder.text()
        if folder_name:
            self.file_manager.create_folder(folder_name)
            new_folders = self.data_model.available_folders + [folder_name]
            self.data_model.available_folders = new_folders
            self.view.input_field_category.clear()
            self.view.input_field_folder.clear()

    def sync_folder_combo(self, folder):
        if folder in self.data_model.available_folders:
            index = self.data_model.available_folders.index(folder)
            self.view.folder_combo.setCurrentIndex(index)

    def handle_scan_finished(self, folders):
        self.data_model.available_folders = folders
        print("Получены папки:", self.data_model.available_folders)