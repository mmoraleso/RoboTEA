from learnblock.Devices import Emotions

def is_Sadness(lbot):
    if lbot.getCurrentEmotion() == Emotions.Sadness:
        return True
    return False
