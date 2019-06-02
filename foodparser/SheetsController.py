import re
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

	def clearSheet(self, sheetRange='data'):
		self.sheet.values().clear(
			spreadsheetId=self.sheetId,
			range=sheetRange).execute()
		

	def insertFoods(self, foods, sheetRange='data'):
		# Get Columns
		result = self.sheet.values().get(
			spreadsheetId=self.sheetId,
			range=sheetRange+'!1:1'
		).execute()
		
		headers = result.get('values',[])[0]

		values = []
		# Match food components to column headers
		for food in foods:
			foodrow = []
			for col in headers:
				if col in food:
					foodrow.append(food[col])
				else:
					foodrow.append(None)
			values.append(foodrow)

		# Build request
		body = {
			"values": values,
			"majorDimension":"ROWS"
		}

		# Execute request
		result = self.sheet.values().append(
			spreadsheetId=self.sheetId,
			range=sheetRange+'!A2:A',
			body=body,
			valueInputOption="USER_ENTERED"
		).execute()


		# Get updated row range
		uRows = result["updates"]["updatedRange"]
		uRows = uRows.split('!')[1].split(':')
		uRows = (re.findall('[0-9]+', uRows[0])[0],
			re.findall('[0-9]+', uRows[1])[0])
		A1uRows = sheetRange + "!A"+  uRows[0] + ":" + chr(ord('A')+len(headers)) + uRows[1]


		# Go back and add formulas
		# function to convert a header title to a letter
		hl = lambda x: chr(headers.index(x) + ord('A'))


		# set of lambda functions for creating formulas
		formulas = {
			"$ / unit": lambda x: '=' +
				hl("Buying Cost")+ x + "/"
				+ hl("Serving Quantity") + x,
			"g Protein / Calorie": lambda x: '=' +
				hl("Serving Protein") + x + "/" + hl("Serving Calories") + x,
			"g Protein / $": lambda x: '=' +
				"(" + hl("Serving Protein") + x + "/" + hl("Serving Quantity")
				+ x + ")/" + hl("$ / unit") + x,
			"Protein Score": lambda x: '=' +
				hl("g Protein / Calorie") + x + "*" + hl("g Protein / $") + x,
			"g Carbs / $": lambda x: '=' +
				"(" + hl("Serving Carbs") + x + "/" + hl("Serving Quantity")
				+ x + ")/" + hl("$ / unit") + x,
			"g Fat / $": lambda x: '=' +
				"(" + hl("Serving Fat") + x + "/" + hl("Serving Quantity")
				+ x + ")/" + hl("$ / unit") + x,
			"Calories / $": lambda x: '=' +
				"(" + hl("Serving Calories") + x + "/" + hl("Serving Quantity")
				+ x + ")/" + hl("$ / unit") + x
		}

		# Generate formulas for each row
		values  = []
		for i in range(int(uRows[0]),int(uRows[1])+1):
			row = []
			for col in headers:
				if col in formulas:
					row.append(formulas[col](str(i)))
				else:
					row.append(None)
			values.append(row)
		
		# Create body
		body = {
			"range":A1uRows,
			"values":values,
			"majorDimension":"ROWS"
		}

		# Execute request
		self.sheet.values().update(
			spreadsheetId=self.sheetId,
			range=A1uRows,
			body=body,
			valueInputOption="USER_ENTERED"
		).execute()
