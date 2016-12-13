import time
import json
gamesDataFile = "data/gamesdata.gtd"


#Manages tasks revolving saving, updating and storing games data
class dataManager:

	#loads stored data from previous sessions, parsed from JSON to dictionary
	def loadGamesData(self):
		try: 
			f = open(gamesDataFile, 'r')
			storedData = json.load(f)
			f.close()

		except IOError:
			print("No prior data was found")
			storedData = {}

		return storedData

	#Takes 2 dictionaries: @stored is the previous data stored in gamesdata.gtd, @scrapped is the new data scrapped from g2a.com
	#Returns updates @stored based on @scrapped, in which games with prior records have been added the new data, and games without prior records have been added
	def update(self, stored, scrapped):
		for game in scrapped:
			#if there is no prior data from this game, it must be added to the stored dictionary
			if game not in stored.keys():
				newGame = {'title': scrapped[game]['title'], 'records': []}
				stored[game] = newGame

			#then the new record can be added
			record = {'dateAndTime': time.strftime("%c"), 'price': scrapped[game]['price']}
			stored[game]['records'].append(record)

	#Writes @data formated as JSON to a file
	def storeGamesData(self, data):
		try: 
			f = open(gamesDataFile, 'w')
			f.write(json.dumps(data))
			f.close()

		except IOError:
			print("Could not save data to 'gamesdata.gtd'")
