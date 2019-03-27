import cv2
from PySide2.QtCore import QRect, QObject, Signal, Slot
from PySide2.QtGui import QImage
from collections import deque
from PreviewThread import PreviewThread
from RecordingThread import RecordingThread

class Camera(QObject):

    def __init__(self, parent, device_id, list_id):
        QObject.__init__(self)
        self.frame_queue = deque() #holds unscaled qt frames
        self.device_id = device_id
        self.division = 1
        self.parent = parent
        self.id = list_id
        self.capture_device = cv2.VideoCapture(self.device_id)
        self.frame_width = self.capture_device.get(cv2.cv2.CAP_PROP_FRAME_WIDTH)
        self.frame_height = self.capture_device.get(cv2.cv2.CAP_PROP_FRAME_HEIGHT)
        self.frame_rate = self.capture_device.get(cv2.cv2.CAP_PROP_FPS) #often zero?
        self.record_time = 10

    def set_division(self, division):
        self.division = division

    def begin_preview_thread(self):
        #self.preview_thread = PreviewThread(self, self.parent, self.capture_device)
        self.preview_thread = PreviewThread(self, self.capture_device)
        self.preview_thread.changePixmap.connect(self.add_image_to_queue)
        self.preview_thread.start()

    def begin_video_recording_thread(self):
        self.recording_thread = RecordingThread(self, self.capture_device, self.record_time, self.output_filename)
        self.preview_thread.changePixmap.connect(self.add_image_to_queue)
        self.recording_thread.start()

    def camera_is_connected(self):
        return self.capture_device.isOpened()

    def add_image_to_queue(self, image):
        self.frame_queue.append(image)

    def set_output_filename(self, filename):
        self.output_filename = filename

    def change_record_time(self, time_in_millis):
        self.record_time = time_in_millis
