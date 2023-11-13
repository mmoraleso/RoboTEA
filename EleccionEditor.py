import sys

from PySide2.QtCore import QFile, QIODevice, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

from listadoAltas import ListadoAltas
from listadoHistoriaPreguntas import ListadoHistoriasPreguntas


class EleccionEditor(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowFlag(Qt.Window)
        self.formVisible = False
        self.botonHistorias.clicked.connect(self.mostrarConfiguracionH)
        self.botonPreguntas.clicked.connect(self.mostrarConfiguracionP)
        self.botonChildren.clicked.connect(self.mostrarConfiguracionChildren)

    # Creo que este metodo no sería necesario
    # def clickAceptar(self):
    #     print("click aceptar")
    #     self.guardarDatos()

    def show(self):
        self.windowEleccion.show()
        self.formVisible = True

    def hide(self):
        self.windowEleccion.hide()
        self.formVisible = False

    def isVisible(self):
        return self.formVisible

    def setupUi(self, DarAlta):

        ui_file_name2 = "./interfaz/EleccionEditor.ui"
        ui_fileDarAlta = QFile(ui_file_name2)

        if not ui_fileDarAlta.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(ui_file_name2, ui_fileDarAlta.errorString()))
            sys.exit(-1)

        loaderAlta = QUiLoader()
        self.windowEleccion = loaderAlta.load(ui_fileDarAlta)
        ui_fileDarAlta.close()

        if not self.windowEleccion:
            print(self.windowEleccion.errorString())
            sys.exit(-1)

        self.botonHistorias = self.windowEleccion.findChild(QPushButton, 'historias_button')
        self.botonPreguntas = self.windowEleccion.findChild(QPushButton, 'preguntas_button')
        self.botonChildren = self.windowEleccion.findChild(QPushButton, 'ninos_button')

    def mostrarConfiguracionH(self):
        #Nos lleva a la siguiente pantalla, el listado de historias
        self.editorDeListado = ListadoHistoriasPreguntas("H")
        self.mostrarPantalla()

    def mostrarConfiguracionP(self):
        #Nos lleva a la siguiente pantalla, el listado de preguntas
        self.editorDeListado = ListadoHistoriasPreguntas("P")
        self.mostrarPantalla()
    def mostrarConfiguracionChildren(self):
        #Nos lleva a la siguiente pantalla, el listado de niños y niñas
        self.editorDeListado = ListadoAltas()
        self.mostrarPantalla()

    def mostrarPantalla(self):
        if self.editorDeListado.isVisible():
            self.editorDeListado.hide()
        else:
            self.editorDeListado.show()
            self.windowEleccion.close()