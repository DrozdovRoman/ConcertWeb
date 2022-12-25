import os.path
from datetime import datetime,timedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json

# Нужно будет поменять на данные из бд
SAMPLE_SPREADSHEET_ID_SALE = '1Sikp8ZmFJMaRCv5Er-QtgzrwE0BielXK0kqHtNayl1Q'
SAMPLE_SPREADSHEET_ID_TARGET = '13fn5I8aSqiIN9USvPc4D7TrKy1PgOO1Op1f8FtV7U2A'

def UpdateTable(target, sell, concertInfo, date):
    for x in concertInfo:
        for y in sell:
            if (x['id'] == y['cat_id']):
                if (x.get('qticketsConcertID') != None):
                    x['qticketsConcertID'].append(y['qticketsConcertID'])
                    x['result_date'].append(y['result_date'])
                    x['result_overall'].append(y['result_overall'])
                else:
                    x['qticketsConcertID'] = [y['qticketsConcertID']]
                    x['result_date'] = [y['result_date']]
                    x['result_overall'] = [y['result_overall']]

        for z in target:
            if (x['id'] == z['cat_id']):
                if(x.get('targetCompanyID') != None):
                    x['targetCompanyID'].append(z['targetCompanyID'])
                    x['sum_date'].append(z['sum_date'])
                    x['sum_overall'].append(z['sum_overall'])
                else:
                    x['targetCompanyID'] = [z['targetCompanyID']]
                    x['sum_date'] = [z['sum_date']]
                    x['sum_overall'] = [z['sum_overall']]
    
    UpdateOverall(concertInfo)
    UpdateDate(concertInfo,date)
    return

def UpdateOverall(concertInfo):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    try:
        concertName = []
        concertCity = []
        idQtickets = []
        countOverallTicket = []
        sumOverallTicket = []
        countOverallRefund = []
        sumOverallRefund = []
        countOverallDeleteWithoutRefund = []
        sumOverallDeleteWithoutRefund = []
        countOverallFreeTickets = []
        for element in concertInfo:
            if (element.get('qticketsConcertID') != None):
                for i in range(len(element['qticketsConcertID'])):
                    concertName.append(element['name'])
                    concertCity.append(element['city'])
                    idQtickets.append(f'''="{element['qticketsConcertID'][i]}" ''')
                    countOverallTicket.append(element['result_overall'][i]['totalResult'][0])
                    sumOverallTicket.append(element['result_overall'][i]['totalResult'][1])
                    countOverallRefund.append(element['result_overall'][i]['refundResult'][0])
                    sumOverallRefund.append(element['result_overall'][i]['refundResult'][1])
                    countOverallDeleteWithoutRefund.append(element['result_overall'][i]['delWhithoutRefundResult'][0])
                    sumOverallDeleteWithoutRefund.append(element['result_overall'][i]['delWhithoutRefundResult'][1])
                    countOverallFreeTickets.append(element['result_overall'][i]['giftTicketResult'][0])
        concertName.extend(["" for element in range(399 - len(concertName))])
        concertCity.extend(["" for element in range(399 - len(concertCity))])
        idQtickets.extend(["" for element in range(399 - len(idQtickets))])
        countOverallTicket.extend(["" for element in range(399 - len(countOverallTicket))])
        sumOverallTicket.extend(["" for element in range(399 - len(sumOverallTicket))])
        countOverallRefund.extend(["" for element in range(399 - len(countOverallRefund))])
        sumOverallRefund.extend(["" for element in range(399 - len(sumOverallRefund))])
        countOverallDeleteWithoutRefund.extend(["" for element in range(399 - len(countOverallDeleteWithoutRefund))])
        sumOverallDeleteWithoutRefund.extend(["" for element in range(399 - len(sumOverallDeleteWithoutRefund))])
        countOverallFreeTickets.extend(["" for element in range(399 - len(countOverallFreeTickets))])
        lib_update = {'values':[concertName, concertCity, idQtickets, countOverallTicket, sumOverallTicket, countOverallRefund, sumOverallRefund, countOverallDeleteWithoutRefund, sumOverallDeleteWithoutRefund, countOverallFreeTickets]}
        SAMPLE_RANGE_NAME = "Техническая таблица 2!B3:OK12"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE,range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET,range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
        print("Ok") 
    except:
        print("Error")

    try:
        concertName = []
        concertCity = []
        idVkTarget = []
        sumOverallTarget = []
        for element in concertInfo:
            if (element.get('targetCompanyID') != None):
                for i in range(len(element['targetCompanyID'])):
                    concertName.append(element['name'])
                    concertCity.append(element['city'])
                    idVkTarget.append(str(element['targetCompanyID'][i]))
                    sumOverallTarget.append('='+str(element['sum_overall'][i]).replace('.',','))
        concertName.extend(["" for element in range(399 - len(concertName))])
        concertCity.extend(["" for element in range(399 - len(concertCity))])
        idVkTarget.extend(["" for element in range(399 - len(idVkTarget))])
        sumOverallTarget.extend(["" for element in range(399 - len(sumOverallTarget))])
        lib_update = {'values':[concertName, concertCity, idVkTarget, sumOverallTarget]}
        SAMPLE_RANGE_NAME = "Техническая таблица 2!B16:OK19"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE,range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET,range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
        print("Ok") 
    except:
        print("Error")

