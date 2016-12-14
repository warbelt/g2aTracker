import sys
from PyQt4 import QtGui
import scrapper
import dataManager
import ui.mainWindow

def main():
    myScrapper = scrapper.scrapper()
    myDataManager = dataManager.dataManager()

    # scrappedData = myScrapper.scrap()
    storedData = myDataManager.loadGamesData()
    # myDataManager.update(storedData, scrappedData)
    # myDataManager.storeGamesData(storedData)

    app = QtGui.QApplication(sys.argv)
    w = ui.mainWindow.mainWindow(storedData)  
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
