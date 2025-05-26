from widgets.left_panel_widget import LeftPanel

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = LeftPanel()
    #window.data_model.available_folders = ['1', '2']
    window.setWindowTitle("Multi Workspace Image Sorter")
    window.resize(1024, 768)
    window.show()
    sys.exit(app.exec_())