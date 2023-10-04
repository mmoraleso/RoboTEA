import os
import sys
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QFile, QIODevice, QSize, QRect, Qt
from PySide2.QtGui import QFont, QPixmap, QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

from CrearEditarHistoriaPregunta import CrearEditarHistoriaPregunta
from db.queries import getAll, deleteById, getAllPreguntas, deletePreguntasById
from editarAlta import EditarAlta

class ListadoHistoriasPreguntas(QWidget):
    def __init__(self, accionSeleccionada):
        QWidget.__init__(self, parent=None)
        self.accionSeleccionada = accionSeleccionada
        self.botonEditarPulsado = False
        self.crearDataButton = 0
        self.setupUi(self)
        self.tabla = self.windowListaH.findChild(QTableWidget, 'tableWidget')
        self.cargarDatosTable()
        self.setWindowFlag(Qt.Window)
        self.formVisible = False
        self.crearDataButton.clicked.connect(self.crearNuevaHP)

    def crearNuevaHP(self):
        if self.accionSeleccionada == 'P':
            self.editarDatosWindow = CrearEditarHistoriaPregunta('C', 'P','', '', '', self)
        else:
            self.editarDatosWindow = CrearEditarHistoriaPregunta('C', 'H', '', '', '', self)
        if self.editarDatosWindow.isVisible():
            self.editarDatosWindow.hide()
        else:
            self.editarDatosWindow.show()
        # self.actualizarDatosTabla()

    def show(self):
        self.windowListaH.show()
        self.formVisible = True

    def hide(self):
        self.windowListaH.hide()
        self.formVisible = False

    def isVisible(self):
        return self.formVisible

    def setupUi(self, DarAlta):
        if self.accionSeleccionada == 'P':
            nombre_ui = "./interfaz/ListadoPreguntas.ui"
        else:
            nombre_ui = "./interfaz/ListadoHistorias.ui"
        ui_fileListado = QFile(nombre_ui)
        if not ui_fileListado.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(nombre_ui, ui_fileListado.errorString()))
            sys.exit(-1)
        loaderAlta = QUiLoader()
        self.windowListaH = loaderAlta.load(ui_fileListado)
        ui_fileListado.close()

        if self.accionSeleccionada == 'P':
            self.crearDataButton = self.windowListaH.findChild(QPushButton, 'addPregunta_Button')
        else:
            self.crearDataButton = self.windowListaH.findChild(QPushButton, 'addHistoria_Button')
        if not self.windowListaH:
            print(self.windowListaH.errorString())
            sys.exit(-1)

    def pulsarEditar(self):
        filaPulsada = self.tabla.currentRow()
        if self.accionSeleccionada == 'P':
            id = self.tabla.item(filaPulsada, 0).text()
            titulo = self.tabla.item(filaPulsada, 1).text()
            contenido = self.tabla.item(filaPulsada, 2).text()
            self.editarDatosWindow = CrearEditarHistoriaPregunta('E', 'P',id, contenido, titulo, self)
        else:
            titulo = self.tabla.item(filaPulsada, 0).text()
            contenido = self.tabla.item(filaPulsada, 1).text()
            self.editarDatosWindow = CrearEditarHistoriaPregunta('E', 'H', titulo, contenido, '', self)
        if self.editarDatosWindow.isVisible():
            self.editarDatosWindow.hide()
        else:
            self.editarDatosWindow.show()
        self.actualizarDatosTabla()


    def pulsarEliminar(self):
        print("Eliminar")
        filaPulsada = self.tabla.currentRow()
        if self.accionSeleccionada == 'P':
            id = self.tabla.item(filaPulsada, 0).text()
            idNum = int(id)
            print("Id row pulsada " + str(id))
            deletePreguntasById(idNum)
        else:
            nombre=self.tabla.item(filaPulsada, 0).text()+".txt"
            os.remove("historias/" + nombre)
        self.actualizarDatosTabla()

    def actualizarDatosTabla(self):
        datos = []
        if self.accionSeleccionada == 'P':
            columnas = ["Id", "Título", "Pregunta", "Editar Pregunta", "Eliminar"]
            datos = getAllPreguntas()
        else:
            columnas = ["Título", "Historia", "Editar Pregunta", "Eliminar"]
            listadoActividades,textoActividades = self.cargarDatosHistorias()
            for (i, fila) in enumerate(listadoActividades):
                obj_aux = [listadoActividades[i],textoActividades[i]]
                datos.append(obj_aux)
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
                self.tabla.setItem(i, j, QTableWidgetItem(str(columna).replace("\\n", "\r\n").replace(",", "")\
                .replace("'", "").replace("[", "").replace("]", "")))
                item = self.tabla.item(i, j)
                item.setTextAlignment(QtCore.Qt.AlignCenter)

    def cargarDatosTable(self):
        if self.accionSeleccionada == 'P':
            columnas = ["Id", "Título", "Pregunta", "Editar Pregunta", "Eliminar"]
        else:
            columnas = ["Título", "Historia", "Editar Pregunta", "Eliminar"]
        self.tabla.setColumnCount(len(columnas))
        self.tabla.setHorizontalHeaderLabels(columnas)
        self.tabla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tabla.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        font = QFont("Arial", 14, QFont.Bold)
        self.tabla.horizontalHeader().setFont(font)
        self.tabla.verticalHeader().setVisible(False)

        self.actualizarDatosTabla()

    def cargarDatosHistorias(self):
        historiasUrl = os.getcwd() + '/historias'
        directorioHistorias = os.listdir(historiasUrl)
        listadoActividades = []
        textoActividades = []
        for fichero in directorioHistorias:
            if os.path.isfile(os.path.join(historiasUrl, fichero)) and fichero.endswith('.txt'):
                listadoActividades.append(fichero[:-4])
                listadoLineas = open("historias/"+fichero).readlines()
                textoActividades.append(listadoLineas)
        return listadoActividades,textoActividades
