from MainWindow import *

class RecordingThread(QThread):
    def __init__(self, parent, cap):
        self.shouldPreview = True
        self.cap = cap
        self.frame_rate = 60.0
        return super().__init__(parent)

    def run(self):
        four_character_code = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', four_character_code, self.frame_rate, (640,480))
        frames_written = 0
        desired_frames = 600

        while(frames_written < desired_frames):
            ret, frame = self.cap.read()
            if ret == True:
                out.write(frame)
                frames_written+=1
            else:
                break



