#Tutorial https://www.youtube.com/watch?v=4ssigWmExak
#Asistencia ChatGPT

# Importación de las bibliotecas necesarias
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests
from bs4 import BeautifulSoup
import re
import datetime
import sys
import os

# Ruta a las credenciales de Google
route = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'creds'))
sys.path.append(route)
from creds import quickstartKey
from creds import quickstartSpreadsheet
from creds import quickstartUrl

# Definición de las constantes necesarias para conectarse a la API de Google Sheets y al sitio web
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = quickstartKey
SAMPLE_SPREADSHEET_ID = quickstartSpreadsheet

# Autenticación con la cuenta de servicio de Google
credsValue = None
credsValue = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Creación del objeto de servicio de Google Sheets
service = build('sheets', 'v4', credentials=credsValue)
sheet = service.spreadsheets()

# Obtención de los valores de compra y venta de una página web
url = quickstartUrl
response = requests.get(url)
soup = BeautifulSoup(response.content.decode(), "html.parser")
string = soup.find("div", {"class": "data__valores"})
buy_regex = r'(\d+\.\d+)Compra'
sell_regex = r'(\d+\.\d+)Venta'
buy = float(re.search(buy_regex, string.text).group(1))
sell = float(re.search(sell_regex, string.text).group(1))

# Obtención de la fecha actual y creación de una matriz de entrada para agregar a la hoja 'Sheet2'
today = datetime.date.today().strftime('%d/%m/%Y')
input = [[today,buy,sell]]

# Agregar los valores a la hoja 'Sheet2' de la hoja de cálculo
request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Hoja 2!A2", valueInputOption="USER_ENTERED", insertDataOption="OVERWRITE", body={"values":input}).execute()
