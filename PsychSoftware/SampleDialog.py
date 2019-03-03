from ui_sample_dialog import *

class SampleDialog(QtWidgets.QDialog):
    def __init__(self):
        super(SampleDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


