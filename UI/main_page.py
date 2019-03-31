# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_page.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class MainPage(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(820, 639)
        self.Graphic = QtWidgets.QGraphicsView(Dialog)
        self.Graphic.setGeometry(QtCore.QRect(470, 90, 321, 311))
        self.Graphic.setObjectName("Graphic")

        self.GraphicLabel = QtWidgets.QLabel(Dialog)
        self.GraphicLabel.setGeometry(QtCore.QRect(509, 56, 161, 21))
        self.GraphicLabel.setText("")
        self.GraphicLabel.setObjectName("GraphicLabel")

        self.TickerSearch = QtWidgets.QLineEdit(Dialog)
        self.TickerSearch.setGeometry(QtCore.QRect(30, 30, 113, 21))
        self.TickerSearch.setObjectName("TickerSearch")

        self.MacD = QtWidgets.QPushButton(Dialog)
        self.MacD.setGeometry(QtCore.QRect(340, 210, 121, 32))
        self.MacD.setObjectName("MacD")

        self.RSI = QtWidgets.QPushButton(Dialog)
        self.RSI.setGeometry(QtCore.QRect(340, 250, 121, 32))
        self.RSI.setObjectName("RSI")

        self.BBands = QtWidgets.QPushButton(Dialog)
        self.BBands.setGeometry(QtCore.QRect(340, 290, 121, 32))
        self.BBands.setObjectName("BBands")

        self.MovAvg = QtWidgets.QPushButton(Dialog)
        self.MovAvg.setGeometry(QtCore.QRect(340, 330, 121, 32))
        self.MovAvg.setObjectName("MovAvg")

        self.Table = QtWidgets.QTableView(Dialog)
        self.Table.setGeometry(QtCore.QRect(-5, 450, 831, 192))
        self.Table.setObjectName("Table")

        self.NewTicker = QtWidgets.QPushButton(Dialog)
        self.NewTicker.setGeometry(QtCore.QRect(30, 50, 113, 32))
        self.NewTicker.setObjectName("NewTicker")

        self.Stock = QtWidgets.QLabel(Dialog)
        self.Stock.setGeometry(QtCore.QRect(50, 200, 191, 61))
        self.Stock.setText("")
        self.Stock.setObjectName("Stock")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.MacD.setText(_translate("Dialog", "MacD"))
        self.RSI.setText(_translate("Dialog", "RSI"))
        self.BBands.setText(_translate("Dialog", "Bollinger Bands"))
        self.MovAvg.setText(_translate("Dialog", "Moving Average"))
        self.NewTicker.setText(_translate("Dialog", "New Ticker:"))


