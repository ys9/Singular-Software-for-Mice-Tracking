import sys
import cv2

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ui_mainwindow import *
from dshow_graph import FilterGraph
from VideoDisplayManager import VideoDisplayManager

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        graph = FilterGraph()
        self.camera_id_list = []
        self.should_reset_preview = True
        self.camera_checkbox_references = [self.ui.Camera1Checkbox, self.ui.Camera2Checkbox, self.ui.Camera3Checkbox, self.ui.Camera4Checkbox]
        self.connected_cameras = graph.get_input_devices()
        self.modify_camera_options()
        self.ui.PR_OptionsApplyButton.clicked.connect(self.apply_preview_options)

    def stop_all_threads(self):
        for camera in self.video_display_manager.camera_list:
            camera.preview_thread.shouldPreview = False
            while camera.preview_thread.isRunning():
                continue

        self.video_display_manager.shouldCapture = False
        while self.video_display_manager.isRunning():
            continue

    def modify_camera_options(self):
        for i in range(len(self.connected_cameras)):
            self.camera_checkbox_references[i].setText(self.connected_cameras[i])
        i+=1
        while i < 4:
            self.camera_checkbox_references[i].setText("")
            self.camera_checkbox_references[i].setEnabled(False)
            i+=1
        pass

    def start_vdm(self):
        self.video_display_manager = VideoDisplayManager(self, self.camera_id_list)
        self.video_display_manager.start()

    def apply_preview_options(self):
        i = 0
        for selection in self.camera_checkbox_references:
            if selection.isChecked() and not i in self.camera_id_list:
                self.camera_id_list.append(i)
                self.should_reset_preview = True
            i+=1
        if self.should_reset_preview:
            self.should_reset_preview = False
            self.start_vdm()
        else:
            pass #set record time of each camera


