import cv2
from background import get_bg
import numpy as np

path = 'traffic.mp4'
cap = cv2.VideoCapture(path)

width = int(cap.get(3))
height = int(cap.get(4))
fourcc = cv2.VideoWriter_fourcc(*'h264')
output = cv2.VideoWriter('detected_obj', fourcc, 10, (width, height))

back_fun = get_bg(path)
back_fun = cv2.cvtColor(back_fun, cv2.COLOR_BGR2GRAY)
frame_count = 0
consec_frames = 8

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        frame_count += 1
        org_frame = frame.copy()
        #print(frame_count)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if frame_count == 1:
            print('created list')
            frame_diff_list = []

        frame_diff = cv2.absdiff(gray, back_fun)
        #print('frame_diff', frame_diff)
        ret, thresh = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)
        #print('thresh',thresh)
        dilate = cv2.dilate(thresh, None, iterations=40)
        #print('dilate', dilate)
        frame_diff_list.append(dilate)
        #print(type(frame_diff_list))

        if len(frame_diff_list) == consec_frames:
            print('success')
            sum_frames = sum(frame_diff)
            contours, hierarchy = cv2.findContours(
                sum_frames, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            print(contours)

            for contour in contours:
                if cv2.contourArea(contour) < 500:
                    continue

                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(org_frame, (x, y), (x + w, y + h), (0, 255, 255), 5)
            cv2.imshow('detected', org_frame)
            output.write(org_frame)
            if cv2.waitKey() == ord('q'):
                break

    else:
        break

cap.release()
cv2.destroyAllWindows()