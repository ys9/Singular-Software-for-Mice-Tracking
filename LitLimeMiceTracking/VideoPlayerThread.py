from MainWindow import *
import time
import math
import types

class VideoPlayerThread(QThread):

    sendPixmapSignal = Signal(types.FunctionType, QImage)
    #changePixmap = Signal(QImage)

    #changeSliderPosition = Signal(int)
    #changeSliderTickCount = Signal(int)
    threadFinished = Signal()

    def __init__(self, parent, video_to_play):
        QThread.__init__(self)
        self.video_to_play = video_to_play
        self.video_label_function = parent.ui.PlaybackVideo.setPixmap

    def change_frame(self, frame_index):
        self.current_frame = frame_index
        self.currentTick = frame_index + 1

    def fast_forward(self):
        pass

    def rewind(self):
        pass

    def play(self):
        pass

    def pause(self):
        pass

    def run(self):
        vid = cv2.VideoCapture(self.video_to_play)
        video_file = open(self.video_to_play, 'rb')

        video_file.seek(32, 0) 
        ms = video_file.read(4) #read 33,34,35,36th byte from avi file. INFO -> # http://www.fastgraph.com/help/avi_header_format.html
                                #contains microseconds between frames
        video_file.seek(12, 1)
        fc = video_file.read(4) #read 48,49,50,51st byte from avi file.
                                #contains the number of frames in the avi file 

        ms_between_frames = int(int.from_bytes(ms, byteorder = sys.byteorder)/1000) - 1# -1 feels more natural
        #ms_between_frames = int.from_bytes(ms, byteorder = sys.byteorder)/1000000#

        frame_count = int.from_bytes(fc, byteorder = sys.byteorder)
        video_file.close()
        #ms_between_frames = int(ms_between_frames/8) #use this to make playback faster (fast-forward)

        #print("ms_between_frames = ", ms_between_frames)
        #self.changeSliderTickCount.emit(frame_count)

        self.current_frame = 0
        slider_update_interval = int(round(frame_count / 100)) #100 is number of positions on slider
        #print(slider_update_interval)
        self.current_tick = 1

        start = time.time()
        while(vid.isOpened()):
            if self.current_frame == self.current_tick - 1:
                ret, frame = vid.read()
            else:
                vid.set(cv2.cv2.CAP_PROP_POS_FRAMES, self.current_frame)
                self.currentTick = self.current_frame + 1
                ret, frame = vid.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)

                key = cv2.waitKey(ms_between_frames)
                #time.sleep(ms_between_frames) #might be able to use this to make playback more precise, 
                                               #since it works similarly and it can take a floating point argument

                #self.changeSliderPosition.emit(self.currentTick)
                self.current_frame += 1
                self.current_tick += 1

                #self.changePixmap.emit(p)
                self.sendPixmapSignal.emit(self.video_label_function, p)
                
                #time.sleep(0.001)
            else:
                break

        end = time.time()
        print("elapsed time =", end - start) # this seems to be working okay (playing at the correct rate)

        vid.release()
        self.threadFinished.emit()