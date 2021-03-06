# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SpectrumWindowClass.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1172, 310)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        Dialog.setFont(font)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(14)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_clear = QtWidgets.QPushButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.btn_clear.setFont(font)
        self.btn_clear.setObjectName("btn_clear")
        self.verticalLayout.addWidget(self.btn_clear)
        self.btn_close = QtWidgets.QPushButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.btn_close.setFont(font)
        self.btn_close.setObjectName("btn_close")
        self.verticalLayout.addWidget(self.btn_close)
        self.btn_save = QtWidgets.QPushButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.btn_save.setFont(font)
        self.btn_save.setObjectName("btn_save")
        self.verticalLayout.addWidget(self.btn_save)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 6, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Trebuchet MS")
        font.setPointSize(10)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setFlat(True)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setContentsMargins(0, 2, 0, -1)
        self.verticalLayout_4.setSpacing(16)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.rbtn_cm = QtWidgets.QRadioButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbtn_cm.sizePolicy().hasHeightForWidth())
        self.rbtn_cm.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.rbtn_cm.setFont(font)
        self.rbtn_cm.setText("")
        self.rbtn_cm.setObjectName("rbtn_cm")
        self.horizontalLayout_4.addWidget(self.rbtn_cm)
        self.cm_label = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cm_label.sizePolicy().hasHeightForWidth())
        self.cm_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.cm_label.setFont(font)
        self.cm_label.setObjectName("cm_label")
        self.horizontalLayout_4.addWidget(self.cm_label, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.rbtn_micron = QtWidgets.QRadioButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.rbtn_micron.setFont(font)
        self.rbtn_micron.setObjectName("rbtn_micron")
        self.verticalLayout_4.addWidget(self.rbtn_micron)
        self.rbtn_nm = QtWidgets.QRadioButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.rbtn_nm.setFont(font)
        self.rbtn_nm.setObjectName("rbtn_nm")
        self.verticalLayout_4.addWidget(self.rbtn_nm)
        self.rbtn_A = QtWidgets.QRadioButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.rbtn_A.setFont(font)
        self.rbtn_A.setObjectName("rbtn_A")
        self.verticalLayout_4.addWidget(self.rbtn_A)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 2, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.btn_filechoose = QtWidgets.QPushButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.btn_filechoose.setFont(font)
        self.btn_filechoose.setObjectName("btn_filechoose")
        self.verticalLayout_2.addWidget(self.btn_filechoose)
        self.label_file_selected = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.label_file_selected.setFont(font)
        self.label_file_selected.setObjectName("label_file_selected")
        self.verticalLayout_2.addWidget(self.label_file_selected)
        self.del_selected_file = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.del_selected_file.sizePolicy().hasHeightForWidth())
        self.del_selected_file.setSizePolicy(sizePolicy)
        self.del_selected_file.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.del_selected_file.setFont(font)
        self.del_selected_file.setObjectName("del_selected_file")
        self.verticalLayout_2.addWidget(self.del_selected_file)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.file_start = QtWidgets.QSpinBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.file_start.setFont(font)
        self.file_start.setMinimum(1)
        self.file_start.setMaximum(999)
        self.file_start.setObjectName("file_start")
        self.verticalLayout_5.addWidget(self.file_start)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.wlth_column = QtWidgets.QSpinBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.wlth_column.setFont(font)
        self.wlth_column.setMinimum(1)
        self.wlth_column.setObjectName("wlth_column")
        self.verticalLayout_5.addWidget(self.wlth_column)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_5.addWidget(self.label_6)
        self.ints_column = QtWidgets.QSpinBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.ints_column.setFont(font)
        self.ints_column.setMinimum(1)
        self.ints_column.setProperty("value", 2)
        self.ints_column.setObjectName("ints_column")
        self.verticalLayout_5.addWidget(self.ints_column)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_5.addWidget(self.label_7)
        self.separ_sign = QtWidgets.QPlainTextEdit(self.groupBox_2)
        self.separ_sign.setMaximumSize(QtCore.QSize(16777215, 32))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.separ_sign.setFont(font)
        self.separ_sign.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.separ_sign.setOverwriteMode(False)
        self.separ_sign.setObjectName("separ_sign")
        self.verticalLayout_5.addWidget(self.separ_sign)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.gridLayout_2.addLayout(self.verticalLayout_5, 0, 4, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 0, 3, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 0, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem6, 0, 5, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_2)
        self.verticalLayout_7.addWidget(self.groupBox_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.btn_filechoose, self.rbtn_A)
        Dialog.setTabOrder(self.rbtn_A, self.rbtn_cm)
        Dialog.setTabOrder(self.rbtn_cm, self.file_start)
        Dialog.setTabOrder(self.file_start, self.wlth_column)
        Dialog.setTabOrder(self.wlth_column, self.ints_column)
        Dialog.setTabOrder(self.ints_column, self.btn_clear)
        Dialog.setTabOrder(self.btn_clear, self.btn_close)
        Dialog.setTabOrder(self.btn_close, self.btn_save)
        Dialog.setTabOrder(self.btn_save, self.del_selected_file)
        Dialog.setTabOrder(self.del_selected_file, self.separ_sign)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Spectrum for convolution"))
        self.btn_clear.setText(_translate("Dialog", "Clear this form"))
        self.btn_close.setText(_translate("Dialog", "Close without change"))
        self.btn_save.setText(_translate("Dialog", "Validate and Close"))
        self.label_2.setText(_translate("Dialog", "Spectral unit"))
        self.cm_label.setText(_translate("Dialog", "cm-1"))
        self.rbtn_micron.setText(_translate("Dialog", "µm"))
        self.rbtn_nm.setText(_translate("Dialog", "nm"))
        self.rbtn_A.setText(_translate("Dialog", "Å"))
        self.label_3.setText(_translate("Dialog", "Choose a file with spectral data for the convolution"))
        self.btn_filechoose.setText(_translate("Dialog", "Choose the spectrum file"))
        self.label_file_selected.setText(_translate("Dialog", "no file selected"))
        self.del_selected_file.setText(_translate("Dialog", "Clear the selected file"))
        self.label_4.setText(_translate("Dialog", "Data starts at line"))
        self.label_5.setText(_translate("Dialog", "Wavelengths in column"))
        self.label_6.setText(_translate("Dialog", "Intensities in column"))
        self.label_7.setText(_translate("Dialog", "Columns separated by (Tab by default)"))
