from __future__ import print_function, absolute_import

import os
import sys
import time
import traceback
from datetime import datetime

import pycozmo
import pyttsx3
from PySide2 import QtWidgets
from PySide2.QtCore import QFile, QIODevice, QSize, Qt
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtWidgets import QGraphicsView
from qtpy import QtCore

from db.queries import getPreguntaById, getHistoriasById, darAltaSesion

sys.path.insert(0, os.path.join(os.getenv('HOME'), ".learnblock", "clients"))
from learnblock.Cozmo import Robot
import sys

class SesionEnCurso(QWidget):
    def __init__(self, datosSesion, windowOpciones):
        QWidget.__init__(self)
        self.windowOpciones = windowOpciones
        self.setWindowTitle("Sesion En Curso")
        self.setupUiSesionEnCurso(self)
        self.setWindowFlag(Qt.Window)
        self.definirIconoBotones()
        self.formVisible = False
        self.estado = 0
        self.pausado = True
        self.detenido = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.mostrarCam)
        self.botonPausar.clicked.connect(self.pausar)
        self.botonReanudar.clicked.connect(self.reanudar)
        self.botonSituacion.clicked.connect(self.contarSituacion)
        self.botonEmociones.clicked.connect(self.comprobarEmociones)
        self.botonPregunta.clicked.connect(self.cozmoPregunta)
        self.botonPremio.clicked.connect(self.darRecompensa)
        self.botonDetener.clicked.connect(self.detener)
        self.botonCamara.clicked.connect(self.infoCam)
        self.botonEvaluacion.clicked.connect(self.evaluarSesion)
        self.barraVolumen.valueChanged.connect(self.cambiarVolumen)
        self.lineasFichero = {}; #listado con las lineas del fichero de situación
        self.lineasSinDecir = {}; #listado de lineas que todavía no se han dicho
        self.datosSesion = datosSesion
        self.historia = datosSesion[0]
        self.pregunta = datosSesion[1]
        self.emocion = datosSesion[2]
        self.idNiño = datosSesion[5]
        self.idAprilTagEmocion = datosSesion[4]
        self.app = QtWidgets.QApplication.instance()
        self.robot = 0
        self.usedFunctions = ['say_Text', 'get_image', 'cozmoDances', 'expressSadness', 'express', 'cozmoIdle']
        self.instanciarCozmo()
        self.windowOpciones.close()
        self.setVolumenInicial()
        self.mostrarPantallas()
        self.emocionCorrecta = False
        self.audioSpeaker = None
        self.camaraEncendida = False
        angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 4.0
        self.robot.cozmo.set_head_angle(angle)
        time.sleep(1)
        self.imagenApril = None

    def mostrarPantallas(self):
        if self.isVisibleSesion():
            self.hideSesion()
        else:
            self.showSesion()

    def showSesion(self):
        self.windowSesion.show()
        self.mostrarCamApagada()
        self.formVisible = True

    def hideSesion(self):
        self.windowSesion.hide()
        self.formVisible = False

    def isVisibleSesion(self):
        return self.formVisible

    def setupUiSesionEnCurso(self, DarAlta):

        ui_file_name2 = "./interfaz/SesionEnCurso3.ui"
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
        self.botonEvaluacion = self.windowSesion.findChild(QPushButton, 'botonEvaluacion')
        self.botonCamara = self.windowSesion.findChild(QPushButton, 'botonCamara')
        self.barraVolumen = self.windowSesion.findChild(QSlider, 'barraVolumen')
        self.camCozmoView = self.windowSesion.findChild(QGraphicsView, 'camGraphicsView')

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

        #imagen boton Detener
        iconoEvaluacion = QIcon()
        iconoEvaluacion.addFile("./interfaz/iconos/puntuaciones.png", QSize(), QIcon.Normal, QIcon.Off)
        self.botonEvaluacion.setIcon(iconoEvaluacion)

        #imagen boton camara
        iconoCamara = QIcon()
        iconoCamara.addFile("./interfaz/iconos/botonCamara.png", QSize(), QIcon.Normal, QIcon.Off)
        self.botonCamara.setIcon(iconoCamara)

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
                self.cozmoPregunta()
            if self.estado == 2:
                self.comprobarEmociones()
            if self.estado == 3:
                self.darRecompensa()
            if self.estado == 4:
                self.evaluarSesion()

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
        self.estado = 0
        print("Contado situación")
        self.mostrarCamApagada()
        self.leerSituacion(self.historia)

        if self.pausado == False:
            self.estado = 1
            self.cambiarEstado()

    def comprobarEmociones(self):
        self.estado = 2
        self.mostrarCamApagada()
        print("Comprobar emociones")
        self.lineasSinDecir = {}
        self.capturarApriltag()
        if self.pausado == False:
            self.estado = 3
            self.cambiarEstado()

    def cozmoPregunta(self):
        self.estado = 1
        self.mostrarCamApagada()
        print("Cozmo pregunta")
        self.lineasSinDecir = {}
        # obtener cuerpo pregunta
        cuerpoPregunta = getPreguntaById(self.pregunta)[0]
        self.app.processEvents()
        self.instanciarAudio()
        self.audioSpeaker.save_to_file(cuerpoPregunta.replace("{nombreNiño}", self.datosSesion[3]),
                                       'pregunta.wav')
        self.audioSpeaker.runAndWait()
        time.sleep(1)
        self.robot.cozmo.play_audio('pregunta.wav')
        print(cuerpoPregunta.replace("{nombreNiño}", self.datosSesion[3]))
        if self.pausado == False:
            self.estado = 2
            self.cambiarEstado()

    def darRecompensa(self):
        self.mostrarCamApagada()
        self.estado = 3
        self.lineasSinDecir = {}
        print("Dando recompensa")
        if self.imagenApril != None:
            if self.emocionCorrecta:
                self.robot.doWInDance(True)
            else:
                self.robot.doWInDance(False)
            if self.pausado == False:
                self.estado = 4
                self.cambiarEstado()

    def evaluarSesion(self):
        self.mostrarCamApagada()
        print("Evaluando Sesion")
        self.evaluacionNiño = None
        self.evaluacionTerapeuta = None
        angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
        self.robot.cozmo.set_head_angle(angle)
        time.sleep(1)

        # Comienzo evaluacion
        self.instanciarAudio()
        self.audioSpeaker.save_to_file("Para finalizar, es hora de evaluar la sesión",
                                       'inicioEvaluacion.wav')
        self.audioSpeaker.runAndWait()
        time.sleep(1)
        self.robot.speakText('inicioEvaluacion.wav')
        os.remove('inicioEvaluacion.wav')

        # Evaluación niño
        self.instanciarAudio()
        self.audioSpeaker.save_to_file("{nombreNiño}, ¿te ha gustado la sesión? Muéstrame cuanto del uno al diez".replace("{nombreNiño}", self.datosSesion[3]),
                                       'evaluacionUsuario.wav')
        self.audioSpeaker.runAndWait()
        time.sleep(1)
        self.robot.speakText('evaluacionUsuario.wav')
        while self.evaluacionNiño == None:
            self.evaluacionNiño = self.robot.getAprilTagId()
        print("Apriltag de la evaluacion del niño: " + str(self.evaluacionNiño))
        os.remove('evaluacionUsuario.wav')
        self.instanciarAudio()
        self.audioSpeaker.save_to_file("Listo",
                                       'listo.wav')
        self.audioSpeaker.runAndWait()
        time.sleep(1)
        self.robot.speakText('listo.wav')

        # Evaluación terapeuta
        self.instanciarAudio()
        self.audioSpeaker.save_to_file("Terapeuta, cuanto ha ayudado a {nombreNiño}".replace("{nombreNiño}", self.datosSesion[3]),
                                       'evaluacionTerapeuta.wav')
        self.audioSpeaker.runAndWait()
        time.sleep(1)
        self.robot.speakText('evaluacionTerapeuta.wav')
        while self.evaluacionTerapeuta == None:
            self.evaluacionTerapeuta = self.robot.getAprilTagId()
        print("Apriltag de la evaluacion del terapeuta " + str(self.evaluacionTerapeuta))
        os.remove('evaluacionTerapeuta.wav')
        self.robot.speakText('listo.wav')
        os.remove('listo.wav')

        print("Guardando Info sesion")
        if self.evaluacionNiño != None and self.evaluacionTerapeuta != None:
            datosSesionAGuardar = (self.historia, self.idNiño, self.pregunta, self.emocion, self.evaluacionNiño, self.evaluacionTerapeuta, self.emocionCorrecta, datetime.now())
            darAltaSesion(datosSesionAGuardar)
        self.estado = 0
        self.detenido = 1
        self.pausado = 1
        if self.pausado == False:
            self.cambiarEstado()

    def setVolumenInicial(self):
        self.robot.cozmo.set_volume(50000)

        # self.robot.cozmo.set_robot_volume(0.75)
        self.barraVolumen.setValue(75)

    def cambiarVolumen(self):

        print("Cambiando volumen cozmo: " + str(self.barraVolumen.value()))
        maxVolum = 65535
        self.robot.cozmo.set_volume((self.barraVolumen.value()*maxVolum) / 100)
        print("volumen: " + str((self.barraVolumen.value()*maxVolum) / 100))
        # self.robot.cozmo.set_robot_volume(self.barraVolumen.value()/100)
        self.app.processEvents()

    def leerSituacion(self, id):
        print("Leyendo situacion: " + str(id))
        fichero = getHistoriasById(id)

        if not self.lineasSinDecir:
            self.lineasFichero = fichero[0].split("\n")
            self.lineasSinDecir = self.lineasFichero.copy()
        print("Empieza la situación")

        while not self.pausado and self.lineasSinDecir and not self.detenido:

            try:
                self.app.processEvents()
                self.instanciarAudio()
                self.audioSpeaker.save_to_file(self.lineasSinDecir[0].replace("{nombreNiño}", self.datosSesion[3]), 'fraseHistoria.wav')
                self.audioSpeaker.runAndWait()
                time.sleep(1)
                self.robot.speakText('fraseHistoria.wav')
                print("Se terminó la frase")

                # Una vez dice la frase podemos borrarla del listado de lineas sin decir
                self.app.processEvents()
                self.lineasSinDecir.pop(0)
                os.remove('fraseHistoria.wav')
            except KeyError:
                print("Hay un error contando la situación")

        print("Cozmo ha terminado de contar la situación.")

    def capturarApriltag(self):
        angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
        self.robot.cozmo.set_head_angle(angle)
        apriltagImagen = None
        # self.robot.cozmo.wait_for_all_actions_completed()
        while apriltagImagen == None:
            apriltagImagen = self.robot.getAprilTagId()
        print("Apriltag de la imagen: " + str(apriltagImagen))
        self.imagenApril = apriltagImagen
        if apriltagImagen != None and apriltagImagen == self.idAprilTagEmocion:
            self.emocionCorrecta = True
        else:
            self.emocionCorrecta = False

    def closeEvent(self, event):
        self.cozmo.robot.disconnect()
        event.accept()  # let the window close

    def instanciarAudio(self):
        if self.audioSpeaker:
            del(self.audioSpeaker)
        self.audioSpeaker = pyttsx3.init()
        self.audioSpeaker.setProperty('rate', 200)
        self.audioSpeaker.setProperty('voice', 'spanish')  # voz lo más femenina posible

    def infoCam(self):
        if self.camaraEncendida:
            print("Apagar cam")
            self.mostrarCamApagada()
        else:
            print("Encender cam")
            self.camaraEncendida = True
            self.timer.start(100)

    def mostrarCamApagada(self):
        self.camaraEncendida = False
        self.timer.stop()
        print("Mostrar cam apagada")
        print("qgrapic size: " + str(self.camCozmoView.size()))
        pix = QPixmap("camaraApagada.png")
        pix.scaled(320, 190)
        item = QGraphicsPixmapItem(pix)
        scene = QtWidgets.QGraphicsScene()
        scene.addItem(item)
        self.camCozmoView.setScene(scene)
        print("Just set scene")

    def mostrarCam(self):
        print("Mostrar cam")
        self.robot.getImageForVideo()
        pix = QPixmap("cam.png")
        pix.scaled(329,198)
        item = QGraphicsPixmapItem(pix)
        scene = QtWidgets.QGraphicsScene()
        scene.addItem(item)
        self.camCozmoView.setScene(scene)
        print("Just set scene")
