from __future__ import print_function, absolute_import

import os
import sys
import traceback

from PySide2 import QtWidgets
from PySide2.QtCore import QFile, QIODevice, QSize, Qt
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

from db.queries import getPreguntaById

sys.path.insert(0, os.path.join(os.getenv('HOME'), ".learnblock", "clients"))
from learnblock.Cozmo import Robot
import sys

class SesionEnCurso(QWidget):
    def __init__(self, datosSesion, windowOpciones):
        QWidget.__init__(self)
        self.windowOpciones = windowOpciones
        self.setWindowTitle("Sesion En Curso")
        # self.windowOpciones.close()
        # self.pantallaDeCarga = PantallaDeCarga()
        # self.mostrarPantallas()
        self.setupUiSesionEnCurso(self)
        self.setWindowFlag(Qt.Window)
        self.definirIconoBotones()
        self.formVisible = False
        self.estado = 0
        self.pausado = True
        self.detenido = True
        self.botonPausar.clicked.connect(self.pausar)
        self.botonReanudar.clicked.connect(self.reanudar)
        self.botonSituacion.clicked.connect(self.contarSituacion)
        self.botonEmociones.clicked.connect(self.comprobarEmociones)
        self.botonPregunta.clicked.connect(self.cozmoPregunta)
        self.botonPremio.clicked.connect(self.darRecompensa)
        self.botonDetener.clicked.connect(self.detener)
        self.barraVolumen.valueChanged.connect(self.cambiarVolumen)
        self.lineasFichero = {}; #listado con las lineas del fichero de situación
        self.lineasSinDecir = {}; #listado de lineas que todavía no se han dicho
        self.datosSesion = datosSesion
        self.historia = datosSesion[0]
        self.pregunta = datosSesion[1]
        self.emocion = datosSesion[2]
        self.idAprilTagEmocion = datosSesion[4]
        self.app = QtWidgets.QApplication.instance()
        self.robot = 0
        self.usedFunctions = ['say_Text', 'get_image', 'cozmoDances', 'expressSadness', 'express', 'cozmoIdle']
        self.instanciarCozmo()
        self.windowOpciones.close()
        self.setVolumenInicial()
        self.mostrarPantallas()
        self.emocionCorrecta = False


    def mostrarPantallas(self):
        if self.isVisibleSesion():
            self.hideSesion()
        else:
            self.showSesion()

    def showSesion(self):
        self.windowSesion.show()
        self.formVisible = True

    def hideSesion(self):
        self.windowSesion.hide()
        self.formVisible = False

    def isVisibleSesion(self):
        return self.formVisible

    def setupUiSesionEnCurso(self, DarAlta):

        ui_file_name2 = "./interfaz/SesionEnCurso2.ui"
        ui_fileSesionCurso = QFile(ui_file_name2)

        if not ui_fileSesionCurso.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(ui_file_name2, ui_fileSesionCurso.errorString()))
            sys.exit(-1)

        loaderAlta = QUiLoader()
        self.windowSesion = loaderAlta.load(ui_fileSesionCurso)
        ui_fileSesionCurso.close()

        if not self.windowSesion:
            print(self.windowSesion.errorString())
            sys.exit(-1)

        self.setWindowTitle("Sesión En Curso")
        self.botonReanudar = self.windowSesion.findChild(QPushButton, 'botonReanudar')
        self.botonPausar = self.windowSesion.findChild(QPushButton, 'botonPausar')
        self.botonSituacion = self.windowSesion.findChild(QPushButton, 'botonSituacion')
        self.botonEmociones = self.windowSesion.findChild(QPushButton, 'botonEmociones')
        self.botonPregunta = self.windowSesion.findChild(QPushButton, 'botonPregunta')
        self.botonPremio = self.windowSesion.findChild(QPushButton, 'botonPremio')
        self.botonDetener = self.windowSesion.findChild(QPushButton, 'botonDetener')
        self.barraVolumen = self.windowSesion.findChild(QSlider, 'barraVolumen')

    def definirIconoBotones(self):
        # imagen boton Contar Sitacion
        iconoSituacion = QIcon()
        iconoSituacion.addFile("./interfaz/iconos/botonVolumen.png", QSize(), QIcon.Normal, QIcon.Off)
        self.botonSituacion.setIcon(iconoSituacion)

        # imagen boton Comprobar Emociones
        iconoEmociones = QIcon()
        iconoEmociones.addFile("./interfaz/iconos/emocionesBoton.png", QSize(), QIcon.Normal, QIcon.Off)
        self.botonEmociones.setIcon(iconoEmociones)

        # imagen boton Cozmo Pregunta
        iconoPregunta = QIcon()
        iconoPregunta.addFile("./interfaz/iconos/preguntaicono.png", QSize(), QIcon.Normal, QIcon.Off)
        self.botonPregunta.setIcon(iconoPregunta)

        # imagen boton Dar Recompensa
        iconoPremio = QIcon()
        iconoPremio.addFile("./interfaz/iconos/premioicono.png", QSize(), QIcon.Normal, QIcon.Off)
        self.botonPremio.setIcon(iconoPremio)

        # imagen boton Reanudar
        iconoReanudar = QIcon()
        iconoReanudar.addFile("./interfaz/iconos/boton-de-play.png", QSize(), QIcon.Normal, QIcon.Off)
        self.botonReanudar.setIcon(iconoReanudar)

        # imagen boton Pausar
        iconoPausar = QIcon()
        iconoPausar.addFile("./interfaz/iconos/boton-de-pausa.png", QSize(), QIcon.Normal, QIcon.Off)
        self.botonPausar.setIcon(iconoPausar)

        #imagen boton Detener
        iconoDetener = QIcon()
        iconoDetener.addFile("./interfaz/iconos/boton-detener.png", QSize(), QIcon.Normal, QIcon.Off)
        self.botonDetener.setIcon(iconoDetener)

        #Valores barra volumen
        self.barraVolumen.setMinimum(0)
        self.barraVolumen.setMaximum(100)
        self.barraVolumen.setTickInterval(1)


    def cambiarEstado(self):
        print("estado " + str(self.estado))
        if self.pausado == False and self.detenido == False:
            if self.estado == 0:
                self.contarSituacion()
            if self.estado == 1:
                self.comprobarEmociones()
            if self.estado == 2:
                self.cozmoPregunta()
            if self.estado == 3:
                self.darRecompensa()

    def detener(self):
        print("Deteniendo la sesión")
        self.detenido = True
        self.lineasSinDecir = {}
        print("Pausado " + str(self.pausado) + " Detenido: " + str(self.detenido))
        self.app.processEvents()

    def reanudar(self):
        print("Reanudando la sesión")
        self.pausado = False
        self.detenido = False
        self.app.processEvents()
        self.cambiarEstado()


    def pausar(self):
        print("Pausando la sesión")
        self.pausado = True
        self.detenido = False
        print("Pausado " + str(self.pausado) + " Detenido: " + str(self.detenido))
        self.app.processEvents()

    def instanciarCozmo(self):
        print(" -- Conexión con Cozmo --")
        try:
            self.robot = Robot(availableFunctions=self.usedFunctions)
        except Exception as e:
            print("Problems creating a robot instance")
            traceback.print_exc()
            raise (e)

    def contarSituacion(self):
        print("Contado situación")
        self.leerSituacion(self.historia)

        if self.pausado == False:
            self.estado = 0
            self.estado += 1
            self.cambiarEstado()

    def comprobarEmociones(self):
        print("Comprobar emociones")
        self.lineasSinDecir = {}
        self.capturarApriltag()
        if self.pausado == False:
            self.estado = 1
            self.estado += 1
            self.cambiarEstado()

    def cozmoPregunta(self):
        self.estado = 2
        print("Cozmo pregunta")
        self.lineasSinDecir = {}
        # obtener cuerpo pregunta
        cuerpoPregunta = getPreguntaById(self.pregunta)[0]
        self.app.processEvents()
        self.robot.say_Text(cuerpoPregunta.replace("{nombreNiño}", self.datosSesion[3]))
        self.robot.cozmo.wait_for_all_actions_completed()
        print(cuerpoPregunta.replace("{nombreNiño}", self.datosSesion[3]))
        if self.pausado == False:
            self.estado += 1
            self.cambiarEstado()

    def darRecompensa(self):
        self.lineasSinDecir = {}
        print("Dando recompensa")
        if self.emocionCorrecta:
            print("EMocion correcta")
            print("baila:")

            self.robot.doWInDance()
        else:
            print("sadness:")
            self.robot.sendBehaviour("unhappy")

        if self.pausado == False:
            self.estado = 3
            self.estado += 1
            self.cambiarEstado()

    def setVolumenInicial(self):
        self.robot.cozmo.set_robot_volume(0.75)
        self.barraVolumen.setValue(75)

    def cambiarVolumen(self):
        print("Cambiando volumen cozmo: " + str(self.barraVolumen.value()))
        self.robot.cozmo.set_robot_volume(self.barraVolumen.value()/100)
        self.app.processEvents()

    def leerSituacion(self, situacion):
        print("Leyendo situacion: " + situacion)
        fichero = open("historias/"+situacion+'.txt')

        if not self.lineasSinDecir:
            self.lineasFichero = fichero.readlines()
            self.lineasSinDecir = self.lineasFichero.copy()
        print("Empieza la situación")
        while not self.pausado and self.lineasSinDecir and not self.detenido:
            print("Pausado " + str(self.pausado) + " Detenido: " + str(self.detenido))

            try:
                self.app.processEvents()
                self.robot.say_Text(self.lineasSinDecir[0].replace("{nombreNiño}", self.datosSesion[3]))
                self.robot.cozmo.wait_for_all_actions_completed()
                print(self.lineasSinDecir[0].replace("{nombreNiño}", self.datosSesion[3]))

                # Una vez dice la frase podemos borrarla del fichero de lineas sin decir
                self.app.processEvents()
                self.lineasSinDecir.pop(0)
            except KeyError:
                print("Hay un error contando la situación")

        print("Cozmo ha terminado de contar la situación.")
        self.pausado = True

    def capturarApriltag(self):
        apriltagImagen = self.robot.getAprilTagId()
        print("Apriltag de la imagen: " + str(apriltagImagen))
        if apriltagImagen == self.idAprilTagEmocion:
            self.emocionCorrecta = True
        else:
            self.emocionCorrecta = False

#TODO: Nuevo método de evaluación
#TODO: Cambiar como habla Cozmo