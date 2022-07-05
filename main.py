import sys, os

import PySide2
# import self as self
from PySide2 import QtCore
from PySide2.QtCore import QFile, QIODevice, QSize, QRect, Qt
from PySide2.QtGui import QFont, QPixmap, QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2 import QtWidgets
from darAlta import DarAltaClass
from listadoAltas import ListadoAltas
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
        editarOrdenesButton = self.mainWindow.findChild(QPushButton, 'editarOrdenesButton')
        iconoEditarOrdenes = QIcon()
        iconoEditarOrdenes.addFile(absolute_path+"./interfaz/iconos/editar_cozmo_150.png", QSize(), QIcon.Normal, QIcon.Off)
        editarOrdenesButton.setIcon(iconoEditarOrdenes)

        #imagen boton Dar de alta niños
        darAltaButton = self.mainWindow.findChild(QPushButton, 'darAltaNinosButton')
        iconoDarAlta = QIcon()
        iconoDarAlta.addFile(absolute_path+"./interfaz/iconos/icons8-niños-150.png", QSize(), QIcon.Normal, QIcon.Off)
        darAltaButton.setIcon(iconoDarAlta)

        #imagen boton Editar informacion niños
        editarOrdenesButton = self.mainWindow.findChild(QPushButton, 'editarInfoButton')
        iconoEditarOrdenes = QIcon()
        iconoEditarOrdenes.addFile(absolute_path+"./interfaz/iconos/icons8-niños-editar-150.png", QSize(), QIcon.Normal, QIcon.Off)
        editarOrdenesButton.setIcon(iconoEditarOrdenes)


        self.childrenList_window = ListadoAltas(self)
        editarOrdenesButton.clicked.connect(self.mostrarListadoNiños)


        #imagen boton ayuda
        helpButton = self.mainWindow.findChild(QPushButton, 'help')
        iconoHelp = QIcon()
        iconoHelp.addFile(absolute_path+"./interfaz/iconos/icons8-ayuda-64.png", QSize(), QIcon.Normal, QIcon.Off)
        helpButton.setIcon(iconoHelp)

        self.opcionesSesionWindow = OpcionesSesion()
        nuevaSesionButton.clicked.connect(self.mostrarOpcionesSesion)
        self.darAlta_window = DarAltaClass(self.childrenList_window)
        self.mainWindow.show()
        darAltaButton.clicked.connect(self.darAltaNiños)
        sys.exit(self.app.exec_())

    def darAltaNiños(self):
        if self.darAlta_window.isVisible():
            self.darAlta_window.hide()
        else:
            self.darAlta_window.show()

    def mostrarListadoNiños(self):
        if self.childrenList_window.isVisible():
            self.childrenList_window.hide()
        else:
            self.childrenList_window.show()

    def mostrarOpcionesSesion(self):
        if self.opcionesSesionWindow.isVisible():
            self.opcionesSesionWindow.hide()
        else:
            self.opcionesSesionWindow.show()


if __name__ == "__main__":
    MainClass()