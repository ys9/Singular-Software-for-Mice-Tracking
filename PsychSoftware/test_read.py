import numpy as np
import cv2

cap = cv2.VideoCapture('output.avi', 0)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
	    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	    cv2.imshow('frame',gray)
	    if cv2.waitKey(1) & 0xFF == ord('q'):
		    break
    else:
        break

cap.release()
cv2.destroyAllWindows()