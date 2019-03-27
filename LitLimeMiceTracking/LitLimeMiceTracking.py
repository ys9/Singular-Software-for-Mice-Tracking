import sys
from MainWindow import MainWindow, QApplication

def main():
    app = QApplication([])

    LitLimeWindow = MainWindow()
    LitLimeWindow.show()

    app.exec_()
    print("done")
    LitLimeWindow.stop_all_threads()

if __name__ == '__main__':
    main()
