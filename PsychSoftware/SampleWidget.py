from ui_sample_widget import *

class SampleWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SampleWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)


