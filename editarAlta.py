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
        comunicacionOralComboBox = self.windowEditar.findChild(QComboBox, 'comboBox_comoral')
        teaComboBox = self.windowEditar.findChild(QComboBox, 'comboBox_tea')
        diComboBox = self.windowEditar.findChild(QComboBox, 'comboBox_di')
        genderComboBox.addItems(['Niño', 'Niña', 'No definido'])
        comunicacionOralComboBox.addItems(['Sí', 'No'])
        teaComboBox.addItems(['Sí', 'No'])
        diComboBox.addItems(['Sí', 'No'])
        self.botonAceptar = self.windowEditar.findChild(QPushButton, 'aceptar_alta_button')
        self.botonCancelar = self.windowEditar.findChild(QPushButton, 'cancelar_alta_button')
        print("Después del show")

    def mostrarDatosActuales(self):
        self.nameLine = self.windowEditar.findChild(QLineEdit, 'lineEdit')
        self.ageSpinBox = self.windowEditar.findChild(QSpinBox, 'spinBox')
        self.genderComboBox = self.windowEditar.findChild(QComboBox, 'comboBox')
        self.comunicacionOralComboBox = self.windowEditar.findChild(QComboBox, 'comboBox_comoral')
        self.teaComboBox = self.windowEditar.findChild(QComboBox, 'comboBox_tea')
        self.diComboBox = self.windowEditar.findChild(QComboBox, 'comboBox_di')

        datosActuales = getById(self.id)
        print("Datos actuales: " + str(datosActuales))
        self.nameLine.setText(datosActuales[1])
        self.ageSpinBox.setValue(datosActuales[2])
        self.genderComboBox.setCurrentText(datosActuales[3])
        self.teaComboBox.setCurrentText('Sí' if datosActuales[4] == 1 else 'No')
        self.diComboBox.setCurrentText('Sí' if datosActuales[5] == 1 else 'No')
        self.comunicacionOralComboBox.setCurrentText('Sí' if datosActuales[6] == 1  else 'No')


    def comprobarDatos(self):
        name = self.nameLine.text()
        age = self.ageSpinBox.value()
        gender = self.genderComboBox.currentText()
        comOral = self.comunicacionOralComboBox.currentIndex()
        tea = self.teaComboBox.currentIndex()
        di = self.diComboBox.currentIndex()


        contadorVacios = 0

        if name == "":
            contadorVacios+=1
        if age == 0:
            contadorVacios += 1
        if gender == "":
            contadorVacios += 1
        if tea < 0:
            contadorVacios += 1
        if comOral < 0:
            contadorVacios += 1
        if di < 0:
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
        comOral = 1 if self.comunicacionOralComboBox.currentIndex() == 0 else 0
        tea = 1 if self.teaComboBox.currentIndex() == 0 else 0
        di = 1 if self.diComboBox.currentIndex() == 0 else 0

        if self.comprobarDatos():
            child = (name, age, gender, tea, di, comOral)
            print(child)
            actualizarDatosNiños(self.id, child)

            self.listadoAltaClass.actualizarDatosTabla()
            self.windowEditar.close()

        else:
            print("No datos")