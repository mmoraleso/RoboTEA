#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import learnblock.Client as Client
import queue
import sys, os, numpy as np, PIL.Image as Image, PIL.ImageFilter as ImageFilter, io, cv2, paho.mqtt.client, threading, math
import time

import pycozmo
from PySide2.QtCore import QThread
from PySide2.QtWidgets import QApplication
from tensorflow_estimator.python.estimator.estimator import maybe_overwrite_model_dir_and_session_config

from PantallaDeCarga import PantallaDeCarga

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(path, ".."))

from learnblock.Client import *
from learnblock.functions import getFuntions

import cozmo as cozmoR
from cozmo.util import radians, degrees, distance_mm, speed_mmps
from learnblock.Devices import *


cozmo = None
K = 1  # Speed constant
L = 45  # Distance between wheels


def cozmo_program(_robot: cozmoR.robot.Robot):
    global cozmo
    global stopThread
    cozmo = _robot
    while not stopThread:
       # print("Dentro de while not stopThread path: " + os.path.join(path, ".."))
        pass

class Robot(Client):
    devicesAvailables = ["base", "camera", "display", "jointmotor", "groundsensors", "acelerometer", "gyroscope", "speaker"]

    def __init__(self):
        global cozmo
        global stopThread
        stopThread = False
        self.app = QApplication.instance()
        Client.__init__(self)
        self.pantallaDeCarga = PantallaDeCarga()
        # time.sleep(2)
        self.mostrarPantallas()
        self.pantallaDeCarga.receiveLoadingPageInfo(10)
        self.pantallaDeCarga.receiveLoadingPageInfo(25)
        print("publishin... " + str(25))
        self.app.processEvents()
        # self.addGroundSensors(GroundSensors(_readFunction=self.deviceReadGSensor))
        # self.addAcelerometer(Acelerometer(_readFunction=self.deviceReadAcelerometer))
        # self.addGyroscope(Gyroscope(_readFunction=self.deviceReadGyroscope, _resetFunction=self.deviceResetGyroscope), "Z_AXIS")
        self.addCamera(Camera(_readFunction=self.deviceReadCamera))
        # self.addBase(Base(_callFunction=self.deviceMove))
        # self.addDisplay(Display(_setEmotion=self.deviceSendEmotion, _setImage=None))
        # self.addJointMotor(JointMotor(_callDevice=self.deviceSendAngleHead, _readDevice=None), "CAMERA")
        # self.addJointMotor(JointMotor(_callDevice=self.deviceSendAngleArm, _readDevice=None), "ARM")
        self.addSpeaker(Speaker(_sendText=self.deviceSendText))
        self.connectToRobot()
        # self.cozmo = cozmo
        # self.cozmo.camera.image_stream_enabled = True
        # self.cozmo.camera.color_image_enabled = True
        # self.cozmo.enable_device_imu(enable_raw=True, enable_gyro = True)
        # self.current_pose_angle = 0
        # self.vueltas = 0
        # self.last_pose_read = 0
        # self.CozmoBehaviors = {}
        # self.setBehaviors()
        self.app.processEvents()
        self.pantallaDeCarga.receiveLoadingPageInfo(75)
        self.app.processEvents()
        print("publishin... " + str(75))
        # self.start()
        self.app.processEvents()
        self.pantallaDeCarga.receiveLoadingPageInfo(100)
        self.app.processEvents()
        print("publishin... " + str(100))
        self.pantallaDeCarga.closePantallaCarga()
        self.isSaved = False
        cozmo = self.cozmo

    def connectToRobot(self):
        global stopThread
        stopThread = True
        print("Conectando cozmo con pycozmo")
        self.cozmo = pycozmo.Client()
        self.cozmo.start()
        self.cozmo.connect()
        self.cozmo.wait_for_robot()
        print("Se ha conectado cozmo con pycozmo")

    def disconnect(self):
        print("disconnecting")
        self.cozmo.disconnect()
        self.cozmo.stop()
        global stopThread
        stopThread = True

    def deviceSendText(self, text):
        self.cozmo.play_audio(text)
        self.cozmo.wait_for(pycozmo.event.EvtAudioCompleted)
    def deviceSendTextHuman(self, text):
        self.cozmo.say_text(text=text, in_parallel=True,use_cozmo_voice=True,voice_pitch=-1.0)

    def deviceSendAngleArm(self, _angle):
        angle_rad = math.radians(_angle)
        if angle_rad > 0.79:
            angle_rad = 0.79
        elif angle_rad < -0.20:
            angle_rad = -0.20
        a = (angle_rad + 0.20) / (0.79 + 0.20)
        self.cozmo.set_lift_height(a, in_parallel=True)

    def deviceSendAngleHead(self, _angle):
        a = degrees(_angle)
        self.cozmo.set_head_angle(a, in_parallel=True)

    def deviceSendEmotion(self, _emotion):
        if self.cozmo.has_in_progress_actions:
            return
        trigger = None
        if _emotion is Emotions.Joy:
            trigger = cozmoR.anim.Triggers.PeekABooGetOutHappy
        elif _emotion is Emotions.Sadness:
            trigger = cozmoR.anim.Triggers.PeekABooGetOutSad
        elif _emotion is Emotions.Surprise:
            trigger = cozmoR.anim.Triggers.PeekABooSurprised
        elif _emotion is Emotions.Disgust:
            trigger = None
        elif _emotion is Emotions.Anger:
            trigger = cozmoR.anim.Triggers.DriveEndAngry
        elif _emotion is Emotions.Fear:
            trigger = cozmoR.anim.Triggers.CodeLabScaredCozmo
        elif _emotion is Emotions.Neutral:
            trigger = cozmoR.anim.Triggers.NeutralFace
        if trigger is not None:
            self.cozmo.play_anim_trigger(trigger, in_parallel=True, ignore_body_track=True,
                                         ignore_head_track=True, ignore_lift_track=True)
            self.cozmo.wait_for_all_actions_completed()

    def deviceReadGyroscope(self):
        rz_n = self.cozmo.pose.rotation.angle_z.degrees
        if rz_n < 0:
            rz_n = 360 + rz_n
        if math.fabs(self.last_pose_read-rz_n) > 180:
            self.vueltas = self.vueltas+np.sign(self.last_pose_read-rz_n)
        self.last_pose_read = rz_n
        rz = rz_n - self.current_pose_angle + self.vueltas*360
        # print("Cozmo gyro", rz_n, rz)
        return int(-rz)

    def deviceResetGyroscope(self):
        self.vueltas=0
        self.current_pose_angle = self.cozmo.pose.rotation.angle_z.degrees
        if self.current_pose_angle < 0:
            self.current_pose_angle = 360 + self.current_pose_angle
        self.last_pose_read = self.current_pose_angle

    def deviceReadAcelerometer(self):
        return self.cozmo.accelerometer.x_y_z

    def deviceReadGSensor(self):
        if self.cozmo.is_cliff_detected:
            ground = 0
        else:
            ground = 100
        return {"central": ground}

    def deviceReadCamera(self):
        print("Realizando foto")
        self.cozmo.enable_camera(enable=True, color=True)
            # Wait for image to stabilize.
        time.sleep(2.0)

        self.cozmo.add_handler(pycozmo.event.EvtNewRawCameraImage, self.on_camera_image, one_shot=True)
        time.sleep(1)
        while not self.isSaved:
            time.sleep(0.5)
        cv_image = cv2.imread(os.path.dirname(__file__) + '/../camera/camera.png', cv2.COLOR_RGB2GRAY)
        if cv_image is not None:
            self.isSaved = False
            return cv_image, True
        else:
            self.isSaved = False
            return None, False

    def deviceMove(self, SAdv, SRot):
        SRot_rad = math.radians(SRot)
        if SRot_rad != 0.:
            Rrot = SAdv / SRot_rad

            Rl = Rrot - (L / 2)
            l_wheel_speed = SRot_rad * Rl * 2

            Rr = Rrot + (L / 2)
            r_wheel_speed = SRot_rad * Rr * 2
        else:
            l_wheel_speed = SAdv * K
            r_wheel_speed = SAdv * K
        self.cozmo.drive_wheel_motors(r_wheel_speed, l_wheel_speed, 0, 0)

    def setBehaviors(self):
        self.CozmoBehaviors["bored"] = cozmoR.anim.Triggers.CodeLabBored
        self.CozmoBehaviors["cat"] = cozmoR.anim.Triggers.CodeLabCat
        self.CozmoBehaviors["dance_mambo"] = cozmoR.anim.Triggers.DanceMambo
        self.CozmoBehaviors["dog"] = cozmoR.anim.Triggers.CodeLabDog
        self.CozmoBehaviors["duck"] = cozmoR.anim.Triggers.CodeLabDuck
        self.CozmoBehaviors["elephant"] = cozmoR.anim.Triggers.CodeLabElephant
        self.CozmoBehaviors["idle"] = cozmoR.anim.Triggers.CodeLabIdle
        self.CozmoBehaviors["sheep"] = cozmoR.anim.Triggers.CodeLabSheep
        self.CozmoBehaviors["sleep"] = cozmoR.anim.Triggers.CodeLabSleep
        self.CozmoBehaviors["sneeze"] = cozmoR.anim.Triggers.CodeLabSneeze
        self.CozmoBehaviors["zombie"] = cozmoR.anim.Triggers.CodeLabZombie
        self.CozmoBehaviors["dancing"] = cozmoR.anim.Triggers.CodeLabWin
        self.CozmoBehaviors["dancingMambo"] = cozmoR.anim.Triggers.CodeLabDancingMambo
        self.CozmoBehaviors["unhappy"] = cozmoR.anim.Triggers.CubePounceLoseSession


    def sendBehaviour(self, bhv):
        if bhv in self.CozmoBehaviors.keys():
            self.cozmo.wait_for_all_actions_completed()
            self.cozmo.play_anim_trigger(self.CozmoBehaviors[bhv]).wait_for_completed()
