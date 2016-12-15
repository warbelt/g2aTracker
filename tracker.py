import scrapper
import dataManager
import ui.trackerGui

def main():
    myScrapper = scrapper.scrapper()
    myDataManager = dataManager.dataManager()

    myDataManager.update(myScrapper)
    myDataManager.storeGamesData()

    myGUI = ui.trackerGui.trackerGui(myDataManager.storedData)

if __name__ == "__main__":
    main()
