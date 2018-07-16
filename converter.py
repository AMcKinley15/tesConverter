#!/usr/bin/env python3

"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import sys


#function to find [[Card Name]] and returns HTML for it
def findCard(cardName, toSearch):
	linkType = 2
	try:
		index = cardName.index("|")
		if(cardName[index+1:] == "image"):
			linkType = 4
		elif(cardName[index+1:] == "link"):
			linkType = 2
		else:
			print("Bad link type provided. Please use 'image' or 'link'")
			exit()
		cardName = cardName[0:index]
	except ValueError:
		linkType = 2

	for row in toSearch:
		if(len(row) != 0):
			if row[0] == cardName:
				return row[linkType]


# Setup the Sheets API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
	creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# Call the Sheets API
SPREADSHEET_ID = '1LusZ4eStjzUYzvcxGHTaorPez40s22-xyRsR238uX_s'
RANGE_NAME = 'MTG: TES Website Links!A4:E'
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
spreadsheet = result.get('values', [])

#open article to convert

article = open(sys.argv[1], 'r', encoding="utf-8")
articleText = article.read()

while(True): 
	try:
		index = articleText.index("[[")
	except ValueError as e:
		break
	endIndex = articleText.index("]]")

	cardName = articleText[index+2:endIndex]

	cardLink = findCard(cardName, spreadsheet)
	if(cardLink is None):
		print("%s at index %s is either not in the spreadsheet or is misspelled. Please Fix!" % (cardName, index))
		break

	articleText = articleText[0:index] + cardLink  + articleText[endIndex+2:]

newArticle = open(sys.argv[2], "w", encoding="utf-8")
newArticle.write(articleText)

newArticle.close()
article.close()
