import sys
import cv2

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ui_mainwindow import *
from VideoDisplayManager import VideoDisplayManager

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.video_display_manager = VideoDisplayManager(self, [0,1])
        self.video_display_manager.start()

    def stop_all_threads(self):
        for camera in self.video_display_manager.camera_list:
            camera.preview_thread.shouldPreview = False
            while camera.preview_thread.isRunning():
                continue

        self.video_display_manager.shouldCapture = False
        while self.video_display_manager.isRunning():
            continue
