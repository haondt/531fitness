import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class SheetsController:
	sheet = None
	sheetId = None

	def __init__(self, tokenPath, credentialsPath, sheetId):
		# if modifying these scopes, delete the file token.pickle
		SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
		
		creds = None
		# Retreive user's access and refresh tokens 
		if os.path.exists(tokenPath):
			with open(tokenPath, 'rb') as token:
				creds = pickle.load(token)
		
		# Create token file by letting the user log in
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(credentialsPath, SCOPES)
				creds = flow.run_local_server()
			# Save the credentials for the next run
			with open(tokenPath, 'wb') as token:
				pickle.dump(creds, token)

		service = build('sheets', 'v4', credentials=creds)
		self.sheet = service.spreadsheets()	
		self.sheetId = sheetId
	
	def get(self, sheetRange="Parameters"):
		result = self.sheet.values().get(spreadsheetId=self.sheetId, range=sheetRange).execute()
		return result.get('values', [])
	
	# Transforms the result into a form parseable to Gzclp
	def transform(self, data):
		titles = data[0]
		iterator = 1
		newdata = {'Lifts':{}, 'Day':0, 'Plates':[], 'Bar Weight':0.0}
		while titles[iterator] is not "":
			for row in data[1:]:
				if row[0] not in newdata['Lifts']:
					newdata['Lifts'][row[0]] = {}
				if len(row) >  iterator:
					newdata['Lifts'][row[0]][titles[iterator]] = row[iterator]
				else:
					newdata['Lifts'][row[0]][titles[iterator]] = ''
			iterator += 1
		
		iterator += 1
		while iterator < len(titles):
			title = titles[iterator]
			print(title)
			if title in newdata:
				if type(newdata[title]) == int:
					newdata[title] = int(data[1][iterator])
				elif type(newdata[title]) == float:
					newdata[title] = float(data[1][iterator])
				elif type(newdata[title]) == list:
					row = 1
					while len(data[row]) >= iterator:
						newdata[title].append(float(data[row][iterator]))
						row += 1
			iterator += 1

		return newdata

class Gzclp:
	day = 0
	plates = []
	bar_weight = 0
	warmup_reps = ['1x5', '1x5', '1x3']
	warmup_multipliers = [0.4, 0.5, 0.6]
	
	# day_lifts[day][tier]
	dayLifts = [{} for i in range(4)]
	
	# reps[stage][tier]
	reps = [
		["5x3", "3x10", "3x15+"],
		["6x2", "3x8", "n/a"],
		["10x1", "3x6", "n/a"]
	]
	
	# stages[lift][tier]
	# 0-indexed
	stages = {}

	# weights[lift][tier]
	# 0-indexed
	# 3 RM
	weights = {}

	# rests[tier]
	rests = [
		"3-5 min"
		"2-3 min"
		"60-90 sec"
	]

	def __init__(self, plates, bar_weight):
		self.plates = plates
		self.bar_weight = bar_weight

	def getDay(self):
		return self.day
	
	def setDay(self, day):
		if day > 4 or day < 0:
			return False
		else:
			self.day = day
			return True

	def helptext(self):
		return """
		How to test for new 5RM: 
		After warming up, start at last successful 5x3 weight and do 5 reps
		Add 5 lbs and repeat until unable to do 5 reps
		Last successful reps is 5RM

		Progression:
		Add 5 lbs to bench/ohp and 10 lbs to squat/DL T1 and T2 after each workout
		Add weight when you can do 25 reps on your AMRAP for T3

		Failure:
		Move to the next stage
		After stage 3, for T1, test for a new 5RM. Use 85% of that to restart cycle
		For T2, find the last weight you lifted using stage 1, add 15-20 lbs to this to restart cycle
		"""
	
	# Rounds a number to the precision of base
	def round(self, num, base):
		return round(base*round(float(num)/base),1)

	# Returns a string representing the weight in a form showing how to load the barbell
	def splitweight(self, weight):
		if weight > self.bar_weight:
			outstr = '%d + 2*(' % self.bar_weight
			weight = (weight - self.bar_weight)/2
			while weight > 0:
				i = 0
				while weight < self.plates[i]:
					i += 1
				outstr += '%.1f + ' % self.plates[i]
				weight -= self.plates[i]
			return outstr[:-3] + ')'
		else:
			return str(weight)
	
	# Given reps r and weight w, formats weight into readable string
	# weight is rounded to 2*smallest plate
	def formatweight(self, r, w):
		# Get plate weight, subtracting bar weight if possible
		plateWeight = w
		if w > self.bar_weight:
			plateWeight -= self.bar_weight
		
		# Round plateweight, according to 2x the smallest plate
		roundedPlateWeight = self.round(plateWeight, (self.plates[-1]*2))
		
		# calculate total weight based on method for calculating plate weight
		roundedWeight = roundedPlateWeight
		if w > self.bar_weight:
			roundedWeight += self.bar_weight
		
		return str(r) + " @ " + str(roundedWeight) + ": " + self.splitweight(roundedWeight)
	
	# Adds a lift with the given name
	# Weights is a 3-item list with the weight for [T1, T2, T3]
	# dayLifts is a 4-item list with the tier chosen for each of the 4 days
	# e.g liftName = "Squat", weight = [120, 110, 100], dayLifts = ["T1","","T2", ""]
	def addLift(self, liftName, weights, dayLifts):
		# Add to daylifts if liftname and/or tier aren't already in there
		for i in range(4):
			if dayLifts[i] is not None and dayLifts[i] is not "":
				if dayLifts[i] not in self.dayLifts[i]:
					self.dayLifts[i][dayLifts[i]] = []
				if liftName not in self.dayLifts[i][dayLifts[i]]:
					self.dayLifts[i][dayLifts[i]].append(liftName)
		# Add to stages
		self.stages[liftName] = [0,0,0]
		
		# Add to weights (make copy)
		self.weights[liftName] = weights[:]
	
		
def main():

	# Set up configuration file paths
	sheetId = ""
	with open('secret/sheetId.txt') as sheet:
		sheetId = sheet.read().strip()
	tokenPath = 'secret/token.pickle'
	credPath = 'secret/credentials.json'

	# Build sheetsController
	sheet = SheetsController(tokenPath, credPath, sheetId)
	plates = [45,35,25,10,5,2.5]
	bar_weight = 45
	gzclp = Gzclp(plates, bar_weight)
	values = sheet.get()
	gzclp.addLift("Squat", [225,185,0],["T1", None, "T2", ""])
	gzclp.addLift("Bench Press", [25,85,0],["T2", None, "T1", ""])
	gzclp.addLift("OHP", [25,85,0],["", "T1", "T1", "T3"])
	print(gzclp.dayLifts)

	if not values:
		print('No data found.')
	else:
		print(sheet.transform(values))
if __name__ == '__main__':
	main()
