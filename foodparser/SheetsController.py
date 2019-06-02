import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class SheetsController:
	sheet = None
	sheetId = None
	gc = None
	sheetName = None
	
	def __init__(self, tokenPath, credentialsPath, sheetId, sheetName='data'):
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
		self.sheetName = sheetName

	def makeHeaders(self, headers, sheetRange='data'):
		#worksheet = self.sheet.worksheet(self.sheetName)

		# Build request
		body = {
			"valueInputOption":"USER_ENTERED",
			"data": [
				{
					"range":sheetRange+"!1:1",
					"values":[[i] for i in headers],
					"majorDimension":"COLUMNS"
				}
			]
		}

		# Execute request
		self.sheet.values().batchUpdate(
			spreadsheetId=self.sheetId,
			body=body
		).execute()

			
		

'''
	
	def get(self, sheetRange="Parameters"):
		result = self.sheet.values().get(spreadsheetId=self.sheetId, range=sheetRange).execute()
		return result.get('values', [])
	
	def init_sheet(self, sheetRange="data"):

		for row
		self.sheet.values().update()
		'''
