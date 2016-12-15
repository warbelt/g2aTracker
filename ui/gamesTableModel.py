from PyQt4 import QtGui, QtCore

# Max amount of price records to show at main table
olderPricesDisplayedMain = 3

class gamesTableModel(QtCore.QAbstractTableModel):
    def __init__(self, dataManager, parent = None):
        QtCore.QAbstractTableModel.__init__(self,parent)
        self.dM = dataManager

    def rowCount(self , parent):
        return self.dM.getGamesDBLen()

    def columnCount(self, parent):
        # List the last @olderPricesDisplayedMain prices, plus name and difference of price
        return (2 + olderPricesDisplayedMain)

    def data(self,index,role):
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
                #if there is enough data stored (older prices)
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
            # For price difference (last column): red if higher, green if lower, default otherwise
            if column == self.columnCount(parent = None) - 1:
                if len(records) < 2:
                    return QtGui.QBrush(QtCore.Qt.black)
                else:
                    newPrice = records[len(records)-1]['price']
                    lastPrice = records[len(records)-2]['price']
                    absoluteDifference = newPrice - lastPrice
                    if absoluteDifference > 0 :
                        return QtGui.QBrush(QtCore.Qt.red)
                    elif absoluteDifference < 0 :
                        return QtGui.QBrush(QtCore.Qt.green)
                    else:
                        return QtGui.QBrush(QtCore.Qt.black)
            # Every other column is black
            else:
                return QtGui.QBrush(QtCore.Qt.black)