#            self.cozmo.wait_for_all_actions_completed()

    def doWInDance(self, bien):
        print("Celebrando")
        self.cozmo.load_anims()
        if bien:
            self.cozmo.play_anim("anim_meetcozmo_celebration_02")
        else:
            self.cozmo.play_anim("anim_dizzy_pickup_01")
        self.cozmo.wait_for(pycozmo.event.EvtAnimationCompleted)

    def getPantallaCargaLoadingValue(self):
        return self.pantallaDeCarga.getLoadingBarValue()

    def mostrarPantallas(self):
        if self.pantallaDeCarga.getLoadingBarValue() < 100:
            if self.pantallaDeCarga.isVisibleCarga():
                print("Hiding pantalla de carga")
                self.pantallaDeCarga.hideCarga()
            else:
                print("Opening pantalla de carga")
                self.pantallaDeCarga.showCarga()
    # def getCozmo(self):
    #     return self.cozmo

    def on_camera_image(self, cli, image):
        print("saving image: ")
        image.save(os.path.dirname(__file__) + '/../camera/camera.png', "PNG")
        self.isSaved = True
        print("Image already saved")

    def celebrar(self):
        print("Celebrando")
        self.cozmo.load_anims()
        self.cozmo.play_anim("anim_meetcozmo_celebration_02")
        self.cozmo.wait_for(pycozmo.event.EvtAnimationCompleted)

    def seleccionErronea(self):
        print("Mostrando que la respuesta es errónea")
        self.cozmo.load_anims()
        self.cozmo.play_anim("anim_dizzy_pickup_01")
        self.cozmo.wait_for(pycozmo.event.EvtAnimationCompleted)

if __name__ == '__main__':
    robot = Robot()
    robot.speakText("hola")
    robot.join()
