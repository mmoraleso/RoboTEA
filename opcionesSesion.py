import os
import pathlib
import sys
from PySide2 import QtCore
from PySide2.QtCore import QFile, QIODevice, QSize, QRect, Qt
from PySide2.QtGui import QFont, QPixmap, QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from SesionEnCurso import SesionEnCurso
from db.queries import darAlta, actualizarDatosNiños, getById, getAll, getAllEmociones, getAllPreguntas


class OpcionesSesion(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.cargarDatos()
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

        self.historiasCB = self.windowOpciones.findChild(QComboBox, 'actividad1_CB')
        self.emocionesCB = self.windowOpciones.findChild(QComboBox, 'actividad2_CB')
        self.preguntasCB = self.windowOpciones.findChild(QComboBox, 'actividad3_CB')

        self.botonAceptar = self.windowOpciones.findChild(QPushButton, 'aceptar_opciones_button')
        self.botonCancelar = self.windowOpciones.findChild(QPushButton, 'cancelar_opciones_button')


    def cargarDatos(self):
        self.cargarDatosHistorias()
        self.cargarDatosNiñosComboBox()
        self.cargarDatosEmocionesComboBox()
        self.cargarDatosPreguntasComboBox()
    def cargarDatosNiñosComboBox(self):
        self.childrenComboBox = self.windowOpciones.findChild(QComboBox, 'childSesion_CB')
        datosNiños = getAll()
        if(datosNiños):
            for(i, fila) in enumerate(datosNiños):
                self.childrenComboBox.addItem(fila[1])

    def cargarDatosEmocionesComboBox(self):
        self.emociones = getAllEmociones()
        if(self.emociones):
            for(i, fila) in enumerate(self.emociones):
                self.emocionesCB.addItem(fila[1])

    def cargarDatosPreguntasComboBox(self):
        self.preguntas = getAllPreguntas()
        if (self.preguntas):
            for(i, fila) in enumerate(self.preguntas):
                self.preguntasCB.addItem(fila[1])

    def cargarDatosHistorias(self):
        historiasUrl = os.getcwd() + '/historias'
        directorioHistorias = os.listdir(historiasUrl)
        listadoActividades = []
        for fichero in directorioHistorias:
            if os.path.isfile(os.path.join(historiasUrl, fichero)) and fichero.endswith('.txt'):
                listadoActividades.append(fichero[:-4])
        if(listadoActividades):
            self.historiasCB.addItems(listadoActividades)

    def guardarDatos(self):

        indexEmociones = self.emocionesCB.currentIndex()
        idAprilTagEmocion = self.emociones[indexEmociones][2]
        indexPreguntas = self.preguntasCB.currentIndex()
        idPregunta = self.preguntas[indexPreguntas][0]
        historia = self.historiasCB.currentText()
        emocion = self.emocionesCB.currentText()
        pregunta = self.preguntasCB.currentText()
        niñoSesion = self.childrenComboBox.currentText()

        self.datosSesion = [historia, idPregunta, emocion, niñoSesion, idAprilTagEmocion]

    def mostrarSesion(self):
        self.guardarDatos()
        #Nos lleva a la siguiente pantalla, la pantalla de la sesión
        self.sesionEnCurso  = SesionEnCurso(self.datosSesion, self.windowOpciones)

