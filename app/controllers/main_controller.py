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
        self.view.right_panel.reset_requested.connect(self.clear_all_checkboxes)
        self.view.right_panel.select_all_requested.connect(self.handle_select_all)
        self.view.right_panel.delete_requested.connect(self.handle_delete)

        self.model.data_changed.connect(self.update_view)

        self.update_combobox_category()
        self.update_model()
        self.update_view()

        # self.initialization_ui()

    def update_model(self):
        folder_name = self.view.left_panel.folder_combo.currentText()

        self.model.load_folder(folder_name)
        self.model.create_list_model()


    def update_view(self):
        name_all_folders = self.model.get_names_folders()

        all_images = len(self.model.list_model)

        self.view.grid_widget.current_page_max = all_images // self.view.grid_widget.items_per_page

        if all_images % self.view.grid_widget.items_per_page != 0:
            self.view.grid_widget.current_page_max += 1

        start = (self.view.grid_widget.current_page - 1) * self.view.grid_widget.items_per_page
        current_images = self.model.list_model[start:start+self.view.grid_widget.items_per_page]
        
        self.view.left_panel.update_page_label(start + len(current_images), all_images)

        self.view.grid_widget.update_grid(image_list = current_images,
                                            category_config = self.model.category_config,
                                            name_all_folders = name_all_folders
                                        )


    def update_combobox_category(self):
        folders_list = self.model.get_names_folders()
        self.view.left_panel.load_available_items(folders_list)
    
        
    def handle_folder_change(self, folder_name):
        self.view.grid_widget.current_page = 1

        self.update_model()

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
        if 1 < self.view.grid_widget.current_page:
            self.view.grid_widget.current_page -= 1

        self.update_view()


    def next_item(self):
        if self.view.grid_widget.current_page < self.view.grid_widget.current_page_max:
            self.view.grid_widget.current_page += 1

        self.update_view()


    def handle_process(self):
        items = []
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


    def handle_select_all(self):
        self.view.grid_widget.set_all_checkboxes(checked=True)


    def clear_all_checkboxes(self):
        self.view.grid_widget.set_all_checkboxes(checked=False)  