import time
import json
gamesDataFile = "data/gamesdata.gtd"


# Manages tasks revolving saving, updating and storing games data
class dataManager:
	def __init__(self, scrapper):
		self.storedData = self.loadGamesData()
		self.scrapper = scrapper

	# returns stored data from previous sessions, parsed from JSON file to dictionary
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

	# Updates @self.storedData with data retrieved by @self.scrapper, 
	# games with prior records are updated with the new data, and games without prior records are added
	def update(self):
		scrapped = self.scrapper.scrap(self.getGamesIDsList())

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
			# If this is the first record for the day, store if directly
			else:
				record = {'dateAndTime': date, 'price': scrapped[game]}
				self.storedData[game]['records'].append(record)

		self.storeGamesData()

	# Writes @self.storedData formated as JSON to a file
	def storeGamesData(self):
		try: 
			f = open(gamesDataFile, 'w')
			f.write(json.dumps(self.storedData))
			f.close()

		except IOError:
			print("Could not save data to 'gamesdata.gtd'")

	# Returns amount of games stored in dictionary
	def getGamesDBLen(self):
		return len(self.storedData)

	# Returns a list of the IDs of every game in @self.storedData
	def getGamesIDsList(self):
		return self.storedData.keys()

	# @url is the address of the product to keep track of. dataManager adds the new product with a fresh record to its dictionary
	# Returns title of added game if successful, else returns -1
	def addNewGame(self, url):
		titleAndId = self.scrapper.getGameTitleAndID(url)

		# If url does not point to a valid product page, return -1
		if titleAndId == -1 :
			return -1

		price = self.scrapper.getPrice(titleAndId['id'])

		record = {'dateAndTime' : time.strftime("%x"), 'price' : price}
		# Check first if the game is already being tracked, if it is not, then add it to the dictionary
		if titleAndId['id'] not in self.storedData.keys():
			self.storedData[titleAndId['id']] = {'title' : titleAndId['title'], 'records' : [record]}

		# Save data to file after adding the product
		self.storeGamesData()

		return titleAndId['title']

	# Removes game whose id is situated at position @index in the keys list of the prudict data dictionary
	def removeGame(self, index):
		self.storedData.pop(self.getGamesIDsList()[index])
		# Save data to file after removing product
		self.storeGamesData()

	# Returns dict of all records stored for a game with id equal to @gameID
	def getGameRecords(self, gameID):
		return self.storedData[gameID]['records']

	# Returns title of product associated to @gameID
	def getGameTitle(self, gameID):
		return self.storedData[gameID]['title']
