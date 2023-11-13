import sys
import time

from PySide2 import QtWidgets
from PySide2.QtCore import QFile, QIODevice, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *


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
        QtWidgets.QApplication.processEvents()
        self.loadingBar.setValue(1)
        QtWidgets.QApplication.processEvents()


    # def setProgressingBarValue(self, robot):
    #     self.loadingBar.setValue(robot.porcentajeCarga)

    def receiveLoadingPageInfo(self, data):
        print("Valor que ha llegado a la pantalla de Carga: " + str(data))
        time.sleep(1)
        self.loadingBar.setValue(data)
        QtWidgets.QApplication.processEvents()

    def showCarga(self):
        self.windowCarga.show()
        self.formVisibleCarga = True
        time.sleep(2)

    def hideCarga(self):
        self.windowCarga.hide()
        self.formVisibleCarga = False

    def isVisibleCarga(self):
        return self.formVisibleCarga

    def getLoadingBarValue(self):
        return self.loadingBar.value()

    def closePantallaCarga(self):
        self.windowCarga.close()