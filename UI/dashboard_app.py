import sys
import alpha_vantage
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from PyQt5.QtWidgets import QDialog, QMessageBox, QInputDialog, QLineEdit, QApplication, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import matplotlib.pyplot as plt
from dashboard import *
from dashboard import *


class DashboardApp(QDialog):

    TIME_SERIES = TimeSeries(key='YJWXREJ7AXYQX6J7', output_format='pandas')
    SECTOR_PERFORMANCE = SectorPerformances(key='YJWXREJ7AXYQX6J7', output_format='pandas')
    TECH_INDICATORS = TechIndicators(key='YJWXREJ7AXYQX6J7', output_format='pandas')

    def __init__(self):
        super().__init__()
        self.dashboard = Dashboard()
        self.dashboard.setupUi(self)
        # self.setStyleSheet('background:red')
        self.dashboard.CompanyLogo.setIcon(QIcon('hflogo.png'))
        self.dashboard.CompanyLogo.setIconSize(QSize(361, 291))
        self.show()
        self.ticker = ''
        self.set_new_ticker()
        self.ticker = str(QInputDialog.getText(self, 'Hesiod Financial, LLC', "Enter a New Ticker", QLineEdit.Normal, "")[0])
        #self.dashboard.MacD.clicked.connect(self.macd)
        #self.dashboard.RSI.clicked.connect(self.rsi)
        #self.dashboard.MovAvg.clicked.connect(self.moving_average)
        #self.dashboard.BBands.clicked.connect(self.bollinger_bands)
        self.dashboard.NewTicker.clicked.connect(self.set_new_ticker)

    def macd(self):
        volume, meta = DashboardApp.TECH_INDICATORS.get_macd(self.ticker)
        self.dashboard.Graphic = volume
        self.dashboard.Graphic.plot()
        self.dashboard.Graphic.show()
        self.dashboard.GraphLabel.setText(f'MacD: {self.ticker}')

    def rsi(self):
        strength, meta = DashboardApp.TECH_INDICATORS.get_rsi(self.ticker)
        self.dashboard.Graphic = strength
        self.dashboard.Graphic.plot()
        self.dashboard.Graphic.show()
        self.dashboard.GraphLabel.setText(f'Relative Strength Index: {self.ticker}')

    def moving_average(self):
        ma, meta = DashboardApp.TECH_INDICATORS.get_wma(self.ticker)
        self.dashboard.Graphic = ma
        self.dashboard.Graphic.plot()
        self.dashboard.Graphic.show()
        self.dashboard.GraphLabel.setText(f'Weighted Moving Average: {self.ticker}')

    def bollinger_bands(self):
        bbands, meta = DashboardApp.TECH_INDICATORS.get_bbands(self.ticker)
        self.dashboard.Graphic = bbands
        self.dashboard.Graphic.plot()
        self.dashboard.Graphic.show()
        self.dashboard.GraphLabel.setText(f'Bollinger Bands: {self.ticker}')

    def set_new_ticker(self):
        # make it so the page refreshes
        new_ticker = self.dashboard.TickerSearch.text()
        self.ticker = new_ticker
        self.dashboard.Stock.setText(f'Current Stock: {new_ticker}')
        self.dashboard.Stock.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    symbol = DashboardApp()
    symbol.show()
    sys.exit(symbol.exec_())
