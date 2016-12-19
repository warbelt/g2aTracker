from PyQt4 import QtGui, QtCore

# Max amount of price records to show at main table
olderPricesDisplayedMain = 3

class gamesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, dataManager, parent = None):
        QtCore.QAbstractTableModel.__init__(self,parent)
        self.dM = dataManager

    # Overloaded method inherited from QtCore.QAbstractTableModel
    # Returns number of rows of the model
    def rowCount(self , parent):
        return self.dM.getGamesDBLen()

    # Overloaded method inherited from QtCore.QAbstractTableModel
    # Returns number of columns of the model
    def columnCount(self, parent):
        # List the last @olderPricesDisplayedMain prices, plus two columns for name and difference of price
        return (2 + olderPricesDisplayedMain)

    # Overloaded method inherited from QtCore.QAbstractTableModel
    # Returns information needed by the view in order to draw the cell of the table situated at @index
    # See Qt docs for @role
    def data(self, index, role):
        row = index.row()
        column = index.column()

        gameID = self.dM.getGamesIDsList()[row]
        records = self.dM.getGameRecords(gameID)

        #Displaying data
        if role == QtCore.Qt.DisplayRole:
            # First column: game name
            if column == 0:
                value = self.dM.getGameTitle(gameID)
                return QtCore.QString(str(value))

            # Next @olderPricesDisplayedMain columns show older prices
            elif column in range(1, olderPricesDisplayedMain+1):
                olderPricesAvailable = len(records)
                # Check if there is enough data stored (older prices)
                if olderPricesAvailable >= (olderPricesDisplayedMain+1-column):
                    value = records[olderPricesAvailable - olderPricesDisplayedMain + column - 1]['price']
                    return QtCore.QString(str(value))
                else:
                    value = "-"
                    return QtCore.QString(str(value))

            # Last column shows price variation since last check (if there is data)
            elif column == (olderPricesDisplayedMain + 1):
                # Show nothing if there is not enough data (at least present and one past price)
                if len(records) < 2:
                    value = "-"
                    return QtCore.QString(str(value))
                # If there is enough data, show difference (absolute and relative value) between two last prices available
                else:
                    newPrice = records[len(records)-1]['price']
                    lastPrice = records[len(records)-2]['price']
                    absoluteDifference = newPrice - lastPrice
                    relativeDifference = absoluteDifference/lastPrice*100
                    value = str(absoluteDifference) + " (" + str(relativeDifference)[:3] + "%)"
                    return QtCore.QString(str(value))

        # Text alignment: Name aligned left, numeric data aligned right
        if role == QtCore.Qt.TextAlignmentRole:
            if column != 0:
                return QtCore.Qt.AlignRight

        # Text Color
        if role == QtCore.Qt.ForegroundRole:
            # For history of prices (intermediate columns): red if higher than previous, green if lower, default otherwise
            if column > 0 and column < (self.columnCount(parent = None) -1):
                # Check if there are enough records stored to compare
                if len(records) >= (self.columnCount(parent = None) - column):
                    pNewer = records[column - self.columnCount(parent = None) + 1]['price']
                    pOlder = records[column - self.columnCount(parent = None)]['price']
                    priceDifference =  pNewer - pOlder
                    if priceDifference < 0:
                        return QtGui.QBrush(QtCore.Qt.darkGreen)
                    elif priceDifference > 0:
                        return QtGui.QBrush(QtCore.Qt.red)
                    else:
                        return QtGui.QBrush(QtCore.Qt.black)
                # Paint black if there are not enough records to compare
                else:
                    return QtGui.QBrush(QtCore.Qt.black)

            # For price difference (last column): red if higher, green if lower, default otherwise
            if column == self.columnCount(parent = None) - 1:
                # At least two different records are needed in order to compare prices. If there aren't enough, paint black
                if len(records) < 2:
                    return QtGui.QBrush(QtCore.Qt.black)
                else:
                    newPrice = records[-1]['price']
                    lastPrice = records[-2]['price']
                    absoluteDifference = newPrice - lastPrice
                    if absoluteDifference > 0 :
                        return QtGui.QBrush(QtCore.Qt.red)
                    elif absoluteDifference < 0 :
                        return QtGui.QBrush(QtCore.Qt.darkGreen)
                    else:
                        return QtGui.QBrush(QtCore.Qt.black)
            # Every other column is black
            else:
                return QtGui.QBrush(QtCore.Qt.black)

        # Background color
        if role == QtCore.Qt.BackgroundRole:
            # Paint odd rows white, even rows grey
            if row % 2 == 0:
                return QtGui.QBrush(QtGui.QColor(220,220,220))

    # Overloaded method inherited from QtCore.QAbstractTableModel
    # Returns information needed by the view in order to draw header cells
    # See Qt docs           
    def headerData(self, section, orientation, role):
        # Displaying Data
        if role == QtCore.Qt.DisplayRole:
            # Only Horizontal header is displayed, vertical is hidden
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return QtCore.QString("Product name")
                if section == self.columnCount(self)-1:
                    return QtCore.QString("Price Variation")
        # Font Role
        if role == QtCore.Qt.FontRole:
            font = QtGui.QFont()
            font.setBold(True)
            return font

    # Calls dataManager to add product located at @url, passes result from dataManager.addNewGame: title of product if OK, else -1
    # dataManager handles validation
    def addNewGame(self, url):
        self.layoutAboutToBeChanged.emit()

        result = self.dM.addNewGame(url)

        # Emit signal to refresh table
        topLeft = self.createIndex(0,0)
        bottomRight = self.createIndex(self.rowCount(self), self.columnCount(self))

        self.dataChanged.emit(topLeft, bottomRight)
        self.layoutChanged.emit()
        return result

    # Calls dataManager to remove product at @row. dataManager handles validation
    def removeGame(self, row):
        self.dM.removeGame(row)

        # Emit signal to refresh table
        topLeft = self.createIndex(0,0)
        bottomRight = self.createIndex(self.rowCount(self), self.columnCount(self))

        self.dataChanged.emit(topLeft, bottomRight)

    # Calls dataManager to change the title of a product at @row to @newTitle
    def setGameTitle(self, row, newTitle):
        self.dM.setGameTitle(row, newTitle)

        topLeft = self.createIndex(row,0)
        bottomRight = self.createIndex(row, 0)

        self.dataChanged.emit(topLeft, bottomRight)

    def getGameUrl(self, row):
        return self.dM.getGameUrl(self.dM.getGamesIDsList()[row])
