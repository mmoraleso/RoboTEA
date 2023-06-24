import sys
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QFile, QIODevice, QSize, QRect, Qt
from PySide2.QtGui import QFont, QPixmap, QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from qtpy import QtGui

class PantallaDeCarga(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        self.setupUi()
        self.setWindowFlag(Qt.FramelessWindowHint)

    def setupUi(self):

        ui_file_name2 = "./interfaz/PantallaDeCarga.ui"
        ui_filePantallaCarga = QFile(ui_file_name2)

        if not ui_filePantallaCarga.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(ui_file_name2, ui_filePantallaCarga.errorString()))
            sys.exit(-1)

        loaderCarga = QUiLoader()
        self.windowCarga = loaderCarga.load(ui_filePantallaCarga)
        ui_filePantallaCarga.close()

        if not self.windowCarga:
            print(self.windowCarga.errorString())
            sys.exit(-1)

        self.loadingBar = self.windowCarga.findChild(QProgressBar, 'loadingBar')
