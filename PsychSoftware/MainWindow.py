import sys
import cv2

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ui_mainwindow import *

from PreviewThread import PreviewThread
from RecordingThread import RecordingThread
from VideoPlayerThread import VideoPlayerThread
from SampleDialog import SampleDialog
from SampleWidget import SampleWidget

from PySide2.QtCore import QMutex

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_button_connects()
        self.start_preview_thread()
        self.thread_count = 0
        self.mutex = QMutex()

    def start_video_player_thread(self):
        if self.thread_count > 0:
            return
        self.thread_count += 1
        self.th.shouldPause = True
        self.vpt = VideoPlayerThread(self)
        self.vpt.changePixmap.connect(self.set_image)
        self.vpt.threadFinished.connect(self.continue_preview)
        self.vpt.start()

    def continue_preview(self):
        self.thread_count -= 1
        self.th.shouldPause = False

    def start_preview_thread(self):
        self.th = PreviewThread(self, 0)
        self.th.changePixmap.connect(self.set_image)
        self.th.start()

    def setup_button_connects(self):
        self.ui.SampleDialogButton.clicked.connect(self.init_sample_dialog_window)
        self.ui.SampleWidgetButton.clicked.connect(self.init_sample_widget_window)
        self.ui.RecordButton.clicked.connect(self.start_record)
        self.ui.PlayButton.clicked.connect(self.start_video_player_thread)

    def set_image(self, image):
        self.ui.VideoArea.setPixmap(QPixmap.fromImage(image))

    def stop_video_threads(self):
        self.th.shouldPreview = False
        while self.th.isRunning():
            pass

    def init_sample_dialog_window(self):
        self.dialog = SampleDialog()
        self.dialog.show()

    def init_sample_widget_window(self):
        self.widget = SampleWidget()
        self.widget.show()

    def start_record(self):
        record_thread = RecordingThread(self, self.th.cap)
        record_thread.start()


