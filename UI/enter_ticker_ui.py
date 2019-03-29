# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'enter_ticker.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class EnterTicker(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(821, 638)
        self.Ticker = QtWidgets.QLineEdit(Dialog)
        self.Ticker.setGeometry(QtCore.QRect(122, 290, 561, 41))
        self.Ticker.setObjectName("Ticker")

        self.Enter = QtWidgets.QLabel(Dialog)
        self.Enter.setGeometry(QtCore.QRect(260, 260, 261, 31))
        self.Enter.setObjectName("Enter")

        self.Launch = QtWidgets.QPushButton(Dialog)
        self.Launch.setGeometry(QtCore.QRect(340, 340, 113, 32))
        self.Launch.setObjectName("Launch")
        self.retranslateUi(Dialog)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Enter.setText(_translate("Dialog", "                          Enter a Ticker:"))
        self.Launch.setText(_translate("Dialog", "Launch"))
