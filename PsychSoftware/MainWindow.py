import sys
import cv2

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ui_mainwindow import *

from PreviewThread import PreviewThread
from RecordingThread import RecordingThread
from SampleDialog import SampleDialog
from SampleWidget import SampleWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.SampleDialogButton.clicked.connect(self.init_sample_dialog_window)
        self.ui.SampleWidgetButton.clicked.connect(self.init_sample_widget_window)
        self.ui.RecordButton.clicked.connect(self.start_record)
        self.th = PreviewThread(self, 0)
        self.th.changePixmap.connect(self.set_image)
        self.th.start()

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


