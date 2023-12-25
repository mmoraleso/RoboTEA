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
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from cozmo.util import degrees

from db.queries import getPreguntaById, getHistoriasById, darAltaSesion

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
        self.botonEvaluacion = self.windowSesion.findChild(QPushButton, 'botonEvaluacion')
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

        #imagen boton Detener
        iconoEvaluacion = QIcon()
        iconoEvaluacion.addFile("./interfaz/iconos/puntuaciones.png", QSize(), QIcon.Normal, QIcon.Off)
        self.botonEvaluacion.setIcon(iconoEvaluacion)

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
        print("Contado situación")
        self.leerSituacion(self.historia)

        self.estado = 0
        self.estado += 1
        if self.pausado == False:
            self.cambiarEstado()

    def comprobarEmociones(self):
        print("Comprobar emociones")
        self.lineasSinDecir = {}
        self.capturarApriltag()
        # self.estado = 1
        self.estado += 1
        if self.pausado == False:
            self.cambiarEstado()

    def cozmoPregunta(self):
        # self.estado = 2
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
        self.estado += 1
        if self.pausado == False:
            self.cambiarEstado()

    def darRecompensa(self):
        self.lineasSinDecir = {}
        print("Dando recompensa")
        if self.imagenApril != None:
            if self.emocionCorrecta:
                print("EMocion correcta")
                print("baila:")

                self.robot.doWInDance()
            else:
                print("sadness:")
                self.robot.sendBehaviour("unhappy")

            self.estado = 3
            self.estado += 1
            if self.pausado == False:
                self.cambiarEstado()

    def evaluarSesion(self):
        print("Evaluando Sesion")
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
        self.evaluacionNiño = self.robot.getAprilTagId()
        print("Apriltag de la evaluacion del niño: " + str(self.evaluacionNiño))
        os.remove('evaluacionUsuario.wav')

        # Evaluación terapeuta
        self.instanciarAudio()
        self.audioSpeaker.save_to_file("Ahora los mayores, ¿Crees que esta sesión a ayudado a {nombreNiño}? Muestrame cuanto del uno al diez".replace("{nombreNiño}", self.datosSesion[3]),
                                       'evaluacionTerapeuta.wav')
        self.audioSpeaker.runAndWait()
        time.sleep(1)
        self.robot.speakText('evaluacionTerapeuta.wav')
        self.evaluacionTerapeuta = self.robot.getAprilTagId()
        print("Apriltag de la evaluacion del terapeuta " + str(self.evaluacionTerapeuta))
        os.remove('evaluacionTerapeuta.wav')

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
            print("Pausado " + str(self.pausado) + " Detenido: " + str(self.detenido))

            try:
                print("Diciendo la linea: "+ self.lineasSinDecir[0].replace("{nombreNiño}", self.datosSesion[3]))
                self.app.processEvents()
                self.instanciarAudio()
                self.audioSpeaker.save_to_file(self.lineasSinDecir[0].replace("{nombreNiño}", self.datosSesion[3]), 'fraseHistoria.wav')
                self.audioSpeaker.runAndWait()
                print("despues del run y antes del speak text")
                time.sleep(1)
                self.robot.speakText('fraseHistoria.wav')
                # self.robot.cozmo.wait_for(pycozmo.event.EvtAudioCompleted)
                # self.robot.deviceSendTextHuman(self.lineasSinDecir[0].replace("{nombreNiño}", self.datosSesion[3]))
                # self.robot.cozmo.wait_for_all_actions_completed()
                print("Se terminó la frase")

                # Una vez dice la frase podemos borrarla del fichero de lineas sin decir
                self.app.processEvents()
                self.lineasSinDecir.pop(0)
                os.remove('fraseHistoria.wav')
            except KeyError:
                print("Hay un error contando la situación")

        print("Cozmo ha terminado de contar la situación.")
        # self.pausado = True

    def capturarApriltag(self):
        angle = (pycozmo.robot.MAX_HEAD_ANGLE.radians - pycozmo.robot.MIN_HEAD_ANGLE.radians) / 2.0
        self.robot.cozmo.set_head_angle(angle)
        # self.robot.cozmo.wait_for_all_actions_completed()
        apriltagImagen = self.robot.getAprilTagId()
        print("Apriltag de la imagen: " + str(apriltagImagen))
        self.imagenApril = apriltagImagen
        if apriltagImagen != None and apriltagImagen == self.idAprilTagEmocion:
            self.emocionCorrecta = True
        else:
            self.emocionCorrecta = False

#TODO: Nuevo método de evaluación
#TODO: Cambiar como habla Cozmo

    # def crearFrasesDefault(self):
    #     print("Creando frases default.")
    #     self.audioSpeaker.save_to_file("Para finalizar, es hora de evaluar la sesión", 'EvaluarSesionIntro.wav')
    #     self.audioSpeaker.runAndWait()
    #     self.audioSpeaker.save_to_file("{nombreNiño}, ¿te ha gustado la sesión? Muéstrame cuanto del uno al diez".replace("{nombreNiño}", self.datosSesion[3]), 'EvaluarSesionChild.wav')
    #     self.audioSpeaker.runAndWait()
    #     self.audioSpeaker.save_to_file("Ahora los mayores, ¿Crees que esta sesión a ayudado a {nombreNiño}? Muestrame cuanto del uno al diez".replace("{nombreNiño}", self.datosSesion[3]), 'EvaluarSesionTerapeuta.wav')
    #     self.audioSpeaker.runAndWait()
    #
    # def play_audio(self, nameFile):
    #     pkts = audio_lib.load_wav(nameFile)
    #     self.robot.set_volume(65535)
    #     cli.play_audio("audio.wav")
    #     cli.wait_for(pycozmo.event.EvtAudioCompleted)

    def closeEvent(self, event):
        self.cozmo.robot.disconnect()
        event.accept()  # let the window close

    def instanciarAudio(self):
        if self.audioSpeaker:
            del(self.audioSpeaker)
        self.audioSpeaker = pyttsx3.init()
        self.audioSpeaker.setProperty('rate', 200)
        self.audioSpeaker.setProperty('voice', 'spanish+f1')  # voz lo más femenina posible
