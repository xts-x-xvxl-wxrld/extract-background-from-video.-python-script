import cv2
import numpy as np


def get_bg(path):
    cap = cv2.VideoCapture(path)
    #select frames
    frames_indi = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=65)

    frames = []#store frames in an array
    for i in frames_indi:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        frames.append(frame)

    #calculate the median
    median = np.median(frames, axis=0).astype(np.uint8)
    return median
