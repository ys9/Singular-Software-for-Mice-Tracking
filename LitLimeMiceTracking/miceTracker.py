import cv2 
from MainWindow import * 


class miceTracker():
        ## Send capture object which was instantiated using cv2.VideoCapture()
        def __init__(self, height, width, name_CSV):
                self.height = height 
                self.width = width 
                self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)) 
                self.fgbg = cv2.bgsegm.createBackgroundSubtractorMOG() 
                self.coordinates = []
        def check_frame(self, frame):
                if frame is None:
                        print("Error: Frame is None")
                        return 
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
                gray = cv2.resize(gray, (self.width, self.height)) 
                gray = cv2.blur(frame, (21, 21))
                fgmask = fgbg.apply(gray, 0.005) 
                fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, self.kernel)
                thresh = cv2.threshold(fgmask, 128, 255, cv2.THRESH_BINARY)[1]
                contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

                maxArea = 0
                for c in contours:
                        if cv2.contourArea(c) < 1000:
                                continue 
                        if cv2.contourArea(c) > maxArea:
                                maxArea = cv2.contourArea(c) 
                                (x, y, w, h) = cv2.boundingRect(c) 
                                self.coordinates.append((x, y, w, h))
                                if (self.coordinates.len() > 20):
                                        update_file()
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                return frame
        
        
        def init_track_frame(self, x, y, w, h, frame):
                self.tracker = cv2.Tracker_create('CSRT') 
                bbox = (x, y, w, h)
                ok = self.tracker.init(frame, bbox) 
        
        def track_frame(self, frame):
                ok, bbox = tracker.update(frame) 
                return bbox


        def calculate_cg(self, x, y, w, h):
                return ((x + w) / 2, (y + h) / 2)

        def update_file(self):
                try:
                        f = open(self.filename, 'ab') 
                        # wr = csv.writer(f, quoting=csv.QUOTE_ALL)
                        # wr.writerow(self.coordinates)
                        f.write()
                except IOError:
                        print("File cannot be opened. Will try again in the next iteration :)")
                except:
                        print("Error Occurred. Will try again in the next iteration")
                finally:
                        f.close()