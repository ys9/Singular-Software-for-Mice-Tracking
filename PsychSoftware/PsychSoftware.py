from MainWindow import *

def window():
    app = QApplication([])

    LitLimeWindow = MainWindow()
    LitLimeWindow.show()

    app.exec_()
    print("done")

    LitLimeWindow.stop_video_threads()


if __name__ == '__main__':
   window()



