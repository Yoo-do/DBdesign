import sys
import FileIO
import DataClass
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QBoxLayout, \
    QTableWidget, QTableWidgetItem, QToolBar, QPushButton, QMessageBox, QMainWindow, QMenuBar, QAction,\
    QMenu, QListWidgetItem
from PyQt5.Qt import Qt, QColor

class Interface(QMainWindow):
    """
    主窗口
    """

    def __init__(self):
        self.app = QApplication(sys.argv)

        super(Interface, self).__init__()

        self.ui_init()
        sys.exit(self.app.exec_())


    def ui_init(self):
        self.show()
        self.resize(1000, 800)
        self.move(400, 100)

        self.setWindowTitle('DBDesign')


        # 导航菜单设置
        self.menu_bar_init()

        self.current_widget_init()
        self.set_current_widget()


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
        self.menu_bar.triggered.connect(lambda: self.set_current_widget())

        self.link_action = QAction('连接')
        self.menu_bar.addAction(self.link_action)

        self.exit_action = QAction('退出')
        self.exit_action.setShortcut(Qt.Key_Escape)
        self.exit_action.triggered.connect(lambda: self.app.quit())
        self.menu_bar.addAction(self.exit_action)

    def current_widget_init(self):
        self.current_widget = QWidget(self)
        self.current_widget.resize(self.width(), self.height() - self.menu_bar.height())
        self.current_widget.show()

    def set_current_widget(self):
        self.file_display_widget_init()

    def file_display_widget_init(self) -> QWidget:
        self.current_widget.close()
        self.current_widget_init()

        self.file_display_widget = QWidget(self.current_widget)
        self.file_display_widget.resize(self.current_widget.width(), self.current_widget.height())
        self.file_display_widget.show()

        display_layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.file_display_widget.setLayout(display_layout)

        files: list = FileIO.get_file_list()

        file_list_widget = QListWidget()
        for row, item in enumerate(files):
            file_list_widget.addItem(item['file_name'])
            if not item['valid']:
                file_list_widget.item(row).setBackground(QColor('red'))

        display_layout.addWidget(file_list_widget)


if __name__ == '__main__':
    interface = Interface()