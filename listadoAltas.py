import sys

from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QFile, QIODevice, Qt
from PySide2.QtGui import QFont
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

from darAlta import DarAltaClass
from db.queries import getAll, deleteById
from editarAlta import EditarAlta


class ListadoAltas(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=None)
        self.crearChildButton = None
        self.botonEditarPulsado = False
        self.setupUi(self)
        self.tabla = self.windowLista.findChild(QTableWidget, 'tableWidget')
        self.cargarDatosTable()
        self.setWindowFlag(Qt.Window)
        self.formVisible = False
        self.crearChildButton.clicked.connect(self.pulsarCrearChild)

    def clickAceptar(self):
        self.guardarDatos()

    def show(self):
        self.windowLista.show()
        self.formVisible = True

    def hide(self):
        self.windowLista.hide()
        self.formVisible = False

    def isVisible(self):
        return self.formVisible

    def setupUi(self, DarAlta):
        nombre_ui = "./interfaz/Listado.ui"
        ui_fileListado = QFile(nombre_ui)
        if not ui_fileListado.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(nombre_ui, ui_fileListado.errorString()))
            sys.exit(-1)
        loaderAlta = QUiLoader()
        self.windowLista = loaderAlta.load(ui_fileListado)
        ui_fileListado.close()

        self.crearChildButton = self.windowLista.findChild(QPushButton, 'addNino_Button')
        if not self.windowLista:
            print(self.windowLista.errorString())
            sys.exit(-1)

    def pulsarEditar(self):
        filaPulsada = self.tabla.currentRow()
        id = self.tabla.item(filaPulsada, 0).text()
        self.editarDatosWindow = EditarAlta(id, self)
        if self.editarDatosWindow.isVisible():
            self.editarDatosWindow.hide()
        else:
            self.editarDatosWindow.show()

    def pulsarCrearChild(self):
        self.crearChildWindow = DarAltaClass(self)
        if self.crearChildWindow.isVisible():
            self.crearChildWindow.hide()
        else:
            self.crearChildWindow.show()


    def pulsarEliminar(self):
        print("Eliminar")
        filaPulsada = self.tabla.currentRow()
        id = self.tabla.item(filaPulsada, 0).text()
        idNum = int(id)
        print("Id row pulsada " + str(id))
        deleteById(idNum)
        self.actualizarDatosTabla()

    def actualizarDatosTabla(self):
        columnas = ["Id", "Nombre", "Edad", "Genero", "Padece TEA", "Padece DI", "C. Oral", "Editar Datos", "Eliminar"]
        datos = getAll()
        self.tabla.setRowCount(len(datos))
        for (i, fila) in enumerate(datos):
            editButton = QPushButton("Editar", self)
            columnafinal = len(columnas)
            self.tabla.setCellWidget(i, columnafinal - 2, editButton)
            editButton.clicked.connect(self.pulsarEditar)
            deleteButton = QPushButton("Eliminar", self)
            self.tabla.setCellWidget(i, columnafinal - 1, deleteButton)
            deleteButton.clicked.connect(self.pulsarEliminar)

            for (j, columna) in enumerate(fila):
                if j > 3 and columna == 1:
                    columna = 'Sí'
                elif j > 3 and columna == 0:
                    columna = 'No'

                self.tabla.setItem(i, j, QTableWidgetItem(str(columna)))
                item = self.tabla.item(i, j)
                item.setTextAlignment(QtCore.Qt.AlignCenter)

    def cargarDatosTable(self):
        columnas = ["Id", "Nombre", "Edad", "Genero", "Padece TEA", "Padece DI", "C. Oral", "Editar Datos", "Eliminar"]
        self.tabla.setColumnCount(len(columnas))
        self.tabla.setHorizontalHeaderLabels(columnas)
        self.tabla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tabla.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        font = QFont("Arial", 14, QFont.Bold)
        self.tabla.horizontalHeader().setFont(font)
        self.tabla.verticalHeader().setVisible(False)

        self.actualizarDatosTabla()
