# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SampleWidget.ui',
# licensing of 'SampleWidget.ui' applies.
#
# Created: Sat Mar  2 20:17:50 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 101))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 119, 101, 151))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.CheckBox1 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.CheckBox1.setObjectName("CheckBox1")
        self.verticalLayout.addWidget(self.CheckBox1)
        self.CheckBox2 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.CheckBox2.setObjectName("CheckBox2")
        self.verticalLayout.addWidget(self.CheckBox2)
        self.CheckBox3 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.CheckBox3.setObjectName("CheckBox3")
        self.verticalLayout.addWidget(self.CheckBox3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "SampleWidgetBoiiiis", None, -1))
        self.CheckBox1.setText(QtWidgets.QApplication.translate("Form", "Check this", None, -1))
        self.CheckBox2.setText(QtWidgets.QApplication.translate("Form", "Or check this", None, -1))
        self.CheckBox3.setText(QtWidgets.QApplication.translate("Form", "But not this", None, -1))

