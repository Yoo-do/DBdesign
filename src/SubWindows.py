from PyQt5.QtWidgets import  QWidget, QListWidget, QBoxLayout, \
    QTableWidget, QTableWidgetItem,  QPushButton, QMessageBox, QMainWindow, QListWidgetItem, QLabel, QLineEdit, QStackedWidget
from PyQt5.Qt import Qt
import DataClass, FileIO, DBLink
from enum import Enum


class SubWindowBase(QWidget):
    """
    子窗口基类
    """

    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window
        super().__init__(self.main_window)



class SubWindowType(Enum):
    FILE_WINDOW = 0,
    DB_LINK_WINDOW = 1,
    DB_STRUCT_WINDOW = 2,


class SubWindow:
    """
    子窗口管理类
    """

    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window
        self.stack_widget = QStackedWidget(main_window)
        main_window.setCentralWidget(self.stack_widget)


        self.file_window_init()
        self.db_link_window_init()
        self.db_struct_window_init()




    def switch_to_window(self, target_window_type: SubWindowType, data=DataClass.DBStruct('')):
        self.stack_widget.setCurrentIndex(target_window_type.value[0])
        if target_window_type == SubWindowType.DB_STRUCT_WINDOW:
            self.stack_widget.currentWidget().fresh_data(data)
        else:
            self.stack_widget.currentWidget().fresh_data()


    def file_window_init(self):
        """
        初始化文件展示窗口
        :return:
        """
        file_window = FileDisplayWindow(self.main_window)
        file_window.ui_init()

        self.stack_widget.addWidget(file_window)

    def db_struct_window_init(self):
        """
        初始化数据库展示窗口
        :return:
        """
        db_struct_window = DBStructDisplayWindow(self.main_window)
        db_struct_window.ui_init()

        self.stack_widget.addWidget(db_struct_window)

    def db_link_window_init(self):
        """
        数据库；连接窗口展示
        :return:
        """
        db_link_window = DBlinkDisplayWindow(self.main_window)
        db_link_window.ui_init()

        self.stack_widget.addWidget(db_link_window)



class FileDisplayWindow(SubWindowBase):
    """
    文件展示widget
    """

    def ui_init(self):
        display_layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(display_layout)

        self.file_list_widget = QListWidget()

        self.file_list_widget.itemDoubleClicked.connect(lambda: self.main_window.table_struct_window_display(FileIO.FileIOUtil.get_db_struct(self.file_list_widget.currentItem().text())))

        display_layout.addWidget(self.file_list_widget)

    def fresh_data(self):
        files: list = FileIO.FileIOUtil.get_file_list()

        self.file_list_widget.clear()
        self.file_list_widget.addItems(files)


class DBStructDisplayWindow(SubWindowBase):
    def ui_init(self):
        window_layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.setLayout(window_layout)

        # schema选项框
        self.schema_list_widget = QListWidget(self)
        window_layout.addWidget(self.schema_list_widget)
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

    def fresh_data(self, data: DataClass.DBStruct):
        """
        导入新的数据库结构数据，并刷新当前窗口
        :param data:
        :return:
        """
        self.data = data
        self.schema_list_widget.clear()
        self.table_list_widget.clear()

        self.column_table.setRowCount(0)
        self.column_table.horizontalHeader().hide()

        self.schema_list_widget.addItems(data.get_schema_names())

    def schema_selected(self):
        curr_schema_name = self.schema_list_widget.currentItem().text()
        self.table_list_widget.clear()

        self.table_list_widget.addItems(self.data.get_schema(curr_schema_name).get_table_names())

        for index, note in enumerate(self.data.get_schema(curr_schema_name).get_table_notes()):
            self.table_list_widget.item(index).setToolTip(note)

    def tabel_selected(self):
        """
        table列表选择后的相应，展示对应的列信息
        :return:
        """
        curr_schema_name = self.schema_list_widget.currentItem().text()
        curr_table_name = self.table_list_widget.currentItem().text()

        tittle_info, column_info = self.data.get_schema(curr_schema_name).get_table(curr_table_name).get_column_infos()

        self.column_table.clear()
        self.column_table.setColumnCount(len(tittle_info))
        self.column_table.setRowCount(len(column_info))

        self.column_table.setHorizontalHeaderLabels(tittle_info)
        self.column_table.horizontalHeader().show()
        for row, column_list in enumerate(column_info):
            for col, column in enumerate(column_list):
                new_item = QTableWidgetItem(column)
                self.column_table.setItem(row, col, new_item)


