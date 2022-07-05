from learnblock.Devices import Emotions

def is_Angry(lbot):
    if lbot.getCurrentEmotion() == Emotions.Anger:
        return True
    return False
