import scrapper
import dataManager

if __name__ == "__main__":
	myScrapper = scrapper.scrapper()
	myDataManager = dataManager.dataManager()

	scrappedData = myScrapper.scrap()
	storedData = myDataManager.loadGamesData()
	myDataManager.update(storedData, scrappedData)
	myDataManager.storeGamesData(storedData)