from __future__ import print_function, absolute_import

import sys
from PySide2 import QtCore
from PySide2.QtCore import QFile, QIODevice, QSize, QRect, Qt
from PySide2.QtGui import QFont, QPixmap, QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from db.queries import darAlta, actualizarDatosNiños, getById, getAll

import sys, os, time, traceback
sys.path.insert(0, os.path.join(os.getenv('HOME'), ".learnblock", "clients"))
from learnblock.Cozmo import Robot
import signal
import sys


class SesionEnCurso(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowFlag(Qt.Window)
        self.definirIconoBotones()
        self.formVisible = False
        self.estado = 0
        self.pausado = True
        self.botonPausar.clicked.connect(self.pausar)
        self.botonReanudar.clicked.connect(self.reanudar)
        self.botonSituacion.clicked.connect(self.contarSituacion)
        self.botonEmociones.clicked.connect(self.comprobarEmociones)
        self.botonPregunta.clicked.connect(self.cozmoPregunta)
        self.botonPremio.clicked.connect(self.darRecompensa)

    def show(self):
        self.windowSesion.show()
        self.formVisible = True

    def hide(self):
        self.windowSesion.hide()
        self.formVisible = False

    def isVisible(self):
        return self.formVisible

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

    def cambiarEstado(self):
        print("estado " + str(self.estado))
        if self.pausado == False:
            if self.estado == 0:
                self.contarSituacion()
            if self.estado == 1:
                self.comprobarEmociones()
            if self.estado == 2:
                self.cozmoPregunta()
            if self.estado == 3:
                self.darRecompensa()

    def reanudar(self):
        self.pausado = False
        self.cambiarEstado()

    def pausar(self):
        self.pausado = True

    def setupUi(self, DarAlta):

        ui_file_name2 = "./interfaz/SesionEnCurso2.ui"
        ui_fileDarAlta = QFile(ui_file_name2)

        if not ui_fileDarAlta.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(ui_file_name2, ui_fileDarAlta.errorString()))
            sys.exit(-1)

        loaderAlta = QUiLoader()
        self.windowSesion = loaderAlta.load(ui_fileDarAlta)
        ui_fileDarAlta.close()

        if not self.windowSesion:
            print(self.windowSesion.errorString())
            sys.exit(-1)

        self.botonReanudar = self.windowSesion.findChild(QPushButton, 'botonReanudar')
        self.botonPausar = self.windowSesion.findChild(QPushButton, 'botonPausar')
        self.botonSituacion = self.windowSesion.findChild(QPushButton, 'botonSituacion')
        self.botonEmociones = self.windowSesion.findChild(QPushButton, 'botonEmociones')
        self.botonPregunta = self.windowSesion.findChild(QPushButton, 'botonPregunta')
        self.botonPremio = self.windowSesion.findChild(QPushButton, 'botonPremio')

    def contarSituacion(self):
        print("Contado situación")
        # Probar cozmo
        # TODO: CODIGO COZMO

        print(" -- Prueba de Cozmo --")
        usedFunctions = ['cozmoCat']
        #
        try:
            robot = Robot(availableFunctions=usedFunctions)
        except Exception as e:
            print("Problems creating a robot instance")
            traceback.print_exc()
            raise (e)

        time_global_start = time.time()

        def elapsedTime(umbral):
            global time_global_start
            time_global = time.time() - time_global_start
            return time_global > umbral

        def signal_handler(sig, frame):
            robot.stop()
            sys.exit(0)

        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        robot.cozmoCat()
        robot.stop()


        if self.pausado == False:
            self.estado = 0
            self.estado += 1
            self.cambiarEstado()

    def comprobarEmociones(self):
        print("Comprobar emociones")
        if self.pausado == False:
            self.estado = 1
            self.estado += 1
            self.cambiarEstado()

    def cozmoPregunta(self):
        self.estado = 2
        print("Cozmo pregunta")
        if self.pausado == False:
            self.estado += 1
            self.cambiarEstado()

    def darRecompensa(self):
        print("Dando recompensa")
        if self.pausado == False:
            self.estado = 3
            self.estado += 1
            self.cambiarEstado(

            )