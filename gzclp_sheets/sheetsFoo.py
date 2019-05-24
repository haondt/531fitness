import pickle
import os.path
from SheetsController import SheetsController
from GZCLP import Gzclp

def main():

	# Set up configuration file paths
	sheetId = ""
	with open('secret/sheetId.txt') as sheet:
		sheetId = sheet.read().strip()
	tokenPath = 'secret/token.pickle'
	credPath = 'secret/credentials.json'
	cachePath = 'secret/dataCache.pickle'

	# Build sheetsController
	sheet = SheetsController(tokenPath, credPath, sheetId)
	
	# Build GZCLP controller
	gzclp = Gzclp([45,35,25,10,5,2.5], 45);
	
	values = None
	
	# Check if data is cached
	if (os.path.exists(cachePath)):
		# Load data from cache
		with open(cachePath, 'rb') as cache:
			values = pickle.load(cache)
	else:
		# Pull data from spreadsheet
		values = sheet.transform(sheet.get())
		
		# cache data
		with open(cachePath, 'wb') as cache:
			pickle.dump(values, cache)
	

	
	gzclp.addLift("Squat", [225,185,0],["T1", None, "T2", ""])
	#print(gzclp.dayLifts)
	
	print(gzclp.getWorkoutString(0))

	if not values:
		print('No data found.')
	else:
		print(values)
	

if __name__ == '__main__':
	main()
