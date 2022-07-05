from learnblock.Devices import Emotions

def is_Neutral(lbot):
    if lbot.getCurrentEmotion() == Emotions.Neutral:
        return True
    return False
