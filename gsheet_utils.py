import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import json
import streamlit as st

# Replace this with your actual Spreadsheet ID
SPREADSHEET_ID = "1EeacW0bx7KsEfOiUevBOjRHSv5oBcAAMH6AX8ammOjQ"

# Define the scope
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Get sheet object
def get_sheet():
    #creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", SCOPE)
    creds_dict = json.loads(st.secrets["SERVICE_ACCOUNT_JSON"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    return sheet

# Log a mood entry
def log_mood(mood, note=""):
    sheet = get_sheet()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, mood, note])

# Retrieve mood data as a pandas DataFrame
def get_mood_data():
    sheet = get_sheet()
    data = sheet.get_all_records()
    return pd.DataFrame(data)
