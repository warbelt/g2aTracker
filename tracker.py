import scrapper
import dataManager

if __name__ == "__main__":
	myScrapper = scrapper.scrapper()
	myDataManager = dataManager.dataManager()

	myDataManager.update(myScrapper)
	myDataManager.storeGamesData()
