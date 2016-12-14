import scrapper
import dataManager

if __name__ == "__main__":
	myScrapper = scrapper.scrapper()
	myDataManager = dataManager.dataManager()

	scrappedData = myScrapper.scrap()

	myDataManager.update(scrappedData)
	myDataManager.storeGamesData()
