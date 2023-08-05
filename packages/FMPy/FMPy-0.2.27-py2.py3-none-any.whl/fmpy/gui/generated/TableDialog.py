# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\a\1\s\fmpy\gui\forms\TableDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TableDialog(object):
    def setupUi(self, TableDialog):
        TableDialog.setObjectName("TableDialog")
        TableDialog.resize(902, 561)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        TableDialog.setPalette(palette)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(TableDialog)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtWidgets.QSplitter(TableDialog)
        self.splitter.setStyleSheet("QSplitter::handle:horizontal {\n"
"    border-left: 1px solid #ccc;\n"
"}")
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.tableView = QtWidgets.QTableView(self.splitter)
        self.tableView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableView.setObjectName("tableView")
        self.frame = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, -1, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plotSettingsWidget = QtWidgets.QWidget(self.frame)
        self.plotSettingsWidget.setObjectName("plotSettingsWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.plotSettingsWidget)
        self.gridLayout_2.setContentsMargins(20, -1, -1, -1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.plotRowsRadioButton = QtWidgets.QRadioButton(self.plotSettingsWidget)
        self.plotRowsRadioButton.setObjectName("plotRowsRadioButton")
        self.gridLayout_2.addWidget(self.plotRowsRadioButton, 1, 0, 1, 1)
        self.plotColumnsRadioButton = QtWidgets.QRadioButton(self.plotSettingsWidget)
        self.plotColumnsRadioButton.setChecked(True)
        self.plotColumnsRadioButton.setObjectName("plotColumnsRadioButton")
        self.gridLayout_2.addWidget(self.plotColumnsRadioButton, 0, 0, 1, 1)
        self.firstColumnAsXAxisCheckBox = QtWidgets.QCheckBox(self.plotSettingsWidget)
        self.firstColumnAsXAxisCheckBox.setChecked(True)
        self.firstColumnAsXAxisCheckBox.setObjectName("firstColumnAsXAxisCheckBox")
        self.gridLayout_2.addWidget(self.firstColumnAsXAxisCheckBox, 0, 1, 1, 1)
        self.firstRowAsXAxisCheckBox = QtWidgets.QCheckBox(self.plotSettingsWidget)
        self.firstRowAsXAxisCheckBox.setEnabled(False)
        self.firstRowAsXAxisCheckBox.setChecked(True)
        self.firstRowAsXAxisCheckBox.setObjectName("firstRowAsXAxisCheckBox")
        self.gridLayout_2.addWidget(self.firstRowAsXAxisCheckBox, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.plotSettingsWidget)
        self.graphicsView = GraphicsLayoutWidget(self.frame)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.verticalLayout_2.addWidget(self.splitter)
        self.buttonBox = QtWidgets.QDialogButtonBox(TableDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(TableDialog)
        self.buttonBox.accepted.connect(TableDialog.accept)
        self.buttonBox.rejected.connect(TableDialog.reject)
        self.plotColumnsRadioButton.toggled['bool'].connect(self.firstColumnAsXAxisCheckBox.setEnabled)
        self.plotRowsRadioButton.toggled['bool'].connect(self.firstRowAsXAxisCheckBox.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(TableDialog)

    def retranslateUi(self, TableDialog):
        _translate = QtCore.QCoreApplication.translate
        self.plotRowsRadioButton.setText(_translate("TableDialog", "Plot Rows"))
        self.plotColumnsRadioButton.setText(_translate("TableDialog", "Plot Columns"))
        self.firstColumnAsXAxisCheckBox.setText(_translate("TableDialog", "first column as x-axis"))
        self.firstRowAsXAxisCheckBox.setText(_translate("TableDialog", "first row as x-axis"))
from pyqtgraph import GraphicsLayoutWidget
from . import icons_rc
