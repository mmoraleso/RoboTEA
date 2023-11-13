import os
import sys

from PySide2.QtCore import QFile, QIODevice, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

from db.queries import actualizarPregunta, darAltaPregunta


class CrearEditarHistoriaPregunta(QWidget):
    def __init__(self, _accion, _tipoDato, _id, _contenido, _tituloPregunta, _listadoHistoriasPreguntasClass):
        QWidget.__init__(self)
        self.accion = _accion
        self.tipoDato = _tipoDato
        self.contenido = _contenido
        self.tituloPregunta = _tituloPregunta
        self.listadoHistoriasPreguntas = _listadoHistoriasPreguntasClass
        if self.accion == 'E':
            if self.tipoDato == 'P':
                print(str(self.accion) + " PRegunta")
                self.id = int(_id)
            else:
                print(str(self.accion) + " Historia")
                self.id = _id

        self.setupUi(self)
        self.mostrarDatosActuales()
        self.setWindowFlag(Qt.Window)
        self.formVisible = False
        self.botonAceptar.clicked.connect(self.guardarDatos)
        self.botonCancelar.clicked.connect(lambda : self.windowEditarHP.close())

    def clickAceptar(self):
        print("click aceptar")
        self.guardarDatos()

    def show(self):
        self.windowEditarHP.show()
        self.formVisible = True

    def hide(self):
        self.windowEditarHP.hide()
        self.formVisible = False

    def isVisible(self):
        return self.formVisible

    def setupUi(self, DarAlta):
        print("Entra en editarCrear")
        ui_file_name2 = "./interfaz/CrearHistoria.ui"
        ui_fileEditarHP = QFile(ui_file_name2)
        if not ui_fileEditarHP.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(ui_file_name2, ui_fileEditarHP.errorString()))
            sys.exit(-1)
        loaderAlta = QUiLoader()
        self.windowEditarHP = loaderAlta.load(ui_fileEditarHP)
        ui_fileEditarHP.close()
        if not self.windowEditarHP:
            print(self.windowEditarHP.errorString())
            sys.exit(-1)


    def mostrarDatosActuales(self):
        tituloWindow = self.windowEditarHP.findChild(QLabel, 'titulo')
        tituloHP = self.windowEditarHP.findChild(QLabel, 'tituloHP')
        contenidoHP = self.windowEditarHP.findChild(QLabel, 'contenidoHP')
        self.tituloTE = self.windowEditarHP.findChild(QTextEdit, 'tituloTextEdit')
        self.contenidoTE = self.windowEditarHP.findChild(QTextEdit, 'contenidoTextEdit')

        if self.accion == 'C':
            if (self.tipoDato == 'P'):
                tituloWindow.setText("Crear pregunta")
            else:
                tituloWindow.setText("Crear historia")
        else:
            if (self.tipoDato == 'P'):
                tituloWindow.setText("Editar pregunta")
                self.tituloTE.setPlainText(self.tituloPregunta)
                self.contenidoTE.setPlainText(self.contenido)
            else:
                tituloWindow.setText("Editar historia")
                self.tituloTE.setPlainText(self.id)
                self.contenidoTE.setPlainText(self.contenido)

        if (self.tipoDato == 'P'):
            tituloHP.setText("Titulo de la pregunta:")
            contenidoHP.setText("Pregunta:")
        else:
            tituloHP.setText("Titulo de la historia:")
            contenidoHP.setText("Historia a contar:")

        self.botonAceptar = self.windowEditarHP.findChild(QPushButton, 'aceptar_alta_button')
        self.botonCancelar = self.windowEditarHP.findChild(QPushButton, 'cancelar_alta_button')

    def comprobarDatos(self):
        titulo = self.tituloTE.toPlainText()
        contenido = self.contenidoTE.toPlainText()

        contadorVacios = 0

        if titulo == "":
            contadorVacios+=1
        if contenido == "":
            contadorVacios += 1

        resultado = True
        if contadorVacios > 0:
            resultado = False #Si hay fallos es false

        return resultado

    def guardarDatos(self):
        print("Se van a guardar datos")

        titulo = self.tituloTE.toPlainText()
        contenido = self.contenidoTE.toPlainText()

        if self.comprobarDatos():
            if self.accion == 'C':
                if (self.tipoDato == 'P'):
                    data = (titulo, contenido)
                    darAltaPregunta(data)
                else:
                    print(str("historias/" + titulo))
                    fichero = open("historias/" + str(titulo)+".txt", 'w')
                    fichero.writelines(contenido)
                    os.fsync(fichero.fileno())
                    fichero.close()
            else:
                if (self.tipoDato == 'P'):
                    data = (titulo, contenido)
                    actualizarPregunta(self.id, data)
                else:
                    os.remove("historias/" + self.id+".txt")
                    fichero = open("historias/"+str(titulo)+".txt", 'w')
                    fichero.writelines(contenido)
                    os.fsync(fichero.fileno())
                    fichero.close()
            self.windowEditarHP.hide()
            self.windowEditarHP.close()
            self.listadoHistoriasPreguntas.actualizarDatosTabla()

        else:
            print("No datos")