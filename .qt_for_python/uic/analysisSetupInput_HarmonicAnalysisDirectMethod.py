# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Kula\Petrobras\OpenPulse\data\user_input\ui\Analysis\Structural\analysisSetupInput_HarmonicAnalysisDirectMethod.ui'
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
        Dialog.resize(430, 339)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(430, 339))
        Dialog.setMaximumSize(QtCore.QSize(430, 339))
        Dialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("c:\\Users\\Kula\\Petrobras\\OpenPulse\\data\\user_input\\ui\\Analysis\\Structural\\../../../../../../Downloads/load - Copia.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setWhatsThis("")
        self.frame_3 = QtWidgets.QFrame(Dialog)
        self.frame_3.setGeometry(QtCore.QRect(0, 0, 430, 61))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setLineWidth(1)
        self.frame_3.setObjectName("frame_3")
        self.label_title = QtWidgets.QLabel(self.frame_3)
        self.label_title.setGeometry(QtCore.QRect(36, 4, 358, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setTextFormat(QtCore.Qt.AutoText)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.label_subtitle = QtWidgets.QLabel(self.frame_3)
        self.label_subtitle.setGeometry(QtCore.QRect(36, 30, 358, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_subtitle.setFont(font)
        self.label_subtitle.setTextFormat(QtCore.Qt.AutoText)
        self.label_subtitle.setAlignment(QtCore.Qt.AlignCenter)
        self.label_subtitle.setObjectName("label_subtitle")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(0, 100, 430, 239))
        self.frame_2.setMinimumSize(QtCore.QSize(430, 239))
        self.frame_2.setMaximumSize(QtCore.QSize(430, 239))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.tabWidget = QtWidgets.QTabWidget(self.frame_2)
        self.tabWidget.setGeometry(QtCore.QRect(24, 14, 381, 171))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayoutWidget_16 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_16.setGeometry(QtCore.QRect(24, 18, 101, 108))
        self.verticalLayoutWidget_16.setObjectName("verticalLayoutWidget_16")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_16)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setSpacing(10)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_22 = QtWidgets.QLabel(self.verticalLayoutWidget_16)
        self.label_22.setMinimumSize(QtCore.QSize(0, 28))
        self.label_22.setMaximumSize(QtCore.QSize(16777215, 28))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_22.setFont(font)
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")
        self.verticalLayout_16.addWidget(self.label_22)
        self.label_23 = QtWidgets.QLabel(self.verticalLayoutWidget_16)
        self.label_23.setMinimumSize(QtCore.QSize(0, 28))
        self.label_23.setMaximumSize(QtCore.QSize(16777215, 28))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_23.setFont(font)
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.verticalLayout_16.addWidget(self.label_23)
        self.label_21 = QtWidgets.QLabel(self.verticalLayoutWidget_16)
        self.label_21.setMinimumSize(QtCore.QSize(0, 28))
        self.label_21.setMaximumSize(QtCore.QSize(16777215, 28))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_21.setFont(font)
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.verticalLayout_16.addWidget(self.label_21)
        self.verticalLayoutWidget_17 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_17.setGeometry(QtCore.QRect(144, 18, 125, 108))
        self.verticalLayoutWidget_17.setObjectName("verticalLayoutWidget_17")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_17)
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_17.setSpacing(10)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.lineEdit_min = QtWidgets.QLineEdit(self.verticalLayoutWidget_17)
        self.lineEdit_min.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_min.setMaximumSize(QtCore.QSize(16777215, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lineEdit_min.setFont(font)
        self.lineEdit_min.setStyleSheet("color: rgb(0, 0, 255);")
        self.lineEdit_min.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_min.setObjectName("lineEdit_min")
        self.verticalLayout_17.addWidget(self.lineEdit_min)
        self.lineEdit_max = QtWidgets.QLineEdit(self.verticalLayoutWidget_17)
        self.lineEdit_max.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_max.setMaximumSize(QtCore.QSize(16777215, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lineEdit_max.setFont(font)
        self.lineEdit_max.setStyleSheet("color: rgb(0, 0, 255);")
        self.lineEdit_max.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_max.setObjectName("lineEdit_max")
        self.verticalLayout_17.addWidget(self.lineEdit_max)
        self.lineEdit_step = QtWidgets.QLineEdit(self.verticalLayoutWidget_17)
        self.lineEdit_step.setMinimumSize(QtCore.QSize(0, 28))
        self.lineEdit_step.setMaximumSize(QtCore.QSize(16777215, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lineEdit_step.setFont(font)
        self.lineEdit_step.setStyleSheet("color: rgb(0, 0, 255);")
        self.lineEdit_step.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_step.setObjectName("lineEdit_step")
        self.verticalLayout_17.addWidget(self.lineEdit_step)
        self.verticalLayoutWidget_18 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_18.setGeometry(QtCore.QRect(282, 18, 61, 108))
        self.verticalLayoutWidget_18.setObjectName("verticalLayoutWidget_18")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_18)
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_18.setSpacing(10)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.label_24 = QtWidgets.QLabel(self.verticalLayoutWidget_18)
        self.label_24.setMinimumSize(QtCore.QSize(0, 28))
        self.label_24.setMaximumSize(QtCore.QSize(16777215, 28))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_24.setFont(font)
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setObjectName("label_24")
        self.verticalLayout_18.addWidget(self.label_24)
        self.label_25 = QtWidgets.QLabel(self.verticalLayoutWidget_18)
        self.label_25.setMinimumSize(QtCore.QSize(0, 28))
        self.label_25.setMaximumSize(QtCore.QSize(16777215, 28))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_25.setFont(font)
        self.label_25.setAlignment(QtCore.Qt.AlignCenter)
        self.label_25.setObjectName("label_25")
        self.verticalLayout_18.addWidget(self.label_25)
        self.label_26 = QtWidgets.QLabel(self.verticalLayoutWidget_18)
        self.label_26.setMinimumSize(QtCore.QSize(0, 28))
        self.label_26.setMaximumSize(QtCore.QSize(16777215, 28))
        font = QtGui.QFont()
        font.setItalic(False)
        self.label_26.setFont(font)
        self.label_26.setAlignment(QtCore.Qt.AlignCenter)
        self.label_26.setObjectName("label_26")
        self.verticalLayout_18.addWidget(self.label_26)
        self.tabWidget.addTab(self.tab_2, "")
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(28, 6, 101, 61))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_8 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_5.addWidget(self.label_8)
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(28, 74, 101, 61))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_9 = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_6.addWidget(self.label_9)
        self.verticalLayoutWidget_7 = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(128, 6, 52, 60))
        self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_10 = QtWidgets.QLabel(self.verticalLayoutWidget_7)
        self.label_10.setMinimumSize(QtCore.QSize(50, 26))
        self.label_10.setMaximumSize(QtCore.QSize(50, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_7.addWidget(self.label_10)
        self.label_11 = QtWidgets.QLabel(self.verticalLayoutWidget_7)
        self.label_11.setMinimumSize(QtCore.QSize(50, 26))
        self.label_11.setMaximumSize(QtCore.QSize(50, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_7.addWidget(self.label_11)
        self.verticalLayoutWidget_8 = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(128, 74, 52, 60))
        self.verticalLayoutWidget_8.setObjectName("verticalLayoutWidget_8")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_13 = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        self.label_13.setMinimumSize(QtCore.QSize(50, 26))
        self.label_13.setMaximumSize(QtCore.QSize(50, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_8.addWidget(self.label_13)
        self.label_12 = QtWidgets.QLabel(self.verticalLayoutWidget_8)
        self.label_12.setMinimumSize(QtCore.QSize(50, 26))
        self.label_12.setMaximumSize(QtCore.QSize(50, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_8.addWidget(self.label_12)
        self.verticalLayoutWidget_9 = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget_9.setGeometry(QtCore.QRect(188, 6, 101, 61))
        self.verticalLayoutWidget_9.setObjectName("verticalLayoutWidget_9")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_9)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(3)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.lineEdit_av = QtWidgets.QLineEdit(self.verticalLayoutWidget_9)
        self.lineEdit_av.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_av.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lineEdit_av.setFont(font)
        self.lineEdit_av.setStyleSheet("color: rgb(0, 0, 255);")
        self.lineEdit_av.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_av.setObjectName("lineEdit_av")
        self.verticalLayout_9.addWidget(self.lineEdit_av)
        self.lineEdit_bv = QtWidgets.QLineEdit(self.verticalLayoutWidget_9)
        self.lineEdit_bv.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_bv.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lineEdit_bv.setFont(font)
        self.lineEdit_bv.setStyleSheet("color: rgb(0, 0, 255);")
        self.lineEdit_bv.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_bv.setObjectName("lineEdit_bv")
        self.verticalLayout_9.addWidget(self.lineEdit_bv)
        self.verticalLayoutWidget_10 = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget_10.setGeometry(QtCore.QRect(292, 4, 61, 63))
        self.verticalLayoutWidget_10.setObjectName("verticalLayoutWidget_10")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_10)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_15 = QtWidgets.QLabel(self.verticalLayoutWidget_10)
        self.label_15.setMinimumSize(QtCore.QSize(0, 26))
        self.label_15.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_10.addWidget(self.label_15)
        self.label_14 = QtWidgets.QLabel(self.verticalLayoutWidget_10)
        self.label_14.setMinimumSize(QtCore.QSize(0, 26))
        self.label_14.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_10.addWidget(self.label_14)
        self.verticalLayoutWidget_11 = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget_11.setGeometry(QtCore.QRect(292, 74, 61, 60))
        self.verticalLayoutWidget_11.setObjectName("verticalLayoutWidget_11")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_11)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_16 = QtWidgets.QLabel(self.verticalLayoutWidget_11)
        self.label_16.setMinimumSize(QtCore.QSize(0, 26))
        self.label_16.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_11.addWidget(self.label_16)
        self.label_17 = QtWidgets.QLabel(self.verticalLayoutWidget_11)
        self.label_17.setMinimumSize(QtCore.QSize(0, 26))
        self.label_17.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_11.addWidget(self.label_17)
        self.verticalLayoutWidget_12 = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget_12.setGeometry(QtCore.QRect(188, 74, 101, 61))
        self.verticalLayoutWidget_12.setObjectName("verticalLayoutWidget_12")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_12)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setSpacing(3)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.lineEdit_ah = QtWidgets.QLineEdit(self.verticalLayoutWidget_12)
        self.lineEdit_ah.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_ah.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lineEdit_ah.setFont(font)
        self.lineEdit_ah.setStyleSheet("color: rgb(0, 0, 255);")
        self.lineEdit_ah.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_ah.setObjectName("lineEdit_ah")
        self.verticalLayout_12.addWidget(self.lineEdit_ah)
        self.lineEdit_bh = QtWidgets.QLineEdit(self.verticalLayoutWidget_12)
        self.lineEdit_bh.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit_bh.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lineEdit_bh.setFont(font)
        self.lineEdit_bh.setStyleSheet("color: rgb(0, 0, 255);")
        self.lineEdit_bh.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_bh.setObjectName("lineEdit_bh")
        self.verticalLayout_12.addWidget(self.lineEdit_bh)
        self.tabWidget.addTab(self.widget, "")
        self.pushButton_confirm_close = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_confirm_close.setGeometry(QtCore.QRect(40, 196, 161, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pushButton_confirm_close.setFont(font)
        self.pushButton_confirm_close.setObjectName("pushButton_confirm_close")
        self.pushButton_confirm_run_analysis = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_confirm_run_analysis.setGeometry(QtCore.QRect(226, 196, 161, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pushButton_confirm_run_analysis.setFont(font)
        self.pushButton_confirm_run_analysis.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.pushButton_confirm_run_analysis.setObjectName("pushButton_confirm_run_analysis")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 60, 430, 41))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(1)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(24, 8, 381, 27))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Harmonic analysis setup"))
        self.label_title.setText(_translate("Dialog", "Harmonic Analysis - Structural"))
        self.label_subtitle.setText(_translate("Dialog", "Direct Method"))
        self.label_22.setText(_translate("Dialog", "Freq min:"))
        self.label_23.setText(_translate("Dialog", "Freq max:"))
        self.label_21.setText(_translate("Dialog", "df:"))
        self.label_24.setText(_translate("Dialog", "[Hz]"))
        self.label_25.setText(_translate("Dialog", "[Hz]"))
        self.label_26.setText(_translate("Dialog", "[Hz]"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Frequency Setup"))
        self.label_8.setText(_translate("Dialog", "Proportional\n"
"viscous"))
        self.label_9.setText(_translate("Dialog", "Proportional\n"
"hysteretic"))
        self.label_10.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">α</span><span style=\" font-size:10pt; vertical-align:sub;\">v</span><span style=\" font-size:10pt;\">:</span></p></body></html>"))
        self.label_11.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">β</span><span style=\" font-size:10pt; vertical-align:sub;\">v</span><span style=\" font-size:10pt;\">:</span></p></body></html>"))
        self.label_13.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">α</span><span style=\" font-size:10pt; vertical-align:sub;\">h</span><span style=\" font-size:10pt;\">:</span></p></body></html>"))
        self.label_12.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">β</span><span style=\" font-size:10pt; vertical-align:sub;\">h</span><span style=\" font-size:10pt;\">:</span></p></body></html>"))
        self.label_15.setText(_translate("Dialog", "[1/s]"))
        self.label_14.setText(_translate("Dialog", "[s]"))
        self.label_16.setText(_translate("Dialog", "[1/s²]"))
        self.label_17.setText(_translate("Dialog", "[-]"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), _translate("Dialog", "Structural damping"))
        self.pushButton_confirm_close.setText(_translate("Dialog", "Confirm and Close"))
        self.pushButton_confirm_run_analysis.setText(_translate("Dialog", "Run analysis"))
        self.label.setText(_translate("Dialog", "ANALYSIS SETUP"))
