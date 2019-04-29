import sys
import cv2

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ui_mainwindow import *
from dshow_graph import FilterGraph
from VideoDisplayManager import VideoDisplayManager
from VideoPlayerThread import VideoPlayerThread

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.PB_BrowseButtonOne.clicked.connect(self.open_file_dialog)
        self.ui.PlayPauseButton.clicked.connect(self.start_video_player_thread)
        self.video_to_play = None
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

    def open_file_dialog(self):
        dlg = QFileDialog()
        dlg.setNameFilters(["Video files (*.avi)"])
        dlg.selectNameFilter("Video files (*.avi)")
        dlg.exec_()
        try:
            self.video_to_play = dlg.selectedFiles()[0]
            self.ui.lineEdit.setText(self.video_to_play)
        except IndexError:
            self.video_to_play = None

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

    def start_video_player_thread(self):
        self.vpt = VideoPlayerThread(self, self.video_to_play)
        for c in self.video_display_manager.camera_list:
            c.preview_thread.shouldPause = True
        self.vpt.sendPixmapSignal.connect(self.set_image)
        self.vpt.changeSliderPosition.connect(self.set_slider_position)
        self.vpt.changeSliderTickCount.connect(self.change_slider_tick_count)
        self.ui.pushButton_4.clicked.connect(self.vpt.fast_forward)
        self.ui.horizontalSlider.sliderMoved.connect(self.vpt.change_video_frame)
        self.ui.StopButton.clicked.connect(self.vpt.stop)
        self.vpt.threadFinished.connect(self.disconnect)
        self.vpt.start()

    def change_slider_tick_count(self, tick_count):
        self.ui.horizontalSlider.setMaximum(tick_count)

    def set_slider_position(self, num):
        self.ui.horizontalSlider.setValue(num)

    def disconnect(self):
        self.vpt.sendPixmapSignal.disconnect()
        for c in self.video_display_manager.camera_list:
            c.preview_thread.shouldPause = False
        self.vpt = None

    def set_image(self, func, image):
        func(QPixmap.fromImage(image))

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


