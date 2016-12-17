import scrapper
import dataManager
import ui.trackerGui

def main():
    myScrapper = scrapper.scrapper()
    myDataManager = dataManager.dataManager(myScrapper)

    myDataManager.update()

    myGUI = ui.trackerGui.trackerGui(myDataManager)

if __name__ == "__main__":
    main()
