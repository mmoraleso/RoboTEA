import sys

import PySide2
from PySide2 import QtCore
from PySide2.QtCore import QFile, QIODevice, QSize, QRect, Qt
from PySide2.QtGui import QFont, QPixmap, QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from darAlta import NewChildren




def darAltaNiños(self):
    window = NewChildren(self)
    #window.show()


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)

    ui_file_name = "interfaz/mainwindow.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print("Cannot open {}: {}".format(ui_file_name, ui_file.errorString()))
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)

    #imagen Titulo
    pixmap = QPixmap("./interfaz/iconos/icons8-larva-del-moscardón-96.png")
    centralwidgetFrame = window.centralwidget
    iconoRobot = window.findChild(QLabel, 'icono_robot')
    iconoRobot.setPixmap(pixmap)

    #imagen boton Nueva Sesión
    nuevaSesionButton = window.findChild(QPushButton, 'nuevaSesionButton')
    iconoSesionNueva = QIcon()
    iconoSesionNueva.addFile("./interfaz/iconos/cozmo.png", QSize(), QIcon.Normal, QIcon.Off)
    nuevaSesionButton.setIcon(iconoSesionNueva)

    #imagen boton Editar Ordenes Cozmo
    editarOrdenesButton = window.findChild(QPushButton, 'editarOrdenesButton')
    iconoEditarOrdenes = QIcon()
    iconoEditarOrdenes.addFile("./interfaz/iconos/editar_cozmo_150.png", QSize(), QIcon.Normal, QIcon.Off)
    editarOrdenesButton.setIcon(iconoSesionNueva)

    #imagen boton Dar de alta niños
    darAltaButton = window.findChild(QPushButton, 'darAltaNinosButton')
    iconoDarAlta = QIcon()
    iconoDarAlta.addFile("./interfaz/iconos/icons8-niños-150.png", QSize(), QIcon.Normal, QIcon.Off)
    darAltaButton.setIcon(iconoDarAlta)

    #imagen boton Editar informacion niños
    editarOrdenesButton = window.findChild(QPushButton, 'editarInfoButton')
    iconoEditarOrdenes = QIcon()
    iconoEditarOrdenes.addFile("./interfaz/iconos/icons8-niños-editar-150.png", QSize(), QIcon.Normal, QIcon.Off)
    editarOrdenesButton.setIcon(iconoEditarOrdenes)

    #imagen boton ayuda
    helpButton = window.findChild(QPushButton, 'help')
    iconoHelp = QIcon()
    iconoHelp.addFile("./interfaz/iconos/icons8-ayuda-64.png", QSize(), QIcon.Normal, QIcon.Off)
    helpButton.setIcon(iconoHelp)

    #darAltaButton.setCheckable(False)
    window.show()
    darAltaButton.clicked.connect(darAltaNiños)
    sys.exit(app.exec_())
