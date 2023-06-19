import sys
from src import SubWindows
from PyQt5.QtWidgets import QApplication,QMainWindow, QMenuBar, QAction, QInputDialog, QMessageBox
from PyQt5.Qt import Qt


class Interface(QMainWindow):
    """
    主窗口
    """

    def __init__(self):

        self.app = QApplication(sys.argv)

        super(Interface, self).__init__()

        self.subwindows = SubWindows.SubWindow(self)
        self.current_window_type: SubWindows.SubWindowType = SubWindows.SubWindowType.FILE_WINDOW
        self.ui_init()


        sys.exit(self.app.exec_())


    def ui_init(self):
        # 隐藏窗口，完成子窗口加载
        self.hide()

        self.resize(1000, 800)
        self.move(400, 100)
        self.setWindowTitle('DBDesign')

        # 导航菜单设置
        self.menu_bar_init()

        self.file_window_display()

        # 子窗口加载完成，显示主窗口
        self.show()

    def menu_bar_init(self):
        """
        菜单栏设置
        :return:
        """
        self.menu_bar = QMenuBar()
        self.menu_bar.show()
        self.setMenuBar(self.menu_bar)

        # 事件设置
        self.file_action = QAction('文件')
        self.menu_bar.addAction(self.file_action)
        self.file_action.triggered.connect(self.file_window_display)

        self.link_action = QAction('连接')
        self.menu_bar.addAction(self.link_action)
        self.link_action.triggered.connect(self.db_link_window_display)

        self.save_action = QAction('保存')
        self.save_action.setEnabled(False)
        self.save_action.triggered.connect(self.save_db_struct)
        self.menu_bar.addAction(self.save_action)


        self.exit_action = QAction('退出')
        self.exit_action.setShortcut(Qt.Key_Escape)
        self.exit_action.triggered.connect(self.app.quit)
        self.menu_bar.addAction(self.exit_action)

    def file_window_display(self):
        target_window_type = SubWindows.SubWindowType.FILE_WINDOW
        self.switch_window_type(target_window_type)
        self.subwindows.switch_to_window(target_window_type=target_window_type)

    def table_struct_window_display(self, data: SubWindows.DataClass.DBStruct):
        target_window_type = SubWindows.SubWindowType.DB_STRUCT_WINDOW
        self.switch_window_type(target_window_type)
        self.subwindows.switch_to_window(target_window_type=target_window_type, data=data)

    def db_link_window_display(self):
        target_window_type = SubWindows.SubWindowType.DB_LINK_WINDOW
        self.switch_window_type(target_window_type)
        self.subwindows.switch_to_window(target_window_type=target_window_type)

    def save_db_struct(self):
        file_name, ok = QInputDialog.getText(self, '保存', '文件名.db')
        if ok :
            if file_name in SubWindows.FileIO.FileIOUtil.get_file_list():
                confirm = QMessageBox.information(self, '提示', '该文件已存在，需要覆盖吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    SubWindows.FileIO.FileIOUtil.write_db_struct(self.subwindows.stack_widget.currentWidget().data, file_name)
            else:
                SubWindows.FileIO.FileIOUtil.write_db_struct(self.subwindows.stack_widget.currentWidget().data, file_name)


    def switch_window_type(self, window_type: SubWindows.SubWindowType):
        self.current_window_type = window_type

        if self.current_window_type == SubWindows.SubWindowType.DB_STRUCT_WINDOW:
            self.save_action.setEnabled(True)
        else:
            self.save_action.setEnabled(False)

if __name__ == '__main__':
    interface = Interface()