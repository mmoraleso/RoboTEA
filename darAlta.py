import sys

from PySide2.QtCore import QFile, QIODevice, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

from db.queries import darAlta


class DarAltaClass(QWidget):
    def __init__(self, listado, parent=None):
        QWidget.__init__(self, parent=None)

        self.setupUi(self)
        self.setWindowFlag(Qt.Window)
        self.formVisible = False
        self.botonAceptar.clicked.connect(self.guardarDatos)
        self.botonCancelar.clicked.connect(lambda: self.windowAlta.close())
        self.listadoAltasClass = listado

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
        ui_file_name2 = "./interfaz/cuestionarioAlta.ui"
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
        genderComboBox = self.windowAlta.findChild(QComboBox, 'comboBox')
        comunicacionOralComboBox = self.windowAlta.findChild(QComboBox, 'comboBox_comoral')
        teaComboBox = self.windowAlta.findChild(QComboBox, 'comboBox_tea')
        diComboBox = self.windowAlta.findChild(QComboBox, 'comboBox_di')
        genderComboBox.addItems(['Niño', 'Niña', 'No definido'])
        comunicacionOralComboBox.addItems(['Sí', 'No'])
        teaComboBox.addItems(['Sí', 'No'])
        diComboBox.addItems(['Sí', 'No'])
        self.botonAceptar = self.windowAlta.findChild(QPushButton, 'aceptar_alta_button')
        self.botonCancelar = self.windowAlta.findChild(QPushButton, 'cancelar_alta_button')
        self.windowAlta.setWindowTitle("Crear")
        print("Después del show")


        #windowCuestionarioAlta.activateWindow()

    def comprobarDatos(self):
        nameLine = self.windowAlta.findChild(QLineEdit, 'lineEdit')
        ageSpinBox = self.windowAlta.findChild(QSpinBox, 'spinBox')
        genderComboBox = self.windowAlta.findChild(QComboBox, 'comboBox')
        comunicacionOralComboBox = self.windowAlta.findChild(QComboBox, 'comboBox_comoral')
        teaComboBox = self.windowAlta.findChild(QComboBox, 'comboBox_tea')
        diComboBox = self.windowAlta.findChild(QComboBox, 'comboBox_di')
        name = nameLine.text()
        age = ageSpinBox.value()
        gender = genderComboBox.currentText()
        comOral = comunicacionOralComboBox.currentIndex()
        tea = teaComboBox.currentIndex()
        di = diComboBox.currentIndex()

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
        nameLine = self.windowAlta.findChild(QLineEdit, 'lineEdit')
        ageSpinBox = self.windowAlta.findChild(QSpinBox, 'spinBox')
        genderComboBox = self.windowAlta.findChild(QComboBox, 'comboBox')
        comunicacionOralComboBox = self.windowAlta.findChild(QComboBox, 'comboBox_comoral')
        teaComboBox = self.windowAlta.findChild(QComboBox, 'comboBox_tea')
        diComboBox = self.windowAlta.findChild(QComboBox, 'comboBox_di')

        name = nameLine.text()
        age = ageSpinBox.value()
        gender = genderComboBox.currentText()
        comOral = 1 if comunicacionOralComboBox.currentIndex() == 0 else 0
        tea = 1 if teaComboBox.currentIndex() == 0 else 0
        di = 1 if diComboBox.currentIndex() == 0 else 0

        if self.comprobarDatos():
            child = (name, age, gender, tea, di, comOral)
            print(child)
            darAlta(child)
            self.listadoAltasClass.actualizarDatosTabla()
            self.windowAlta.close()
        else:
            print("No datos")
            self.windowAlta.close()