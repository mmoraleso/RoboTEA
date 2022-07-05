from learnblock.Devices.Base import Base
from learnblock.Devices.DistanceSensors import DistanceSensors
from learnblock.Devices.GroundSensors import GroundSensors
from learnblock.Devices.Gyroscope import Gyroscope
from learnblock.Devices.Acelerometer import Acelerometer
from learnblock.Devices.Camera import Camera
from learnblock.Devices.JointMotor import JointMotor
from learnblock.Devices.Display import Display
from learnblock.Devices.Led import Led, LedStatus, RGBLed
from learnblock.Devices.Speaker import Speaker
from learnblock.Devices.Matrix import Matrix
from learnblock.Devices.MP3 import MP3
from learnblock.Devices.Ir import Ir
from learnblock.Devices.LightSensor import LightSensor
from learnblock.Devices.Controller import Controller
from enum import Enum


__all__ = ['Display', 'Base', 'DistanceSensors', 'GroundSensors', 'Gyroscope', 'Acelerometer', 'Camera', 'Emotions', 'JointMotor', 'Speaker', 'Led', 'RGBLed', 'LedStatus','Matrix','MP3','Ir','LightSensor','Controller']

class Emotions(Enum):
    NoneEmotion = -1
    Fear = 0
    Surprise = 1
    Anger = 2
    Sadness = 3
    Disgust = 4
    Joy = 5
    Neutral = 6
