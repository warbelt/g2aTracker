import time
import json
gamesDataFile = "data/gamesdata.gtd"


# Manages tasks revolving saving, updating and storing games data
class dataManager:
	def __init__(self):
		self.storedData = self.loadGamesData()

	# loads stored data from previous sessions, parsed from JSON to dictionary
	def loadGamesData(self):
		try: 
			f = open(gamesDataFile, 'r')
			data = json.load(f)
			f.close()

		except IOError:
			print("No prior data was found")
			data = {}

		return data

	# Takes a dictionary: @scrapped is the new data retrieved from g2a.com by scrapper class
	# Updates @self.storedData based on @scrapped, in which games with prior records have been added the new data, and games without prior records have been added
	def update(self, scrapped):
		for game in scrapped:
			#if there is no prior data from this game, it must be added to the stored dictionary
			if game not in self.storedData.keys():
				newGame = {'title': scrapped[game]['title'], 'records': []}
				self.storedData[game] = newGame

			# then the new record can be added
			# Only the last price retrieved each day is stored. If there is already an stored price from the present day, it is overwritten
			date = time.strftime("%x")

			# If the last record is from this day, it's price is overwritten
			if len(self.storedData[game]['records']) > 0:
				if self.storedData[game]['records'][-1]['dateAndTime'] == date : 
					self.storedData[game]['records'][-1]['price'] = scrapped[game]['price']

				else:
					record = {'dateAndTime': date, 'price': scrapped[game]['price']}
					self.storedData[game]['records'].append(record)
			else:
				record = {'dateAndTime': date, 'price': scrapped[game]['price']}
				self.storedData[game]['records'].append(record)

			

	# Writes @self.storedData formated as JSON to a file
	def storeGamesData(self):
		try: 
			f = open(gamesDataFile, 'w')
			f.write(json.dumps(self.storedData))
			f.close()

		except IOError:
			print("Could not save data to 'gamesdata.gtd'")
