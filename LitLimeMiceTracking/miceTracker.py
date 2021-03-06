import cv2 
from MainWindow import * 


class miceTracker():
        ## Send capture object which was instantiated using cv2.VideoCapture()
        def __init__(self, height, width, name_CSV):
                self.height = height 
                self.width = width 
                self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)) 
                #self.fgbg = cv2.bgsegm.createBackgroundSubtractorMOG() 
                self.fgbg = cv2.bgsegm.createBackgroundSubtractorMOG() 
                self.coordinates = []
                self.filename = name_CSV
                self.file = open(self.filename, 'w+')

        def check_frame(self, frame):
                if frame is None:
                        print("Error: Frame is None")
                        return 
                # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) 
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #gray = cv2.resize(gray, (self.width, self.height)) 
                gray = cv2.blur(frame, (21, 21))
                fgmask = self.fgbg.apply(gray, 0.005)                
                fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, self.kernel)
                thresh = cv2.threshold(fgmask, 128, 255, cv2.THRESH_BINARY)[1]
                contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

                maxArea = 0
                flag = True
                for c in contours:
                        if cv2.contourArea(c) < 1000:
                                flag = True
                                continue 
                        if cv2.contourArea(c) > maxArea:
                                flag = False
                                maxArea = cv2.contourArea(c) 
                                (x, y, w, h) = cv2.boundingRect(c) 
                                self.coordinates.append((x, y, w, h))
                                if (len(self.coordinates) > 20):
                                        self.update_file()
                if not flag:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                return frame

        def init_track_frame(self, x, y, w, h, frame):
                self.tracker = cv2.Tracker_create('CSRT') 
                bbox = (x, y, w, h)
                ok = self.tracker.init(frame, bbox) 
        
        def track_frame(self, frame):
                ok, bbox = self.tracker.update(frame) 
                return bbox


        def calculate_cg(self, x, y, w, h):
                return ((x + w) / 2, (y + h) / 2)

        def update_file(self):
                try:
                        # f = open(self.filename, 'a') 
                        # wr = csv.writer(f, quoting=csv.QUOTE_ALL)
                        # wr.writerow(self.coordinates)
                        for i in self.coordinates:
                                y = self.calculate_cg(i[0], i[1], i[2], i[3])
                                print(str(y[0]) + "," + str(y[1]), file=self.file)
                                # self.f.write(str(y[0]) + "," + str(y[1]))   
                                self.coordinates.remove(i)
                        # f.close()
                except IOError:
                        print("File cannot be opened. Will try again in the next iteration :)")
                except ValueError:
                        print("Wait, I'll Try again Later")
                except:
                        print("Error Occurred. Will try again in the next iteration")
        def __del__(self):
                self.file.close()