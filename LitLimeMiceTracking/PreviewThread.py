from MainWindow import *
#import numpy as np
import time
from miceTracker import *

class PreviewThread(QThread):

    changePixmap = Signal(QImage)
    average_fps = 0
    frames_counted = 0

    #def __init__(self, camera, parent, capture_device):
    def __init__(self, parent, capture_device):
        QThread.__init__(self)
        self.shouldPreview = True
        self.shouldPause = False
        self.division = parent.division
        self.capture_device = capture_device
        self.frame_width = parent.frame_width
        self.frame_height = parent.frame_height
        self.mice_tracker = miceTracker(int(self.frame_height/self.division), int(self.frame_width/self.division), "software_engineering_sucks.csv")

    def run(self):
        while self.shouldPreview:
            if self.shouldPause:
                time.sleep(1)
                continue
            #chk1 = time.time()
            ret, frame = self.capture_device.read()
            #chk2 = time.time()
            if ret:
                # rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mouse_frame = self.mice_tracker.check_frame(frame)
                #p = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                #convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                convertToQtFormat = QImage(mouse_frame.data, mouse_frame.shape[1], mouse_frame.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(self.frame_width/self.division, self.frame_height/self.division, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
            #else:
            #    break
            #if chk2 == chk1 or (chk2 - chk1) < 0.01: #don't evaluate if more than 100fps, getting weird values when not doing this
            #    continue

            #self.frames_counted += int(1/(chk2 - chk1))
            #self.average_fps = int(self.frames_counted / self.frame_count)

            #self.measured_fps = int(1/(chk2 - chk1))
            #print("fps = ", self.measured_fps)
            #print("fps = ", self.average_fps)
