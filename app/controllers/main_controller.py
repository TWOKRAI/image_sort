from PyQt5.QtCore import QObject

from app.views.main_view import MainView
from app.models.image_model import SortingModel


class SortingController(QObject):
    def __init__(self, model: SortingModel, view: MainView):
        super().__init__()
        self.model = model
        self.view = view

        self.view.left_panel.folder_changed.connect(self.handle_folder_change)
        self.view.left_panel.clear_requested.connect(self.clear_current_folder)

        self.view.right_panel.prev_btn_requested.connect(self.prev_item)
        self.view.right_panel.next_btn_requested.connect(self.next_item)
        self.view.right_panel.apply_requested.connect(self.handle_process)
        self.view.right_panel.delete_requested.connect(self.handle_delete)
        self.view.right_panel.select_all_requested.connect(self.handle_delete)
        self.view.right_panel.reset_requested.connect(self.handle_delete)

        self.model.data_changed.connect(self.update_view)

        self.update_combobox_category()
        self.update_view()

        # self.initialization_ui()

    def update_view(self):
        #self.view.left_panel.load_available_folders(self.model.get_name_folders())
        #         
        folder_name = self.view.left_panel.folder_combo.currentText()
        name_all_folders = self.model.get_names_folders()
        
        self.model.load_folder(folder_name)
        
        current_category = self.model.find_key_by_folder(folder_name)

        self.view.grid_widget.update_grid(image_paths = self.model.image_paths,
                                            category_config = self.model.category_config,
                                            current_category = current_category,
                                            name_all_folders = name_all_folders
                                        )
        
        self.view.left_panel.update_counter_label(len(self.model.image_paths))


    def update_combobox_category(self):
        #category_list = self.model.get_category()
        folders_list = self.model.get_names_folders()
        self.view.left_panel.load_available_items(folders_list)
    
        
    def handle_folder_change(self, folder_name):

        folder_name2 = self.view.left_panel.folder_combo.currentText()
        print(folder_name, folder_name2)
        
        try:
            self.update_view()
        except Exception as e:
            self.view.show_message("Error", str(e))


    def clear_current_folder(self):
        try:
            self.model.clear_current_folder
        except Exception as e:
            self.view.show_message("Error", str(e))


    def prev_item(self):
        pass


    def next_item(self):
        pass


    def handle_process(self, items):
        for path, category in items:
            try:
                self.model.move_image(path, category)
            except Exception as e:
                self.view.show_message("Error", f"Failed to process {path}: {str(e)}")


    def handle_delete(self, items):
        for path in items:
            try:
                self.model.delete_image(path)
            except Exception as e:
                self.view.show_message("Error", f"Failed to delete {path}: {str(e)}")


