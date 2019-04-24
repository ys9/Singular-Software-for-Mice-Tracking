# from imutils.video import VideoStream 
# import argparse 
# import datetime 
# import imutils 
# import time 
# import cv2 


# ap = argparse.ArgumentParser() 

# ap.add_argument("-v", "--video", help="path to the video file")
# ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
# args = vars(ap.parse_args) 

# if args.get("video", None) is None:
#         vs = VideoStream(src=0).start()
#         time.sleep(2.0)
# else:
#         vs = cv2.VideoCapture(args["video"])
# firstFrame = None 

# while True:
#         frame = vs.read() 
#         frame = frame if args.get("video", None) is None else frame[1]
#         text = "Unoccupied"

#         if frame is None:
#                 break
#         frame = imutils.resize(frame, width=500) 
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         gray = cv2.GaussianBlur(gray, (21, 21), 0)

#         if firstFrame is None:
#                 firstFrame = gray 
#                 continue 
        
#         frameDelta = cv2.absdiff(firstFrame, gray)
#         thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

#         thresh = cv2.dilate(thresh, None, iterations=2)
#         cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         cnts = imutils.grab_contours(cnts) 


#         for c in cnts:
#                 if cv2.contourArea(c) < 500:
#                         continue 
#                 (x, y, w, h) = cv2.boundingRect(c) 
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 
#                 print(" x: " + str(x) +
#                 " y: " + str(y) + 
#                 " w: " + str(w) + 
#                 " h: " + str(h))
#                 text = "Occupied"
#         cv2.imshow("feed", frame)
#         cv2.imwrite("mice1.jpg", frame)
#         key = cv2.waitKey(1) & 0xff
        
#         if key == ord("q"):
#                 break 
#         break
# vs.stop() if args.get("video", None) is None else vs.release()
# cv2.destroyAllWindows() 


import cv2 

cap = cv2.VideoCapture('micetest.avi') 
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
firstFrame = None 
while True:
        ok, frame = cap.read() 
        frame = cv2.resize(frame, (500, 500)) 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        gray = cv2.GaussianBlur(gray, (21, 21), 0) 

        if firstFrame is None:
                firstFrame = gray 
                continue 
        frameDelta = cv2.absdiff(firstFrame, gray) 
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1] 
        thresh = cv2.dilate(thresh, kernel=kernel, iterations=2) 
        cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
        # area = {}
        # for c in cnts:
        #         # area[c] = cv2.contourArea(c) 
        # maxArea = max(area)
        # (x, y, w, h) = cv2.boundingRect(maxArea)
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 
        maxArea = 0
        for c in cnts:
                if cv2.contourArea(c) < 1000:
                        continue         
                if cv2.contourArea(c) > maxArea:
                        maxArea = cv2.contourArea(c)
                        (x, y, w, h) = cv2.boundingRect(c)
        # (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 
        # print("x: " + str(x) + " y: " + str(y) + " w: " + str(w) + " h: " + str(h)) 
        cv2.imshow("frame", frame) 

        firstFrame = gray
        if cv2.waitKey(5) >= 0:
                break 
cap.release()