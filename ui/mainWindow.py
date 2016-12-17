from PyQt4 import QtGui, QtCore
import gamesTableModel

#App's front tab. Displays basic data from tracked games
class mainWindow(QtGui.QMainWindow):
    def __init__(self, dataManager):
        super(mainWindow, self).__init__()
        self.dataManager = dataManager
        self.initUI()

    def initUI(self):
        # Init main window items
        self.initGamesTable()
        self.initTextBoxUrl()
        self.initButtonAddGame()
        self.initButtonRemoveGame()

        # Connect buttons' clicked event to buttonClicled slot
        self.buttonAddGame.clicked.connect(self.buttonClicked)
        self.buttonRemoveGame.clicked.connect(self.buttonClicked)

        # Position and size
        self.setGeometry(300,300,900,600)
        # WIndow title
        self.setWindowTitle("g2aTracker")

        self.show()

    #Main table with all the data
    def initGamesTable(self):
        self.gamesTable = QtGui.QTableView(self)
        # Table model
        self.myGamesTableModel = gamesTableModel.gamesTableModel(self.dataManager)
        self.gamesTable.setModel(self.myGamesTableModel)

        # Vertical header: hidden
        self.gamesTable.verticalHeader().hide()

        # Selection Behavior: full rows
        # Selection Mode: single element
        self.gamesTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.gamesTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        # Set column width
        colCount = self.myGamesTableModel.columnCount(self.gamesTable.currentIndex())
        # Game name column
        self.gamesTable.setColumnWidth(0,400)
        # Prices history columns
        for col in range(1, colCount-1):
            self.gamesTable.setColumnWidth(col, 80)
        # Price variation column
        self.gamesTable.setColumnWidth(colCount-1, 137)

        # Position and size
        self.gamesTable.setGeometry(50,100,800,300)
        # Grid lines: hidden
        self.gamesTable.setShowGrid(False)
        # Scroll bar: show always
        self.gamesTable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

    # Text box for new item url
    def initTextBoxUrl(self):
        self.textBoxUrl = QtGui.QLineEdit(self)
        self.textBoxUrl.move(150, 450)
        self.textBoxUrl.setFixedWidth(400)

    # Add game button
    def initButtonAddGame(self):
        self.buttonAddGame = QtGui.QPushButton("Add new item", self)
        self.buttonAddGame.setFixedWidth(100)
        self.buttonAddGame.move(50,450)

    # Remove game button
    def initButtonRemoveGame(self):
        self.buttonRemoveGame = QtGui.QPushButton("Remove selected item", self)
        self.buttonRemoveGame.setFixedWidth(150)
        self.buttonRemoveGame.move(700,450)

    # Handles button clicks in main window
    def buttonClicked(self):
        sender = self.sender()
        if sender == self.buttonAddGame:
            self.buttonAddGameClicked()
        elif sender == self.buttonRemoveGame:
            self.buttonRemoveGameClicked()

    # Add game clicked
    def buttonAddGameClicked(self):
        url = str(self.textBoxUrl.text())

        # Check if there is enything to pass to model
        if url == "" or url == None:
            return -1

        # Call to model to add game to data storage
        result = self.myGamesTableModel.addNewGame(url)
        if result == -1:
            self.textBoxUrl.setText("Error")
        else:
            self.textBoxUrl.setText("Added" + result)

    # Remove game clicked
    def buttonRemoveGameClicked(self):
        try:
            # Get selected row
            row = self.gamesTable.selectedIndexes()[0].row()
        except:
            return
        # Confirmation dialog
        productName = self.myGamesTableModel.data(self.myGamesTableModel.index(row, 0), QtCore.Qt.DisplayRole)
        box = QtGui.QMessageBox(self)
        reply = box.question(self,
                            QtCore.QString("Remove product"),
                            QtCore.QString("Are you sure you want to stop tracking ").append(productName).append(QtCore.QString("?")),
                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            # Clear selection and call model to remove product
            self.gamesTable.clearSelection()
            self.myGamesTableModel.removeGame(row)
