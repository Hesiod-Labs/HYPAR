# this will be the application that controls the ticker get commands

from enter_ticker_ui import *
from main_page import *
from main_app import *


class TickerUI(QDialog):

    def __init__(self):
        super().__init__()
        self.ticker_ui = EnterTicker()
        self.ticker_ui.setupUi(self)
        self.show()
        self.ticker_ui.Launch.clicked.connect(self.ticker_entered)
        self.dashboard = ''

    def ticker_entered(self):
        self.dashboard = DashboardApp(self.ticker_ui.Ticker.text())
        self.dashboard.show()
        self.destroy()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    symbol = TickerUI()
    symbol.show()
    sys.exit(symbol.exec_())

