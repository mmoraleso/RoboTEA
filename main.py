import os
import signal
import sys

# import self as self
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtCore import QFile, QIODevice, QSize
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

from EleccionEditor import EleccionEditor
from opcionesSesion import OpcionesSesion

absolute_path = os.path.dirname(__file__)
if absolute_path:
    absolute_path += '/'


class MainClass(QtWidgets.QMainWindow):
    def __init__(self):
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
        self.app = QApplication(sys.argv)

        ui_file_name = absolute_path + "interfaz/mainwindow.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(ui_file_name, ui_file.errorString()))
            sys.exit(-1)
        loader = QUiLoader()
        self.mainWindow = loader.load(ui_file)
        ui_file.close()
        if not self.mainWindow:
            print(loader.errorString())
            sys.exit(-1)

        #imagen Titulo
        pixmap = QPixmap(absolute_path+"./interfaz/iconos/icons8-larva-del-moscardón-96.png")
        centralwidgetFrame = self.mainWindow.centralwidget
        iconoRobot = self.mainWindow.findChild(QLabel, 'icono_robot')
        iconoRobot.setPixmap(pixmap)

        #imagen boton Nueva Sesión
        nuevaSesionButton = self.mainWindow.findChild(QPushButton, 'nuevaSesionButton')
        iconoSesionNueva = QIcon()
        iconoSesionNueva.addFile(absolute_path+"./interfaz/iconos/cozmo.png", QSize(), QIcon.Normal, QIcon.Off)
        nuevaSesionButton.setIcon(iconoSesionNueva)

        #imagen boton Editar Ordenes Cozmo
        editarOrdenesCozmoButton = self.mainWindow.findChild(QPushButton, 'editarOrdenesButton')
        iconoEditarCozmoOrdenes = QIcon()
        iconoEditarCozmoOrdenes.addFile(absolute_path+"./interfaz/iconos/editar_cozmo_150.png", QSize(), QIcon.Normal, QIcon.Off)
        editarOrdenesCozmoButton.setIcon(iconoEditarCozmoOrdenes)

        self.mainWindow.show()

        editarOrdenesCozmoButton.clicked.connect(self.eleccionEditor)

        #imagen boton ayuda
        helpButton = self.mainWindow.findChild(QPushButton, 'help')
        iconoHelp = QIcon()
        iconoHelp.addFile(absolute_path+"./interfaz/iconos/icons8-ayuda-64.png", QSize(), QIcon.Normal, QIcon.Off)
        helpButton.setIcon(iconoHelp)

        nuevaSesionButton.clicked.connect(self.mostrarOpcionesSesion)
        sys.exit(self.app.exec_())

    def eleccionEditor(self):
        self.eleccionEditorWindow = EleccionEditor()
        if self.eleccionEditorWindow.isVisible():
            self.eleccionEditorWindow.hide()
        else:
            self.eleccionEditorWindow.show()

    def mostrarOpcionesSesion(self):
        self.opcionesSesionWindow = OpcionesSesion()
        if self.opcionesSesionWindow.isVisible():
            self.opcionesSesionWindow.hide()
        else:
            self.opcionesSesionWindow.show()

def sigint_handler(*args):
    print("Control C pulsado")
    QtCore.QCoreApplication.quit()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, sigint_handler)
    MainClass()
