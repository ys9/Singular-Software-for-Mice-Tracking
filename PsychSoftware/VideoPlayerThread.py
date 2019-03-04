from MainWindow import *
import numpy as np
import time

class VideoPlayerThread(QThread):

    changePixmap = Signal(QImage)
    threadFinished = Signal()

    def __init__(self, parent):
        return super().__init__(parent)

    def run(self):
        vid = cv2.VideoCapture('output.avi')
        start = time.time()
        while(vid.isOpened()):
            ret, frame = vid.read()
            if ret:

                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)

                if cv2.waitKey(15) & 0xFF == ord('q'):
                    break

                self.changePixmap.emit(p)
            else:
                break

        end = time.time()
        print("elapsed time =", end - start)

        vid.release()
        self.threadFinished.emit()