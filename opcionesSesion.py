import sys
from PySide2 import QtCore
from PySide2.QtCore import QFile, QIODevice, QSize, QRect, Qt
from PySide2.QtGui import QFont, QPixmap, QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from SesionEnCurso import SesionEnCurso
from db.queries import darAlta, actualizarDatosNiños, getById, getAll


class OpcionesSesion(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.cargarDatosComboBox()
        self.setWindowFlag(Qt.Window)
        self.formVisible = False
        self.botonAceptar.clicked.connect(self.mostrarSesion)
        self.botonCancelar.clicked.connect(lambda : self.windowOpciones.close())
        self.datosSesion = {}

    # Creo que este metodo no sería necesario
    # def clickAceptar(self):
    #     print("click aceptar")
    #     self.guardarDatos()

    def show(self):
        self.windowOpciones.show()
        self.formVisible = True

    def hide(self):
        self.windowOpciones.hide()
        self.formVisible = False

    def isVisible(self):
        return self.formVisible

    def setupUi(self, DarAlta):

        ui_file_name2 = "./interfaz/opcionesSesion.ui"
        ui_fileDarAlta = QFile(ui_file_name2)

        if not ui_fileDarAlta.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(ui_file_name2, ui_fileDarAlta.errorString()))
            sys.exit(-1)

        loaderAlta = QUiLoader()
        self.windowOpciones = loaderAlta.load(ui_fileDarAlta)
        ui_fileDarAlta.close()

        if not self.windowOpciones:
            print(self.windowOpciones.errorString())
            sys.exit(-1)

        self.actividad1CB = self.windowOpciones.findChild(QComboBox, 'actividad1_CB')
        self.actividad1CB.addItems(['Actividad1', 'Actividad2', 'Actividad3'])
        self.actividad2CB = self.windowOpciones.findChild(QComboBox, 'actividad2_CB')
        self.actividad2CB.addItems(['Actividad1', 'Actividad2', 'Actividad3'])
        self.actividad3CB = self.windowOpciones.findChild(QComboBox, 'actividad3_CB')
        self.actividad3CB.addItems(['Actividad1', 'Actividad2', 'Actividad3'])

        self.botonAceptar = self.windowOpciones.findChild(QPushButton, 'aceptar_opciones_button')
        self.botonCancelar = self.windowOpciones.findChild(QPushButton, 'cancelar_opciones_button')


    def cargarDatosComboBox(self):
        self.childrenComboBox = self.windowOpciones.findChild(QComboBox, 'childSesion_CB')
        datosNiños = getAll()

        for(i, fila) in enumerate(datosNiños):
            self.childrenComboBox.addItem(fila[1])

    def guardarDatos(self):

        actividad1 = self.actividad1CB.currentText()
        actividad2 = self.actividad2CB.currentText()
        actividad3 = self.actividad3CB.currentText()
        niñoSesion = self.childrenComboBox.currentText()

        self.datosSesion = [actividad1, actividad2, actividad3, niñoSesion]

    def mostrarSesion(self):
        self.guardarDatos()
        #Nos lleva a la siguiente pantalla, la pantalla de la sesión
        self.sesionEnCurso  = SesionEnCurso(self.datosSesion, self.windowOpciones)

