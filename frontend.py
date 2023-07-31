import sys

from qtpy.QtCore import QCoreApplication, Qt, QUrl, Slot
from qtpy.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QSizePolicy
from qtpy.QtWebEngineWidgets import QWebEngineView
from qtpy.QtWebChannel import QWebChannel


class ApplicationWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.webengineview = QWebEngineView()
        self.webengineview.page().profile().setHttpUserAgent(
            "Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
        )
        self.webengineview.hide()
        self.channel = QWebChannel()
        self.channel.registerObject("backend", self)
        self.webengineview.page().setWebChannel(self.channel)

        self.widget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setAutoFillBackground(False)
        self.widget.setStyleSheet("")
        button = QPushButton("Login")
        button.clicked.connect(self.open_login_page)

        layout = QVBoxLayout(self.widget)
        layout.addWidget(button)
        layout.addWidget(self.webengineview)

        self.setCentralWidget(self.widget)


    def open_login_page(self):
        self.webengineview.load(QUrl("http://localhost:8000/"))
        self.webengineview.show()

    @Slot(str)
    def foo(self, uid: str):
        print("**************", uid)


def main():
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(['', '--no-sandbox'])

    app.setOrganizationName("NamLH")
    app.setApplicationName("DemoApp")
    app.setApplicationVersion("0.1.0")

    window = ApplicationWindow()
    window.setWindowTitle("DemoApp v0.1.0")
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':

    main()