from View.ViewConsole import ViewConsole
from View.ViewBoard import ViewBoard
from Model.DataBoard import DataBoard
from Model.DictionaryAndList import DictionaryAndList
from PyQt5.QtWidgets import QMainWindow, QTabWidget
from PyQt5 import uic
import os

MainWindowPath = os.path.dirname(os.path.realpath(__file__)) + '/ui{}MainWindow.ui'.format(os.sep)
Ui_MainWindow, QtBaseClass = uic.loadUiType(MainWindowPath)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.createsComponentsAndPointers()
        self.setupWindowTabs()

    def setupWindowTabs(self):
        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)
        self.tabWidget.addTab(self.boardView, "Board")
        self.tabWidget.addTab(self.consoleView, "Console")

    def createsComponentsAndPointers(self):
        dataBoard = DataBoard()
        dicoAndList = DictionaryAndList().returnInfos()
        # Components
        self.boardView = ViewBoard(dataBoard, dicoAndList)
        self.consoleView = ViewConsole()
