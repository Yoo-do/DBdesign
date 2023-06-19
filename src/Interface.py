import sys
from src import SubWindows
from PyQt5.QtWidgets import QApplication,QMainWindow, QMenuBar, QAction
from PyQt5.Qt import Qt


class Interface(QMainWindow):
    """
    主窗口
    """

    def __init__(self):

        self.app = QApplication(sys.argv)

        super(Interface, self).__init__()

        self.subwindows = SubWindows.SubWindow(self)
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

        self.exit_action = QAction('退出')
        self.exit_action.setShortcut(Qt.Key_Escape)
        self.exit_action.triggered.connect(self.app.quit)
        self.menu_bar.addAction(self.exit_action)

    def file_window_display(self):
        self.subwindows.switch_to_window(target_window_type=SubWindows.SubWindowType.FILE_WINDOW)

    def table_struct_window_display(self, file_name):
        self.subwindows.switch_to_window(target_window_type=SubWindows.SubWindowType.DB_STRUCT_WINDOW)

    def db_link_window_display(self):
        self.subwindows.switch_to_window(target_window_type=SubWindows.SubWindowType.DB_LINK_WINDOW)

if __name__ == '__main__':
    interface = Interface()