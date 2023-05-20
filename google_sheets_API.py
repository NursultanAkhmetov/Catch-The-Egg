from googleapiclient.discovery import build
from google.oauth2 import service_account

class GoogleSheetsAPI():
	def __init__(self):
		self.SERVICE_ACCOUNT_FILE = 'keys.json'
		self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

		self.creds = None
		self.creds = service_account.Credentials.from_service_account_file(
				self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)

		self.SPREADSHEET_ID = '1p_tF8A1rb8-XdkDFXPBhBM3dW2sDAzFTdbOyX3-umWo'
		self.service = build('sheets', 'v4', credentials=self.creds)
		self.sheet = self.service.spreadsheets()
	
	def get_values_for_highscores(self, level):
		res = self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID,
	                            range=level+"!A2:D10000").execute()
		values = res.get('values', [])

		values.sort(key=lambda row: (-int(row[2]), -int(row[0])), reverse=True)
		return values
	
	def get_total_scores(self, level):
		self.total_scores = int(self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID,
									range=level+"!A1").execute().get('values', [])[0][0])
		return self.total_scores

	def get_values_for_top_score(self, level):
		res = self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID,
									range=level+"!A2:D10000").execute()
		
		values = res.get('values', [])
		values.sort(key=lambda row: (int(row[2])))
		return values

	def save_score(self, total_scores, level, score, nickname = "Unknown"):
		aoa = [[total_scores + 1, nickname, score]]
		request = self.sheet.values().update(spreadsheetId=self.SPREADSHEET_ID,
								range=level+"!A" + str(total_scores + 2),
								valueInputOption="USER_ENTERED",
								body={"values":aoa}).execute()
		return total_scores + 2