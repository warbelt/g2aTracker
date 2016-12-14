from PyQt4 import QtGui
import gamesTableModel

#App's front tab. Displays basic data from tracked games
class mainWindow(QtGui.QMainWindow):
    def __init__(self, storedData):
        super(mainWindow, self).__init__()
        self.initUI(storedData)

    def initUI(self, storedData):
        #Main table with all the data
        self.gamesTable = QtGui.QTableView(self)
        self.myGamesTableModel = gamesTableModel.gamesTableModel(storedData)
        self.gamesTable.setModel(self.myGamesTableModel)
        self.gamesTable.setGeometry(50,100,800,300)

        self.setGeometry(300,300,900,600)
        self.setWindowTitle("g2aTracker")
        self.show()
