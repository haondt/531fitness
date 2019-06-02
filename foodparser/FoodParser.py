import hashlib
import os.path
import sys
import pickle
from SuperStoreParser import Parser as ssParser
from SheetsController import SheetsController
def main():
	if (len(sys.argv) != 2):
		print("usage: python3 FoodParser.py inputfile.txt")
		return
	if (not os.path.exists(sys.argv[1])):
		print("Could not find file \"" + sys.argv[1] + "\"")
		return

	
	urls = []
	with open(sys.argv[1]) as urlFile:
		urls = [i.strip() for i in urlFile.readlines()]

	# Set up configuration file paths
	sheetId = ""
	with open('secret/sheetId.txt') as sheet:
		sheetId = sheet.read().strip()
	tokenPath = 'secret/token.pickle'
	credPath = 'secret/credentials.json'
	





	
	# Build superstore parser
	print("Building SuperStoreParser...")
	ssp = ssParser()

	caching = True
	debugging = True
	data = []
	
	for i in range(len(urls)):
		print('yoinking page and parsing data...(' + str(i+1) + '/'
			+ str(len(urls)) + ')')

		url = urls[i]
		html = None

		if caching:
			cachePath = 'cache/'
			cachePath += hashlib.md5(url.encode()).hexdigest()
			cachePath += '.pickle'
			if(not os.path.exists(cachePath)):
				html = ssp.gethtml(url)
				with open(cachePath, 'wb') as cache:
					pickle.dump(html, cache)
			else:
				with open(cachePath, 'rb') as cache:
					html = pickle.load(cache)
		else:
			html = ssp.gethtml(url)

		if debugging:
			data.append(ssp.parse(html,url))
		else:
			try:
				data.append(ssp.parse(html,url))
			except:
				#print("Error in parsing data (" + url[35:85] + "...)")
				print("Error in parsing data")
				print("URL:", url)
	
	ssp.closeWindow()

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

	# Clear out sheet
	sheet.clearSheet()


	# Fill in headers
	sheet.makeHeaders(headers)

	print('Writing to sheets...')
	# Insert items
	sheet.insertFoods(data)


if __name__ == '__main__':
	main()
