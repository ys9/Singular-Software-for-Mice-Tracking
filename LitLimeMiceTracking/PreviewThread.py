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
        self.mice_tracker = miceTracker(int(self.frame_height/self.division), int(self.frame_width/self.division), "test.csv")

    def run(self):
        while self.shouldPreview:
            if self.shouldPause:
                time.sleep(1)
                continue
            ret, frame = self.capture_device.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mouse_frame = self.mice_tracker.check_frame(rgbImage)
                convertToQtFormat = QImage(mouse_frame.data, mouse_frame.shape[1], mouse_frame.shape[0], QImage.Format_RGB888)
                #convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(self.frame_width/self.division, self.frame_height/self.division, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

