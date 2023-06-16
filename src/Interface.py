import sys
import FileIO
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QBoxLayout, \
    QTableWidget, QTableWidgetItem, QToolBar, QPushButton, QMessageBox, QMainWindow, QMenuBar, QAction,\
    QMenu, QListWidgetItem
from PyQt5.Qt import Qt, QColor
import SubWindows

class Interface(QMainWindow):
    """
    主窗口
    """

    def __init__(self):

        self.app = QApplication(sys.argv)

        super(Interface, self).__init__()

        self.current_window = SubWindows.SubWindow(self)
        self.ui_init()
        sys.exit(self.app.exec_())


    def ui_init(self):
        self.show()
        self.resize(1000, 800)
        self.move(400, 100)

        self.setWindowTitle('DBDesign')


        # 导航菜单设置
        self.menu_bar_init()

        self.file_window_display()


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
        self.menu_bar.triggered.connect(self.file_window_display)

        self.link_action = QAction('连接')
        self.menu_bar.addAction(self.link_action)

        self.exit_action = QAction('退出')
        self.exit_action.setShortcut(Qt.Key_Escape)
        self.exit_action.triggered.connect(self.app.quit)
        self.menu_bar.addAction(self.exit_action)

    def file_window_display(self):
        self.current_window.close()
        self.current_window = SubWindows.FileDisplayWindow(self)
        self.current_window.ui_init()
        self.current_window.display()

    def table_struct_window_display(self, file_name):
        self.current_window.close()
        self.current_window = SubWindows.DBStructDisplayWindow(self, file_name)
        self.current_window.ui_init()
        self.current_window.display()



if __name__ == '__main__':
    interface = Interface()