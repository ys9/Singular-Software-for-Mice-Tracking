from MainWindow import *
import time

class RecordingThread(QThread):
    def __init__(self, camera, capture_device, record_time, output_filename):
        QThread.__init__(self)
        self.record_time = record_time #IN SECONDS
        self.capture_device = capture_device
        self.output_filename = output_filename
        self.frame_rate = camera.frame_rate
        self.camera = camera

    def run(self):

        four_character_code = cv2.VideoWriter_fourcc(*'XVID')

        #wait_time = int((1 / self.frame_rate)*1000)

        if self.frame_rate != 0:
            wait_time = int((1 / self.frame_rate)*1000)
        else:
            wait_time = 15
            self.frame_rate = 60

        print(wait_time)

        frame_dimensions = (int(self.camera.frame_width), int(self.camera.frame_height))
        out = cv2.VideoWriter(self.output_filename, four_character_code, self.frame_rate, frame_dimensions)

        frames_written = 0

        total_frames_to_write = self.frame_rate * self.record_time

        start = time.time()

        while(frames_written < total_frames_to_write):
            ret, frame = self.capture_device.read()
            if ret:
                out.write(frame)
                frames_written += 1
            else:
                break
            key = cv2.waitKey(wait_time)

        out.release()
        end = time.time()

        print("record elapsed time =", end - start)
