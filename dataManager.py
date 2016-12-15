import time
import json
gamesDataFile = "data/gamesdata.gtd"


# Manages tasks revolving saving, updating and storing games data
class dataManager:
	def __init__(self):
		self.storedData = self.loadGamesData()

	# loads stored data from previous sessions, parsed from JSON to dictionary
	def loadGamesData(self):
		data = {}

		try: 
			f = open(gamesDataFile, 'r')
			try:
				data = json.load(f)
			except:
				pass
			f.close()

		except IOError:
			print("No prior data was found")

		return data

	# Takes @scrapper: scrapper object created in main function
	# Updates @self.storedData with data retrieved by @scrapper, in which games with prior records have been added the new data, and games without prior records have been added
	def update(self, scrapper):
		scrapped = scrapper.scrap(self.getGamesIDsList())

		for game in scrapped:
			# Only the last price retrieved each day is stored. If there is already an stored price from the present day, it is overwritten
			date = time.strftime("%x")

			# If the last record is from this day, it's price is overwritten
			if len(self.storedData[game]['records']) > 0:
				if self.storedData[game]['records'][-1]['dateAndTime'] == date : 
					self.storedData[game]['records'][-1]['price'] = scrapped[game]

				else:
					record = {'dateAndTime': date, 'price': scrapped[game]}
					self.storedData[game]['records'].append(record)
			else:
				record = {'dateAndTime': date, 'price': scrapped[game]}
				self.storedData[game]['records'].append(record)

	# Writes @self.storedData formated as JSON to a file
	def storeGamesData(self):
		try: 
			f = open(gamesDataFile, 'w')
			f.write(json.dumps(self.storedData))
			f.close()

		except IOError:
			print("Could not save data to 'gamesdata.gtd'")

	# Returns a list of the IDs of every game in @self.storedData
	def getGamesIDsList(self):
		return self.storedData.keys()

	# @url is the address of the product to keep track of. dataManager adds the new product with a fresh record to its dictionary
	def addNewGame(self, scrapper, url):
		titleAndId = scrapper.getGameTitleAndID(url)
		price = scrapper.getPrice(titleAndId['id'])

		record = {'dateAndTime' : time.strftime("%x"), 'price' : price}

		# Check first if the game is already being tracked, if it is not, then add it to the dictionary
		if titleAndId['id'] not in self.storedData.keys():
			self.storedData[titleAndId['id']] = {'title' : titleAndId['title'], 'records' : [record]}
