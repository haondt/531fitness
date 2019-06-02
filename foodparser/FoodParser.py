import hashlib
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
	
	print("Building sheets controller...")
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
	# sheet.makeHeaders(headers)


	# Build superstore parser
	urls = ['https://www.realcanadiansuperstore.ca/Food/Bakery/Packaged-Breads/White%2C-Wheat-%26-Grain/Old-Mill-100%25-Whole-Wheat-Bread/p/20801296_EA',
	'https://www.realcanadiansuperstore.ca/Food/Meal-Kits-%26-Deli/Ready-Meals-%26-Sides/Salads/Greek-Feta-Dressing%2C-Pouch/p/20597966_EA?isPDPFlow=Y']

	cachePath = 'cache.pickle'
	
	print("Building SuperStoreParser...")
	ssp = ssParser()
	
	caching = True
	data = []
	
	for i in range(len(urls)):
		print('yoinking page and parsing data...(' + str(i+1) + '/'
			+ str(len(urls)) + ')')

		url = urls[i]
		html = None

		if caching:
			cachePath = hashlib.md5(url.encode()).hexdigest()
			if(not os.path.exists(cachePath)):
				html = ssp.gethtml(urls[0])
				with open(cachePath, 'wb') as cache:
					pickle.dump(html, cache)
			else:
				with open(cachePath, 'rb') as cache:
					html = pickle.load(cache)
		else:
			html = ssp.gethtml(url)

		data.append(ssp.parse(html,url))

	print('Writing to sheets...')
	
	# Insert items
	sheet.insertFoods(data)


if __name__ == '__main__':
	main()
