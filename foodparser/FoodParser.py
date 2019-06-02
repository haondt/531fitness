import os.path
import pickle
from SuperStoreParser import Parser as ssParser
from SheetsController import SheetsController
def main():

	# Set up configuration file paths
	sheetId = ""
	with open('secret/sheetId.txt') as sheet:
		sheetId = sheet.read().strip()
	tokenPath = 'secret/token.pickle'
	credPath = 'secret/credentials.json'

	# Build sheetsController
	sheet = SheetsController(tokenPath, credPath, sheetId)


	# Build list of headers
	headers = [
		'Food',
		'MFP Name',
		'Verified',
		'Link',
		'Unit',
		'Buying Quantity',
		'Buying Cost',
		'Serving Quantity',
		'$ / unit',
		'Serving Calories',
		'Serving Fat',
		'Serving Carbs',
		'Serving Protein',
		'g Protein / Calorie',
		'g Protein / $',
		'Protein Score',
		'Normalized Protein Score',
		'g Carbs / $',
		'g Fat / $',
		'Calories / $'
	]


	# Fill in headers
	sheet.makeHeaders(headers)


	# Build superstore parser
	url = 'https://www.realcanadiansuperstore.ca/Food/Bakery/Packaged-Breads/White%2C-Wheat-%26-Grain/Old-Mill-100%25-Whole-Wheat-Bread/p/20801296_EA'
	cachePath = 'cache.pickle'
	
	ssp = ssParser()
	html = None

	if(not os.path.exists(cachePath)):
		html = ssp.gethtml(url)
		with open(cachePath, 'wb') as cache:
			pickle.dump(html, cache)
	else:
		with open(cachePath, 'rb') as cache:
			html = pickle.load(cache)
	
	data = ssp.parse(html, url)
	for key in data:
		print(key,':', data[key])


if __name__ == '__main__':
	main()
