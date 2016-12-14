import urllib
import contextlib
import json


#Returns first appearance of a substring that is preceded by @before and followed by @after
#Utilized for extracting certain values from the unparsed html source
def getSubSBetween(source, before, after):
	return source.split(before)[1].split(after)[0]

#Manages tasks for scrapping www.g2a.com looking for prices
class scrapper:
	#Retrieves the title and product ID from the url passed as @url, returns them as an id:title pair
	def getGameTitleAndID(self, url):
		#Get raw html from url. Prices information is served asynchronously in a json so we use this to get the title and ID of the product, and url of said json
		with contextlib.closing(urllib.urlopen(url)) as handle:
			rawHTML = handle.read()

		# Extract title and pID from html
		sTitle = getSubSBetween(rawHTML, "<title>", " - G2A.COM") #Game title
		pID = getSubSBetween(rawHTML, "productID = ", ";") #internal ID used by g2a to identify each product. Neded in order to get the json url

		return {'title': sTitle, 'id': pID}

	#Retrieves the cheapest price available at the moment for a product given by it's @pID
	def getPrice(self, pID):
		#knowing the product's ID, I retrieve the json which contains all its marketplace details (seller,prices)
		with contextlib.closing(urllib.urlopen("https://www.g2a.com/marketplace/product/auctions/?id=" + pID)) as handle:
			json_object = json.loads(handle.read())

		#Since offers come unordered and we don't care about the seller, we extract every price and select the lowest one
		prices = []
		for seller in json_object['a'].values():
			#p is the value in selected (from cookies??) currency without sign. f is the value with sign, which is problematic with currencies with special characteres such as euro
			### TODO 
			### aknowledge different currencies
			prices.append(float(seller['p']))
		return min(prices)

	# Gets a list if product ids, @ids. Returns a dictionary with pairs: {id:price} for each game
	def scrap(self, ids):
		gamesData = {}

		for game in ids:
			gamesData[game] = self.getPrice(game)

		return gamesData
