from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QBoxLayout, \
    QTableWidget, QTableWidgetItem, QToolBar, QPushButton, QMessageBox, QMainWindow, QMenuBar, QAction,\
    QMenu, QListWidgetItem
from PyQt5.Qt import Qt, QColor
from PyQt5 import QtCore
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
                # item.setBackground(QColor(255,0,0))
                item.setFlags(QtCore.Qt.NoItemFlags)
            file_list_widget.addItem(item)

        file_list_widget.itemDoubleClicked.connect(lambda: self.main_window.table_struct_window_display(file_list_widget.currentItem().text()) )

        display_layout.addWidget(file_list_widget)




class DBStructDisplayWindow(SubWindow):
    def __init__(self, main_window: QMainWindow, file_name):
        super().__init__(main_window)
        self.file_name = file_name
        self.data: DataClass.DBStruct = FileIO.get_db_struct_by_file_name(file_name)
    def ui_init(self):
        window_layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.setLayout(window_layout)

        # schema选项框
        self.schema_list_widget = QListWidget(self)
        window_layout.addWidget(self.schema_list_widget)
        self.schema_list_widget.addItems(self.data.get_schema_names())
        self.schema_list_widget.itemClicked.connect(self.schema_selected)
        window_layout.setStretchFactor(self.schema_list_widget, 1)

        # table选项框
        self.table_list_widget = QListWidget(self)
        window_layout.addWidget(self.table_list_widget)
        self.table_list_widget.itemClicked.connect(self.tabel_selected)
        window_layout.setStretchFactor(self.table_list_widget, 4)

        # column展示框
        self.column_table = QTableWidget(self)
        self.column_table.show()
        window_layout.addWidget(self.column_table)
        window_layout.setStretchFactor(self.column_table, 8)

    def schema_selected(self):
        curr_schema_name = self.schema_list_widget.currentItem().text()
        self.table_list_widget.clear()

        self.table_list_widget.addItems(self.data.get_schema(curr_schema_name).get_table_names())

        for index, note in enumerate(self.data.get_schema(curr_schema_name).get_table_notes()):
            self.table_list_widget.item(index).setToolTip(note)


    def tabel_selected(self):
        curr_schema_name = self.schema_list_widget.currentItem().text()
        curr_table_name = self.table_list_widget.currentItem().text()

        tittle_info, column_info = self.data.get_schema(curr_schema_name).get_table(curr_table_name).get_column_infos()

        self.column_table.clear()
        self.column_table.setColumnCount(len(tittle_info))
        self.column_table.setRowCount(len(column_info))

        self.column_table.setHorizontalHeaderLabels(tittle_info)
        for row, column_list in enumerate(column_info):
            for col, column in enumerate(column_list):
                new_item = QTableWidgetItem(column)
                self.column_table.setItem(row, col, new_item)