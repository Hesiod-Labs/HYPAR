import sys
import alpha_vantage
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget
import matplotlib.pyplot as plt
from main_page import *
from enter_ticker_ui import *


class DashboardApp(QDialog):

    TIME_SERIES = TimeSeries(key='YJWXREJ7AXYQX6J7', output_format='pandas')
    SECTOR_PERFORMANCE = SectorPerformances(key='YJWXREJ7AXYQX6J7', output_format='pandas')
    TECH_INDICATORS = TechIndicators(key='YJWXREJ7AXYQX6J7', output_format='pandas')

    def __init__(self, ticker):
        super().__init__()
        self.main_page = MainPage()
        self.main_page.setupUi(self)
        self.ticker =
        self.main_page.MacD.clicked.connect(self.macd)
        self.main_page.RSI.clicked.connect(self.rsi)
        self.main_page.MovAvg.clicked.connect(self.moving_average)
        self.main_page.BBands.clicked.connect(self.bollinger_bands)
        self.show()

    def macd(self):
        volume, meta = DashboardApp.TECH_INDICATORS.get_macd(self.ticker)
        self.main_page.Graphic = volume
        self.main_page.Graphic.plot()
        self.main_page.Graphic.show()
        self.main_page.GraphicLabel.setText(f'MacD: {self.ticker}')

    def rsi(self):
        strength, meta = DashboardApp.TECH_INDICATORS.get_rsi(self.ticker)
        self.main_page.Graphic = strength
        self.main_page.Graphic.plot()
        self.main_page.Graphic.show()
        self.main_page.GraphicLabel.setText(f'Relative Strength Index: {self.ticker}')

    def moving_average(self):
        ma, meta = DashboardApp.TECH_INDICATORS.get_wma(self.ticker)
        self.main_page.Graphic = ma
        self.main_page.Graphic.plot()
        self.main_page.Graphic.show()
        self.main_page.GraphicLabel.setText(f'Weighted Moving Average: {self.ticker}')

    def bollinger_bands(self):
        bbands, meta = DashboardApp.TECH_INDICATORS.get_bbands(self.ticker)
        self.main_page.Graphic = bbands
        self.main_page.Graphic.plot()
        self.main_page.Graphic.show()
        self.main_page.GraphicLabel.setText(f'Bollinger Bands: {self.ticker}')
