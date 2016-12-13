import urllib
import contextlib
import json
#URLs of every game we want to check
urls = ["https://www.g2a.com/dishonored-game-of-the-year-edition-steam-cd-key-global.html"
	,"https://www.g2a.com/dying-light-the-following-enhanced-edition-steam-cd-key-global.html"
	,"https://www.g2a.com/keep-talking-and-nobody-explodes-steam-cd-key-global.html"
	,"https://www.g2a.com/dragon-age-origins-ultimate-edition-origin-cd-key-global.html"
	,"https://www.g2a.com/borderlands-goty-edition-steam-cd-key-global.html"
	,"https://www.g2a.com/sid-meier-s-civilization-vi-steam-cd-key-preorder-row-1.html"
	]


#Returns first appearance of a substring that is preceded by @before and followed by @after
#Utilized for extracting certain values from the unparsed html source
def getSubSBetween(source, before, after):
	return source.split(before)[1].split(after)[0]

#Manages tasks for scrapping www.g2a.com looking for prices
class scrapper:
	#Retrieves the title and product ID from the raw html passed as @source, returns them as an id:title pair
	def getGameTitleAndID(self, source):
		sTitle = getSubSBetween(source, "<title>", "</title>") #Game title
		pID = getSubSBetween(source, "productID = ", ";") #internal ID used by g2a to identify each product. Neded in order to get the json url

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

	#Returns a dictionary @gamesData comprising, for every game scraped: productID as key, and a dictionary with scrapped game data as value (Title and cheapest price)
	def scrap(self):
		gamesData = {}

		for url in urls:
			game = {}
			
			#Get raw html from url. Prices information is served asynchronously in a json so we use this to get the title and ID of the product, and url of said json
			with contextlib.closing(urllib.urlopen(url)) as handle:
				rawHTML = handle.read()
			gameTitleAndID = self.getGameTitleAndID(rawHTML)

			game['title'] = gameTitleAndID['title']
			game['price'] = self.getPrice(gameTitleAndID['id'])
			gamesData[gameTitleAndID['id']] = game

		return gamesData
