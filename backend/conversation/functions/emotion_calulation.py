import numpy as np

def calculateEmotionRate(rate, emotion, count):
    sum_emotion_score = rate * count 
    weights = [[1.0], [0.5], [0.15], [0.1]]

    now_emotion_score = np.dot(emotion, weights)
    
    sum_emotion_score += now_emotion_score[0][0]
    emotion_rate = sum_emotion_score / (count + 1)
    return emotion_rate

def calculateBadRate(rate, emotion, count):
    now_bad_score = 0
    sum_bad_score = rate * count

    if emotion == 0:
        now_bad_score = 1.0
    elif emotion == 1:
        now_bad_score = 1.0
    
    sum_bad_score += now_bad_score
    bad_rate = sum_bad_score / (count + 1)
    return bad_rate