import sys

from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QFile, QIODevice, Qt
from PySide2.QtGui import QFont
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

from CrearEmocion import CrearEmocion
from EditarEmocion import EditarEmocion
from db.queries import getAllEmociones, deleteEmocionesById


class ListadoEmociones(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=None)
        self.crearEmocionesButton = None
        self.botonEditarPulsado = False
        self.setupUi(self)
        self.tabla = self.windowListaEmocion.findChild(QTableWidget, 'tableWidget')
        self.cargarDatosTable()
        self.setWindowFlag(Qt.Window)
        self.formVisible = False
        self.crearEmocionesButton.clicked.connect(self.pulsarCrearEmocion)

    def clickAceptar(self):
        self.guardarDatos()

    def show(self):
        self.windowListaEmocion.show()
        self.formVisible = True

    def hide(self):
        self.windowListaEmocion.hide()
        self.formVisible = False

    def isVisible(self):
        return self.formVisible

    def setupUi(self, DarAlta):
        nombre_ui = "./interfaz/ListadoEmociones.ui"
        ui_fileListado = QFile(nombre_ui)
        if not ui_fileListado.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(nombre_ui, ui_fileListado.errorString()))
            sys.exit(-1)
        loaderAlta = QUiLoader()
        self.windowListaEmocion = loaderAlta.load(ui_fileListado)
        ui_fileListado.close()

        self.crearEmocionesButton = self.windowListaEmocion.findChild(QPushButton, 'add_Button')
        if not self.windowListaEmocion:
            print(self.windowListaEmocion.errorString())
            sys.exit(-1)

    def pulsarEditar(self):
        filaPulsada = self.tabla.currentRow()
        id = self.tabla.item(filaPulsada, 0).text()
        self.editarDatosWindow = EditarEmocion(id, self)
        if self.editarDatosWindow.isVisible():
            self.editarDatosWindow.hide()
        else:
            self.editarDatosWindow.show()

    def pulsarCrearEmocion(self):
        self.crearChildWindow = CrearEmocion(self)
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
        deleteEmocionesById(idNum)
        self.actualizarDatosTabla()

    def actualizarDatosTabla(self):
        print("Actualizando tabla de emociones")
        columnas = ["Id", "Emoción", "AprilTag Asignado",  "Editar Datos", "Eliminar"]
        datos = getAllEmociones()
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
                self.tabla.setItem(i, j, QTableWidgetItem(str(columna)))
                item = self.tabla.item(i, j)
                item.setTextAlignment(QtCore.Qt.AlignCenter)

    def cargarDatosTable(self):
        columnas = ["Id", "Emoción", "AprilTag Asignado", "Editar Datos", "Eliminar"]
        self.tabla.setColumnCount(len(columnas))
        # self.tabla.horizontalHeaders().setSectionResizeMode(
        #     2, QtWidgets.QHeaderView.Stretch)
        # self.tabla.setColumnWidth(4, 10)
        # self.tabla.setColumnWidth(3, 10)
        self.tabla.setHorizontalHeaderLabels(columnas)
        self.tabla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tabla.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        font = QFont("Arial", 14, QFont.Bold)
        self.tabla.horizontalHeader().setFont(font)
        self.tabla.verticalHeader().setVisible(False)

        self.actualizarDatosTabla()
