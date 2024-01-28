
import sys

from PySide2.QtCore import QFile, QIODevice, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

from db.queries import actualizarEmocion, getEmocionById


class EditarEmocion(QWidget):
    def __init__(self, _id, _listadoEmociones):
        QWidget.__init__(self)
        self.id = int(_id)
        print("Se va a editar la emocion con el id " + str(self.id))
        self.setupUi(self)
        self.mostrarDatosActuales()
        self.setWindowFlag(Qt.Window)
        self.formVisible = False
        self.listadoEmocionesClass = _listadoEmociones
        self.botonAceptar.clicked.connect(self.guardarDatos)
        self.botonCancelar.clicked.connect(lambda : self.windowEditar.close())

    def clickAceptar(self):
        print("click aceptar")
        self.guardarDatos()

    def show(self):
        self.windowEditar.show()
        self.formVisible = True

    def hide(self):
        self.windowEditar.hide()
        self.formVisible = False

    def isVisible(self):
        return self.formVisible

    def setupUi(self, DarAlta):
        ui_file_name2 = "./interfaz/EditarEmocion.ui"
        ui_fileDarAlta = QFile(ui_file_name2)
        if not ui_fileDarAlta.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(ui_file_name2, ui_fileDarAlta.errorString()))
            sys.exit(-1)
        loaderAlta = QUiLoader()
        self.windowEditar = loaderAlta.load(ui_fileDarAlta)
        ui_fileDarAlta.close()
        if not self.windowEditar:
            print(self.windowEditar.errorString())
            sys.exit(-1)

        self.botonAceptar = self.windowEditar.findChild(QPushButton, 'aceptar_alta_button')
        self.botonCancelar = self.windowEditar.findChild(QPushButton, 'cancelar_alta_button')
        print("Después del show")

    def mostrarDatosActuales(self):
        self.emocionTE = self.windowEditar.findChild(QTextEdit, 'emocionTextEdit')
        self.aprilTagSpinBox = self.windowEditar.findChild(QSpinBox, 'spinBox')
        emocion = self.emocionTE.toPlainText()
        apriltag = self.aprilTagSpinBox.value()

        datosActuales = getEmocionById(self.id)
        print("Datos actuales: " + str(datosActuales))
        self.emocionTE.setText(datosActuales[0])
        self.aprilTagSpinBox.setValue(datosActuales[1])

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
        print("Se van a guardar datos")

        emocion = self.emocionTE.toPlainText()
        apriltag = self.aprilTagSpinBox.value()

        if self.comprobarDatos():
            emocionToSave = (emocion, apriltag)
            print(emocionToSave)
            actualizarEmocion(self.id, emocionToSave)

            self.listadoEmocionesClass.actualizarDatosTabla()
            self.windowEditar.close()

        else:
            print("No datos")