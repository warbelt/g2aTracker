import urllib
import contextlib
import json

#URLs of every game we want to check
urls = ["https://www.g2a.com/dishonored-game-of-the-year-edition-steam-cd-key-global.html",
		"https://www.g2a.com/dying-light-the-following-enhanced-edition-steam-cd-key-global.html",
		"https://www.g2a.com/keep-talking-and-nobody-explodes-steam-cd-key-global.html"]


#Returns first appearance of a substring that is preceded by @before and followed by @after
#Utilized for extracting certain values from the unparsed html source
def getSubSBetween(source, before, after):
	return source.split(before)[1].split(after)[0]


#Returns Title and cheapest price for a game located at @url
def getInfo(url):
	#Get raw html from url. Prices information is served asynchronously in a json so we use this to get the title of the game and the url of said json
	with contextlib.closing(urllib.urlopen(url)) as handle:
		html_content = handle.read()

	sTitle = getSubSBetween(html_content, "<title>", "</title>") #Game title
	pID = getSubSBetween(html_content, "productID = ", ";") #internal ID used by g2a to identify each product. Neded in order to get the json url

	#knowing the product's ID I retrieve the json which contains all its marketplace details (seller,prices)
	with contextlib.closing(urllib.urlopen("https://www.g2a.com/marketplace/product/auctions/?id=" + pID)) as handle:
		json_object = json.loads(handle.read())

	#Since offers come unordered and we don't care about the seller, we extract every price and select the lowest one
	prices = []
	for seller in json_object['a'].values():
		#p is the value in selected (from cookies??) currency without sign. f is the value with sign, which is problematic with currencies with special characteres such as euro
		prices.append(float(seller['p']))
	fLowestPrice = min(prices)

	return [sTitle,fLowestPrice]


if __name__ == "__main__":
	for game in urls:
		gameData = getInfo(game)
		print
		print "\t" + (gameData[0])
		print "\t" + (str(gameData[1]))
