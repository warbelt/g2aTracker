import scrapper
import dataManager
import ui.trackerGui

def main():
    myScrapper = scrapper.scrapper()
    myDataManager = dataManager.dataManager()

    # scrappedData = myScrapper.scrap()
    storedData = myDataManager.loadGamesData()
    # myDataManager.update(storedData, scrappedData)
    # myDataManager.storeGamesData(storedData)

    myGUI = ui.trackerGui.trackerGui(storedData)


if __name__ == "__main__":
    main()