class DBlinkDisplayWindow(SubWindowBase):
    """
    用于记录数据库连接
    """

    def ui_init(self):
        window_layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.setLayout(window_layout)

        # 数据库连接列表
        db_config_list_layout = QBoxLayout(QBoxLayout.TopToBottom)
        window_layout.addLayout(db_config_list_layout)
        window_layout.setStretchFactor(db_config_list_layout, 1)

        self.db_config_list_widget = QListWidget(self)
        self.db_config_list_widget.itemClicked.connect(self.db_config_selected)
        db_config_list_layout.addWidget(self.db_config_list_widget)

        db_config_button_layout = QBoxLayout(QBoxLayout.LeftToRight)
        db_config_list_layout.addLayout(db_config_button_layout)

        self.db_config_add_button = QPushButton('新增', self)
        self.db_config_add_button.clicked.connect(self.db_config_add_action)
        db_config_button_layout.addWidget(self.db_config_add_button)

        self.db_config_delete_button = QPushButton('删除', self)
        self.db_config_delete_button.clicked.connect(self.db_config_delete_action)
        db_config_button_layout.addWidget(self.db_config_delete_button)


        # 数据库配置展示框
        self.db_config_info_widget = QWidget(self)
        self.db_config_info_widget.show()
        window_layout.addWidget(self.db_config_info_widget)
        window_layout.setStretchFactor(self.db_config_info_widget, 4)


    def fresh_data(self):
        # 获取缓存中数据库配置信息
        self.db_config_io = FileIO.DBConfigIO()

        # 需要保存的 db_config

        self.db_config_list_widget.clear()

        self.db_config_list_widget.addItems([config.link_name for config in self.db_config_io.db_config])



    def fresh_config_data(self, item: QListWidgetItem):
        current_config = self.db_config_io.db_config[self.db_config_list_widget.row(item)]

        self.link_name_edit.setText(current_config.link_name)
        self.host_line_edit.setText(current_config.host)
        self.port_line_edit.setText(current_config.port)
        self.database_line_edit.setText(current_config.database)
        self.user_line_edit.setText(current_config.user)
        self.password_line_edit.setText(current_config.password)

    @staticmethod
    def line_widget(parent: QWidget, label_text: str):
        widget = QWidget(parent)
        layout = QBoxLayout(QBoxLayout.LeftToRight)
        widget.setLayout(layout)
        label = QLabel(label_text, widget)
        layout.addWidget(label)
        line_edit = QLineEdit(widget)
        layout.addWidget(line_edit)

        return widget, line_edit

    def db_config_selected(self, item: QListWidgetItem):

        if len(self.db_config_info_widget.children()) > 0:
            self.fresh_config_data(item)
            return

        db_config_info_widget_layout = QBoxLayout(QBoxLayout.TopToBottom)
        db_config_info_widget_layout.setAlignment(Qt.AlignCenter)
        self.db_config_info_widget.setLayout(db_config_info_widget_layout)

        self.link_name_widget, self.link_name_edit = self.line_widget(self.db_config_info_widget, 'name     : ')
        db_config_info_widget_layout.addWidget(self.link_name_widget)


        self.host_widget, self.host_line_edit = self.line_widget(self.db_config_info_widget, 'host     : ')
        db_config_info_widget_layout.addWidget(self.host_widget)

        self.port_widget, self.port_line_edit = self.line_widget(self.db_config_info_widget, 'port     : ')
        db_config_info_widget_layout.addWidget(self.port_widget)

        self.database_widget, self.database_line_edit = self.line_widget(self.db_config_info_widget, 'database : ')
        db_config_info_widget_layout.addWidget(self.database_widget)

        self.user_widget, self.user_line_edit = self.line_widget(self.db_config_info_widget, 'user     : ')
        db_config_info_widget_layout.addWidget(self.user_widget)

        self.password_widget, self.password_line_edit = self.line_widget(self.db_config_info_widget, 'password : ')
        db_config_info_widget_layout.addWidget(self.password_widget)

        group_button_layout = QBoxLayout(QBoxLayout.LeftToRight)
        db_config_info_widget_layout.addLayout(group_button_layout)

        save_button = QPushButton('保存')
        save_button.clicked.connect(self.save_config_info)
        group_button_layout.addWidget(save_button)

        test_button = QPushButton('测试连接')
        test_button.clicked.connect(self.test_button_action)
        group_button_layout.addWidget(test_button)

        query_button = QPushButton('查看结构')
        query_button.clicked.connect(self.query_button_action)
        group_button_layout.addWidget(query_button)

        self.fresh_config_data(item)

    def save_config_info(self):
        current_row = self.db_config_list_widget.row(self.db_config_list_widget.selectedItems()[0])
        current_config = self.db_config_io.db_config[current_row]

        current_config.link_name = self.link_name_edit.text()
        current_config.host = self.host_line_edit.text()
        current_config.port = self.port_line_edit.text()
        current_config.database = self.database_line_edit.text()
        current_config.user = self.user_line_edit.text()
        current_config.password = self.password_line_edit.text()

        self.save_action()
        self.fresh_data()
        self.db_config_list_widget.item(current_row).setSelected(True)


    def db_config_add_action(self):
        self.db_config_io.add_link(f"link{len(self.db_config_io.db_config)+1}")
        self.save_action()
        self.fresh_data()
    def db_config_delete_action(self):
        self.db_config_io.delete_link(self.db_config_io.db_config[self.db_config_list_widget.currentRow()].sort_no)
        self.save_action()
        self.fresh_data()

    def save_action(self):
        self.db_config_io.save_link()

    def test_button_action(self):
        host = self.host_line_edit.text()
        database = self.database_line_edit.text()
        port = self.port_line_edit.text()
        user = self.user_line_edit.text()
        password = self.password_line_edit.text()

        db_link = DBLink.PostgresLink(host=host, database=database, port=port, user=user, password=password)
        is_ok, text_info = db_link.connect_test()

        if is_ok:
            QMessageBox.information(self.db_config_info_widget, '测试消息', text_info, QMessageBox.Ok)
        else:
            QMessageBox.critical(self.db_config_info_widget, '测试消息', text_info, QMessageBox.Ok)

    def query_button_action(self):
        host = self.host_line_edit.text()
        database = self.database_line_edit.text()
        port = self.port_line_edit.text()
        user = self.user_line_edit.text()
        password = self.password_line_edit.text()

        db_link = DBLink.PostgresLink(host=host, database=database, port=port, user=user, password=password)
        is_ok, text_info = db_link.connect_test()

        if is_ok:
            db_link.get_connected()
            db_struct = db_link.get_db_struct(database)
            db_link.close()

            self.main_window.table_struct_window_display(db_struct)
        else:
            QMessageBox.critical(self.db_config_info_widget, '测试消息', text_info, QMessageBox.Ok)
