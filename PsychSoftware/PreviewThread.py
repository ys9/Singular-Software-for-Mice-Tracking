from MainWindow import *
#import numpy as np

class PreviewThread(QThread):

    changePixmap = Signal(QImage)

    def __init__(self, parent, device_id):
        self.shouldPreview = True
        self.device_id = device_id
        return super().__init__(parent)

    def run(self):
        self.cap = cv2.VideoCapture(self.device_id)
        self.cap.set(cv2.cv2.CAP_PROP_FPS, 60)
        while self.shouldPreview:
            ret, frame = self.cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    
