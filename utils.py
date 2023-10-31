import cv2
import numpy as np
import pygame


pygame.mixer.init()
improper_form = pygame.mixer.Sound("siren.mp3")

def detect_bicep_curls(frame, keypoints, rep_cnt, prev_rep, fault):
    
    img = frame.copy()
    y, x, c = frame.shape
    a, b, c = [keypoints[joint] for joint in ["left_shoulder", "left_elbow", "left_wrist"]]
        
    angleInRad = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angleInDeg = np.abs(angleInRad * 180.0 / np.pi)

    angleInDeg = angleInDeg if angleInDeg <= 180 else 360 - angleInDeg
    cv2.putText(img, str(int(angleInDeg)), (int(b[1]*x),int(b[0]*y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    if angleInDeg > 120:
        text = 'Take UP'
        prev_rep = True
        cv2.putText(img, text, (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    elif angleInDeg < 50:
        text = 'Take DOWN'
        if prev_rep:
            rep_cnt += 1
            fault = False
            prev_rep = False
        cv2.putText(img, text, (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    else:
        text = 'Less Go'
        prev_rep = True
        cv2.putText(img, text, (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    
    if abs(b[1] - a[1]) > 0.07:
        
#         improper_form.play()

        if not fault and rep_cnt > 0:
            rep_cnt -= 1
            fault = True
        cv2.putText(img, 'Improper Form', (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
 
    cv2.putText(img, str(rep_cnt), (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return img,rep_cnt,prev_rep, fault

        
def detect_pushup(frame, keypoints, rep_cnt, prev_rep, fault):
    img = frame.copy()
    y, x, c = frame.shape
    
    a, b, c = [keypoints[joint] for joint in ["left_wrist", "nose", "right_wrist"]]

    angleInRad = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angleInDeg = np.abs(angleInRad * 180.0 / np.pi)

    angleInDeg = angleInDeg if angleInDeg <= 180 else 360 - angleInDeg
    cv2.putText(img, str(int(angleInDeg)), (int(b[1]*x),int(b[0]*y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

    if angleInDeg < 80:
        text = 'GO DOWN'
        prev_rep = True
        cv2.putText(img, text, (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    elif angleInDeg > 120:
        text = 'GO UP'
        if prev_rep:
            rep_cnt += 1
            fault = False
            prev_rep =  False
        cv2.putText(img, text, (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    else:
        text = 'Less Go'
        prev_rep = True
        cv2.putText(img, text, (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    if abs(keypoints["left_wrist"][1] - keypoints["right_wrist"][1]) < 0.2:
#         improper_form.play()

        if not fault and rep_cnt > 0:
            rep_cnt -= 1
            fault = True
        cv2.putText(img, 'Too Close', (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  
    elif abs(keypoints["left_wrist"][1] - keypoints["right_wrist"][1]) > 0.35:
#         improper_form.play()

        if not fault and rep_cnt > 0:
            rep_cnt -= 1
            fault = True
        cv2.putText(img, 'Shoulder Risk', (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.putText(img, str(rep_cnt), (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    return img, rep_cnt, prev_rep, fault


def detect_shoulder(frame, keypoints, rep_cnt, prev_rep, fault):
    img = frame.copy()
    y, x, c = frame.shape
    
    wrist_center = (keypoints["left_wrist"][0] + keypoints["right_wrist"][0]) /2
    shoulder_center = (keypoints["left_shoulder"][0] + keypoints["right_shoulder"][0]) /2
    

    d = abs(keypoints["right_wrist"][1] - keypoints["left_wrist"][1])
    
    if d > 0.6:
#         improper_form.play()

        text = 'Too Wide'
        cv2.putText(img, text, (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if not fault and rep_cnt > 0:
            rep_cnt -= 1
            fault = True
    elif d < 0.4 and abs(wrist_center - shoulder_center) < 0.1:
#         improper_form.play()

        text = 'Too Close'
        cv2.putText(img, text, (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if not fault and rep_cnt > 0:
            rep_cnt -= 1
            fault = True
    else:
        fault = False

    if abs(shoulder_center - wrist_center) > 0.25:
        text = 'Move Down'
        cv2.putText(img, text, (30,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        if prev_rep:
            rep_cnt += 1
            fault = False
            prev_rep = False
    elif abs(shoulder_center - wrist_center) < 0.15:
        text = 'Move Up'
        cv2.putText(img, text, (30,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        prev_rep = True
    else:
        text = "Less gO"
        cv2.putText(img, text, (30,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        prev_rep = True
        
    cv2.putText(img, str(rep_cnt), (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    return img, rep_cnt, prev_rep, fault


def detect_squats(frame, keypoints, rep_cnt, prev_rep, fault):
    img = frame.copy()
    y, x, c = frame.shape
    a, b, c = [keypoints[joint] for joint in ["right_hip", "right_knee", "right_ankle"]]
        
    angleInRad = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angleInDeg = np.abs(angleInRad * 180.0 / np.pi)

    angleInDeg = angleInDeg if angleInDeg <= 180 else 360 - angleInDeg
    cv2.putText(img, str(int(angleInDeg)), (int(b[1]*x),int(b[0]*y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
             
    if angleInDeg > 120:
        text = 'Go Down'
        prev_rep = True
        cv2.putText(img, text, (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    elif angleInDeg < 60:
        text = 'Come Up'
        if prev_rep:
            rep_cnt += 1
            fault = False
            prev_rep = False
        cv2.putText(img, text, (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    else:
        text = 'Less Go'
        prev_rep = True
        cv2.putText(img, text, (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    
    if abs(b[1] - c[1]) > 0.1:
#         improper_form.play()

        if not fault and rep_cnt > 0:
            rep_cnt -= 1
            fault = True
        cv2.putText(img, 'Knee Beyond Toes', (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    a, b, c = [keypoints[joint] for joint in ["right_shoulder","right_hip","right_knee"]]
        
    angleInRad = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angleInDeg = np.abs(angleInRad * 180.0 / np.pi)

    angleInDeg = angleInDeg if angleInDeg <= 180 else 360 - angleInDeg
    if angleInDeg < 60:
#         improper_form.play()

        if not fault and rep_cnt > 0:
            rep_cnt -= 1
            fault = True
        cv2.putText(img, f'Too Much Bend', (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        
    cv2.putText(img, str(rep_cnt), (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return img, rep_cnt, prev_rep, fault


