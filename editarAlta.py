import sys

from PySide2.QtCore import QFile, QIODevice, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

from db.queries import actualizarDatosNiños, getById


class EditarAlta(QWidget):
    def __init__(self, _id, _listadoAlta):
        QWidget.__init__(self)
        self.id = int(_id)
        print("Se va a editar el niño con el id " + str(self.id))
        self.setupUi(self)
        self.mostrarDatosActuales()
        self.setWindowFlag(Qt.Window)
        self.formVisible = False
        self.listadoAltaClass = _listadoAlta
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
        print("Entra en darNiñosAlta")
        ui_file_name2 = "./interfaz/cuestionarioAlta.ui"
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
        genderComboBox = self.windowEditar.findChild(QComboBox, 'comboBox')
        genderComboBox.addItems(['Niño', 'Niña', 'No definido'])
        self.botonAceptar = self.windowEditar.findChild(QPushButton, 'aceptar_alta_button')
        self.botonCancelar = self.windowEditar.findChild(QPushButton, 'cancelar_alta_button')
        print("Después del show")

    def mostrarDatosActuales(self):
        self.nameLine = self.windowEditar.findChild(QLineEdit, 'lineEdit')
        self.ageSpinBox = self.windowEditar.findChild(QSpinBox, 'spinBox')
        self.genderComboBox = self.windowEditar.findChild(QComboBox, 'comboBox')
        name = self.nameLine.text()
        age = self.ageSpinBox.value()
        gender = self.genderComboBox.currentText()

        datosActuales = getById(self.id)
        print("Datos actuales: " + str(datosActuales))
        self.nameLine.setText(datosActuales[1])
        self.ageSpinBox.setValue(datosActuales[2])
        self.genderComboBox.setCurrentText(datosActuales[3])

    def comprobarDatos(self):
        name = self.nameLine.text()
        age = self.ageSpinBox.value()
        gender = self.genderComboBox.currentText()

        contadorVacios = 0

        if name == "":
            contadorVacios+=1
        if age == 0:
            contadorVacios += 1
        if gender == "":
            contadorVacios += 1

        resultado = True
        if contadorVacios > 0:
            resultado = False #Si hay fallos es false

        return resultado

    def guardarDatos(self):
        print("Se van a guardar datos")

        name = self.nameLine.text()
        age = self.ageSpinBox.value()
        gender = self.genderComboBox.currentText()

        if self.comprobarDatos():
            child = (name, age, gender)
            print(child)
            actualizarDatosNiños(self.id, child)

            self.listadoAltaClass.actualizarDatosTabla()
            self.windowEditar.close()

        else:
            print("No datos")