# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Kula\Petrobras\OpenPulse\data\user_input\ui\Analysis\runAnalysisInput.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(600, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(600, 450))
        Dialog.setMaximumSize(QtCore.QSize(600, 450))
        Dialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("c:\\Users\\Kula\\Petrobras\\OpenPulse\\data\\user_input\\ui\\Analysis\\../../../../../../Downloads/load - Copia.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setWhatsThis("")
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.frame_title = QtWidgets.QFrame(Dialog)
        self.frame_title.setGeometry(QtCore.QRect(0, 0, 600, 51))
        self.frame_title.setMinimumSize(QtCore.QSize(600, 0))
        self.frame_title.setMaximumSize(QtCore.QSize(600, 16777215))
        self.frame_title.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_title.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_title.setLineWidth(1)
        self.frame_title.setObjectName("frame_title")
        self.label_title = QtWidgets.QLabel(self.frame_title)
        self.label_title.setGeometry(QtCore.QRect(6, 6, 589, 39))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setTextFormat(QtCore.Qt.AutoText)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.frame_message = QtWidgets.QFrame(Dialog)
        self.frame_message.setGeometry(QtCore.QRect(0, 50, 600, 400))
        self.frame_message.setMinimumSize(QtCore.QSize(600, 400))
        self.frame_message.setMaximumSize(QtCore.QSize(600, 400))
        self.frame_message.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_message.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_message.setObjectName("frame_message")
        self.label_message = QtWidgets.QLabel(self.frame_message)
        self.label_message.setGeometry(QtCore.QRect(6, 6, 589, 389))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_message.setFont(font)
        self.label_message.setAlignment(QtCore.Qt.AlignCenter)
        self.label_message.setObjectName("label_message")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Run analysis"))
        self.label_title.setText(_translate("Dialog", "Run analysis"))
        self.label_message.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#0000ff;\">Solution in progress…</span></p></body></html>"))
