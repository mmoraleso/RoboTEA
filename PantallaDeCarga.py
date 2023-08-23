import sys
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QFile, QIODevice, QSize, QRect, Qt
from PySide2.QtGui import QFont, QPixmap, QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from qtpy import QtGui
from learnblock.Cozmo import Robot

class PantallaDeCarga(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi()
        self.formVisibleCarga = False
        self.setWindowFlag(Qt.Window)

    def setupUi(self):
        print("Creando setup Pantalla de Carga")
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
        self.setWindowTitle("Pantalla de Carga")
        self.loadingBar = self.windowCarga.findChild(QProgressBar, 'loadingBar')
        self.loadingBar.setValue(0)

    def setProgressingBarValue(self, robot):
        self.loadingBar.setValue(robot.porcentajeCarga)

    def receiveLoadingPageInfo(self, data):
        print("Valor que ha llegado a la pantalla de Carga: " + str(data))
        self.loadingBar.setValue(data)

    def showCarga(self):
        self.windowCarga.show()
        self.formVisibleCarga = True

    def hideCarga(self):
        self.windowCarga.hide()
        self.formVisibleCarga = False

    def isVisibleCarga(self):
        return self.formVisibleCarga

    def getLoadingBarValue(self):
        return self.loadingBar.value()

