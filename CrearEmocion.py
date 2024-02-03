import sys

from PySide2.QtCore import QFile, QIODevice, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

from db.queries import darAltaEmociones


class CrearEmocion(QWidget):
    def __init__(self, listado, parent=None):
        QWidget.__init__(self, parent=None)

        self.setupUi(self)
        self.setWindowFlag(Qt.Window)
        self.formVisible = False
        self.botonAceptar.clicked.connect(self.guardarDatos)
        self.botonCancelar.clicked.connect(lambda : self.windowEditar.close())
        self.listadoEmocionClass = listado

    def clickAceptar(self):
        print("click aceptar")
        self.guardarDatos()

    def show(self):
        self.windowAlta.show()
        self.formVisible = True


    def hide(self):
        self.windowAlta.hide()
        self.formVisible = False

    def isVisible(self):
        return self.formVisible

    def setupUi(self, DarAlta):
        ui_file_name2 = "./interfaz/CrearEmocion.ui"
        ui_fileDarAlta = QFile(ui_file_name2)
        if not ui_fileDarAlta.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(ui_file_name2, ui_fileDarAlta.errorString()))
            sys.exit(-1)
        loaderAlta = QUiLoader()
        self.windowAlta = loaderAlta.load(ui_fileDarAlta)
        ui_fileDarAlta.close()
        if not self.windowAlta:
            print(self.windowAlta.errorString())
            sys.exit(-1)
        self.emocionTE = self.windowAlta.findChild(QTextEdit, 'tituloTextEdit_2')
        self.aprilTagSpinBox = self.windowAlta.findChild(QSpinBox, 'spinBox')
        self.botonAceptar = self.windowAlta.findChild(QPushButton, 'aceptar_alta_button_2')
        self.botonCancelar = self.windowAlta.findChild(QPushButton, 'cancelar_alta_button_2')
        self.windowAlta.setWindowTitle("Crear")
        print("Después del show")



    def comprobarDatos(self):

        name = self.emocionTE.toPlainText()
        age = self.aprilTagSpinBox.value()

        contadorVacios = 0

        if name == "":
            contadorVacios+=1
        if age == 0:
            contadorVacios += 1

        resultado = True
        if contadorVacios > 0:
            resultado = False #Si hay fallos es false

        return resultado

    def guardarDatos(self):
        emocion = self.emocionTE.toPlainText()
        apriltag = self.aprilTagSpinBox.value()

        if self.comprobarDatos():
            emocionToSave = (emocion, apriltag)
            print(emocionToSave)
            darAltaEmociones(emocionToSave)
            self.listadoEmocionClass.actualizarDatosTabla()
            self.windowAlta.close()
        else:
            print("No datos")
            self.windowAlta.close()