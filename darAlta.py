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
        genderComboBox.addItems(['Niño', 'Niña', 'No definido'])
        self.botonAceptar = self.windowAlta.findChild(QPushButton, 'aceptar_alta_button')

        print("Después del show")


        #windowCuestionarioAlta.activateWindow()

    def comprobarDatos(self):
        nameLine = self.windowAlta.findChild(QLineEdit, 'lineEdit')
        ageSpinBox = self.windowAlta.findChild(QSpinBox, 'spinBox')
        genderComboBox = self.windowAlta.findChild(QComboBox, 'comboBox')

        name = nameLine.text()
        age = ageSpinBox.value()
        gender = genderComboBox.currentText()

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
        nameLine = self.windowAlta.findChild(QLineEdit, 'lineEdit')
        ageSpinBox = self.windowAlta.findChild(QSpinBox, 'spinBox')
        genderComboBox = self.windowAlta.findChild(QComboBox, 'comboBox')

        name = nameLine.text()
        age = ageSpinBox.value()
        gender = genderComboBox.currentText()

        if self.comprobarDatos():
            child = (name, age, gender)
            print(child)
            darAlta(child)
            self.listadoAltasClass.actualizarDatosTabla()
            self.windowAlta.close()
        else:
            print("No datos")
            self.windowAlta.close()