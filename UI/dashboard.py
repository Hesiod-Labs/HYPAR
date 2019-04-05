# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dashboard.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Dashboard(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(820, 639)
        self.Graphic = QtWidgets.QGraphicsView(Dialog)
        self.Graphic.setGeometry(QtCore.QRect(450, 40, 341, 281))
        self.Graphic.setObjectName("Graphic")
        self.TickerSearch = QtWidgets.QLineEdit(Dialog)
        self.TickerSearch.setGeometry(QtCore.QRect(20, 50, 113, 21))
        self.TickerSearch.setObjectName("TickerSearch")
        self.Table = QtWidgets.QTableView(Dialog)
        self.Table.setGeometry(QtCore.QRect(-5, 450, 831, 192))
        self.Table.setObjectName("Table")
        self.NewTicker = QtWidgets.QPushButton(Dialog)
        self.NewTicker.setGeometry(QtCore.QRect(140, 50, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NewTicker.setFont(font)
        self.NewTicker.setObjectName("NewTicker")
        self.Stock = QtWidgets.QLabel(Dialog)
        self.Stock.setGeometry(QtCore.QRect(10, 390, 301, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.Stock.setFont(font)
        self.Stock.setText("")
        self.Stock.setObjectName("Stock")
        self.TickerLabel = QtWidgets.QLabel(Dialog)
        self.TickerLabel.setGeometry(QtCore.QRect(20, 30, 181, 20))
        self.TickerLabel.setObjectName("TickerLabel")
        self.GraphLabel = QtWidgets.QLabel(Dialog)
        self.GraphLabel.setGeometry(QtCore.QRect(450, 5, 191, 31))
        self.GraphLabel.setText("")
        self.GraphLabel.setObjectName("GraphLabel")
        self.CompanyLogo = QtWidgets.QPushButton(Dialog)
        self.CompanyLogo.setGeometry(QtCore.QRect(70, 100, 261, 291))
        self.CompanyLogo.setText("")
        self.CompanyLogo.setObjectName("CompanyLogo")
        self.GraphicCombos = QtWidgets.QComboBox(Dialog)
        self.GraphicCombos.setGeometry(QtCore.QRect(503, 330, 231, 41))
        self.GraphicCombos.setObjectName("GraphicCombos")
        self.GraphicCombos.addItem("")
        self.GraphicCombos.addItem("")
        self.GraphicCombos.addItem("")
        self.GraphicCombos.addItem("")
        self.GraphicCombos.addItem("")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.NewTicker.setText(_translate("Dialog", "Refresh"))
        self.TickerLabel.setText(_translate("Dialog", "Enter a new ticker:"))
        self.GraphicCombos.setItemText(0, _translate("Dialog", "Bollinger Bands"))
        self.GraphicCombos.setItemText(1, _translate("Dialog", "Moving Averages"))
        self.GraphicCombos.setItemText(2, _translate("Dialog", "LinReg"))
        self.GraphicCombos.setItemText(3, _translate("Dialog", "RSI"))
        self.GraphicCombos.setItemText(4, _translate("Dialog", "MACD"))


