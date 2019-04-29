from MainWindow import *

from Camera import Camera
from VideoPlayerThread import VideoPlayerThread
from collections import deque
import time
import types

class VideoDisplayManager(QThread):
    
    max_cameras = 4

    changePixmap = Signal(types.FunctionType, QImage)
    vptStarted = Signal()

    camera_list = []

    def __init__(self, parent, device_id):
        QThread.__init__(self)
        self.shouldCapture = True
        self.vpt = None
        self.add_cameras(device_id)
        self.parent = parent
        self.create_label_array()
        self.set_divisions()
        self.connect_pixmap()
        self.connect_buttons()
        #print(parent.ui.gridLayoutWidget.geometry())
        self.start_all_camera_previews() # get rid of soon


    def connect_pixmap(self):
        self.changePixmap.connect(self.set_image)

    def connect_buttons(self):
        #self.parent.ui.PlayPauseButton.clicked.connect(self.start_video_player_thread)
        for camera in self.camera_list:
            camera.set_output_filename('camera' + str(camera.device_id)+ '.avi')
            self.parent.ui.RecordButton.clicked.connect(camera.begin_video_recording_thread)

    def start_all_camera_previews(self):
        for camera in self.camera_list:
            camera.begin_preview_thread()

    def set_divisions(self):
        if len(self.camera_list) > 1:
            for camera in self.camera_list:
                camera.division = 2
        else:
            self.camera_list[0].division = 1

    def create_label_array(self):
        self.label_array = []
        if len(self.camera_list) > 1:
            i = 0
            #for camera in self.camera_list:
            for c in range(self.max_cameras):
                tmp_label = QLabel(self.parent.ui.gridLayoutWidget)
                tmp_label.setText("")
                tmp_label.setObjectName("PreviewVideo" + str(i))
                row = i & 0x2
                column = i & 0x1
                self.parent.ui.gridLayout.addWidget(tmp_label, row, column, 1,1)
                self.label_array.append(tmp_label.setPixmap)
                i += 1
        elif len(self.camera_list) == 1:
            tmp_label = QLabel(self.parent.ui.gridLayoutWidget)
            tmp_label.setText("")
            tmp_label.setObjectName("PreviewVideo0")
            self.parent.ui.gridLayout.addWidget(tmp_label, 0, 0, 1, 1)
            self.label_array.append(tmp_label.setPixmap)

    #def start_video_player_thread(self):
    #    self.vpt = VideoPlayerThread(self.parent, 'output.avi')
    #    for c in self.camera_list:
    #        c.preview_thread.shouldPause = True
    #    self.vpt.sendPixmapSignal.connect(self.set_image)
    #    self.vpt.threadFinished.connect(self.disconnect)
    #    self.vpt.start()

    #def disconnect(self):
    #    self.vpt.sendPixmapSignal.disconnect()
    #    for c in self.camera_list:
    #        c.preview_thread.shouldPause = False
    #    self.vpt = None

    def set_image(self, func, image):
        func(QPixmap.fromImage(image))

    #pass either list of device id's or single device id
    def add_cameras(self, device_id):
        if isinstance(device_id, list):
            for id in device_id:
                self.add_cameras(id)
        else:
            self.camera_list.append(Camera(self, device_id, len(self.camera_list)))

    def remove_cameras(self, device_id):
        if isinstance(device_id):
            for id in device_id:
                self.remove_cameras(id)
        else:
            for cam in self.camera_list:
                if cam.device_id == device_id:
                    self.camera_list.remove(cam)

    def run(self):
        #sys.stdout = open('nul', 'w')  # Direct output to nowhere.

        while self.shouldCapture:
            for camera in self.camera_list:
                if len(camera.frame_queue) > 0:
                    frame = camera.frame_queue.popleft() #get qt frame from frame queue
                    #frame = frame.scaled(320, 240, Qt.KeepAspectRatio)
                    self.changePixmap.emit(self.label_array[camera.id], frame)
            #print()  # Print new line to nowhere.
            time.sleep(0.01)

        #sys.stdout = sys.__stdout__  # Direct output to console again.
