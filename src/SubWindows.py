from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QBoxLayout, \
    QTableWidget, QTableWidgetItem, QToolBar, QPushButton, QMessageBox, QMainWindow, QMenuBar, QAction,\
    QMenu, QListWidgetItem
from PyQt5.Qt import Qt, QColor
import DataClass
import FileIO


class SubWindow(QWidget):
    """
    子窗口基类
    """

    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window
        super().__init__(self.main_window)


    def display(self):
        self.show()
        self.main_window.setCentralWidget(self)

    def close(self):
        self.deleteLater()
class FileDisplayWindow(SubWindow):
    """
    文件展示widget
    """
    def ui_init(self):
        display_layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(display_layout)

        files: list = FileIO.get_file_list()

        file_list_widget = QListWidget()
        for file in files:
            item = QListWidgetItem(file['file_name'])
            if not file['valid']:
                item.setBackground(QColor(255,0,0))
            file_list_widget.addItem(item)

        display_layout.addWidget(file_list_widget)
