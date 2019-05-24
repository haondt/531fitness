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