def UpdateDate(concertInfo, date):

    countPosition = (date - datetime(day=1,month=9,year=2022)).days # Позиция элемента в таблице заполнения 23 + ( countPosition * 17 ячеек ) = ячейка заполнения
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()

    try:
        concertName = []
        concertCity = []
        idQtickets = []
        countDateTicket = []
        sumDateTicket = []
        countDateFreeTickets = []
        for element in concertInfo:
            if (element.get('qticketsConcertID') != None):
                for i in range(len(element['qticketsConcertID'])):
                    concertName.append(element['name'])
                    concertCity.append(element['city'])
                    idQtickets.append(f''' ="{element['qticketsConcertID'][i]}" ''')
                    countDateTicket.append(element['result_date'][i]['totalResult'][0])
                    sumDateTicket.append(element['result_date'][i]['totalResult'][1])
                    countDateFreeTickets.append(element['result_date'][i]['giftTicketResult'][0])
        concertName.extend(["" for element in range(399 - len(concertName))])
        concertCity.extend(["" for element in range(399 - len(concertCity))])
        idQtickets.extend(["" for element in range(399 - len(idQtickets))])
        countDateTicket.extend(["" for element in range(399 - len(countDateTicket))])
        sumDateTicket.extend(["" for element in range(399 - len(sumDateTicket))])
        countDateFreeTickets.extend(["" for element in range(399 - len(countDateFreeTickets))])
        lib_update = {'values':[concertName, concertCity, idQtickets, countDateTicket, sumDateTicket, countDateFreeTickets]}
        first_pos = 23 + (countPosition * 13)
        second_pos = 32 + (countPosition * 13)
        SAMPLE_RANGE_NAME = "Техническая таблица 2!B{}:OK{}".format(first_pos,second_pos)
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE,range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET,range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
        print("Ok") 
    except:
        print("Error")

    try:
        concertName = []
        concertCity = []
        idVkTarget = []
        sumDateTarget = []
        for element in concertInfo:
            if (element.get('targetCompanyID') != None):
                for i in range(len(element['targetCompanyID'])):
                    concertName.append(element['name'])
                    concertCity.append(element['city'])
                    idVkTarget.append('=' + str(element['targetCompanyID'][i]))
                    sumDateTarget.append('='+str(element['sum_date'][i]).replace('.',','))
        concertName.extend(["" for element in range(399 - len(concertName))])
        concertCity.extend(["" for element in range(399 - len(concertCity))])
        idVkTarget.extend(["" for element in range(399 - len(idVkTarget))])
        sumDateTarget.extend(["" for element in range(399 - len(sumDateTarget))])
        lib_update = {'values':[concertName, concertCity, idVkTarget, sumDateTarget]}
        first_pos = 30 + (countPosition * 13)
        second_pos = 33 + (countPosition * 13)
        SAMPLE_RANGE_NAME = "Техническая таблица 2!B{}:OK{}".format(first_pos,second_pos)
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE,range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET,range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
        print("Ok") 
    except:
        print("Error")
    return
