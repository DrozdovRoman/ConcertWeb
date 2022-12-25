import os.path
from datetime import datetime,timedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
from string import ascii_uppercase

SAMPLE_SPREADSHEET_ID_SALE = '1Sikp8ZmFJMaRCv5Er-QtgzrwE0BielXK0kqHtNayl1Q'
SAMPLE_SPREADSHEET_ID_TARGET = '13fn5I8aSqiIN9USvPc4D7TrKy1PgOO1Op1f8FtV7U2A'

def FindIndex(position):
    temp = 0
    if position < 26:
        for letter in ascii_uppercase:
            if temp == position:
                return(letter)
            temp += 1
    elif position < 676:
        for letter1 in ascii_uppercase:
            for letter2 in ascii_uppercase:
                if temp == position:
                    return(letter1 + letter2)
                temp += 1
    elif position:
        for letter1 in ascii_uppercase:
            for letter2 in ascii_uppercase:
                for letter3 in ascii_uppercase:
                    if temp == position:
                        return(letter1 + letter2 + letter3)
                    temp += 1
    return "A"


# Создание шаблона под концерт
def CreateConcertTemplateSellTable(name, city, concert_date):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
    SAMPLE_RANGE_NAME = "Продажи 2!A4:A1001"
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()

    result = service.get(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    if (len(values) != 0):
        for i in range(len(values)):
            if values[i] == [] or values[i] == [""]:
                FirstFreePosition = i + 4
                break
            else:
                FirstFreePosition = len(values) + 4
    else:
        FirstFreePosition = 0 + 4

    concertDate = concert_date.strftime('%Y;%m;%d')

    # Заполнение продаж концерта
    temp = concertDate.split(";")
    value = (datetime(int(temp[0]),int(temp[1]),int(temp[2])) - datetime(2022,9,1)).days
    tempSellsFormuls = []
    if value >= 0:
        for i in range(value + 1):
            tempSellsFormuls.append(
            f"=IFERROR(HLOOKUP(AN{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AO{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AP{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AQ{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AR{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AS{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0)" 
            )
            tempSellsFormuls.append(
            f"=IFERROR(HLOOKUP(AN{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AO{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AP{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AQ{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AR{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AS{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0)" 
            )
    SAMPLE_RANGE_NAME = f"Продажи 2!CX{FirstFreePosition}:CDQ{FirstFreePosition}"
    lib_update = {'values':[tempSellsFormuls]}
    responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    
    tempFirstFreePosition = str(FirstFreePosition)
    tempName = str(name)
    tempCity = str(city)
    tempConcertDate = f"=DATE({concertDate})"
    tempDayBeforeConcert = f"=D{FirstFreePosition} - TODAY()"
    tempTargetOverallFormula = f'''=IFERROR(HLOOKUP($H${FirstFreePosition};'Техническая таблица 2'!$B$18:$OK$19;2;FALSE) +
    HLOOKUP($I${FirstFreePosition};'Техническая таблица 2'!$B$18:$OK$19;2;FALSE) +
    HLOOKUP($J${FirstFreePosition};'Техническая таблица 2'!$B$18:$OK$19;2;FALSE) +
    HLOOKUP($K${FirstFreePosition};'Техническая таблица 2'!$B$18:$OK$19;2;FALSE) +
    HLOOKUP($L${FirstFreePosition};'Техническая таблица 2'!$B$18:$OK$19;2;FALSE); "-")'''
    tempNeedToSell = f"=M{FirstFreePosition} - CV{FirstFreePosition}"
    tempPointZero = f"=CW{FirstFreePosition} - O{FirstFreePosition}"
    tempAvgTicket = f"=IF(CV{FirstFreePosition} = 0; 0; CW{FirstFreePosition} / CV{FirstFreePosition})"
    tempOrgProfit = f"=P{FirstFreePosition} - R{FirstFreePosition}"
    tempSalesForkVerySmall = f"=(T{FirstFreePosition} * U{FirstFreePosition} - V{FirstFreePosition} - O{FirstFreePosition})"
    tempSalesForkSmall = f"=(T{FirstFreePosition} * X{FirstFreePosition} - Y{FirstFreePosition} - O{FirstFreePosition})"
    tempSalesForkMedium = f"=(T{FirstFreePosition} * AA{FirstFreePosition} - AB{FirstFreePosition} - O{FirstFreePosition})"
    tempSalesForkBig = f"=(T{FirstFreePosition} * AD{FirstFreePosition} - AE{FirstFreePosition} - O{FirstFreePosition})"
    tempSalesForkVeryBig = f"=(T{FirstFreePosition} * AG{FirstFreePosition} - AH{FirstFreePosition} - O{FirstFreePosition})"

    lib_update = {'values':[[tempFirstFreePosition,tempName,tempCity,tempConcertDate,tempDayBeforeConcert,None,tempTargetOverallFormula,
    None, None, None, None, None, None, tempNeedToSell, None, tempPointZero, tempAvgTicket, None, tempOrgProfit, None, None, None, tempSalesForkVerySmall,
    None, None, tempSalesForkSmall, None, None, tempSalesForkMedium, None, None, tempSalesForkBig, None, None, tempSalesForkVeryBig]]}
    SAMPLE_RANGE_NAME = f"Продажи 2!A{FirstFreePosition}:AI{FirstFreePosition}"
    responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    tempBudgetBalance = f"=F{FirstFreePosition} - N{FirstFreePosition}"
    tempTargetOverallFormula2 = f"=IF(ISNUMBER(H{FirstFreePosition}); H{FirstFreePosition}; 0) + IF(ISNUMBER(G{FirstFreePosition});G{FirstFreePosition};0)"
    tempSellFormula = f"=R{FirstFreePosition} + BS{FirstFreePosition}"

    lib_update = {'values':[[tempFirstFreePosition, tempName, tempCity, tempConcertDate, tempBudgetBalance, None, None, None, None, None,
    None, None, None, tempTargetOverallFormula2, None, tempSellFormula]]}
    SAMPLE_RANGE_NAME = f"Таргет 2!A{FirstFreePosition}:P{FirstFreePosition}"
    responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    value = (datetime(int(temp[0]),int(temp[1]),int(temp[2])) - datetime(2022,9,5)).days
    tempTargetFormuls = []
    tempTargetFormuls.append(f'''=O{FirstFreePosition} - P{FirstFreePosition} ''')
    tempTargetFormuls.append(f'''=IF(P{FirstFreePosition} > 0; N{FirstFreePosition} / P{FirstFreePosition}; 0)''')
    if value >= 0:
        for i in range(value + 1):
            if i > 0 and i % 7 == 0:
                # Освоенно денег за неделю
                tempTargetFormuls.append(
                f"={FindIndex(len(tempTargetFormuls) + 50 - 3)}{FirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 7)}{FirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 11)}{FirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 15)}{FirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 19)}{FirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 23)}{FirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 27)}{FirstFreePosition}"
                )
                # Количество продаж за неделю
                tempTargetFormuls.append(
                f"={FindIndex(len(tempTargetFormuls) + 50 - 6)}{FirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 10)}{FirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 14)}{FirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 18)}{FirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 22)}{FirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 26)}{FirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 30)}{FirstFreePosition}"
                )
                # Стоимость лида за неделю
                tempTargetFormuls.append(f'''=IF({FindIndex(len(tempTargetFormuls) + 50 - 2)}{FirstFreePosition} > 0;''' +
            f'''{FindIndex(len(tempTargetFormuls) + 50 - 3)}{FirstFreePosition} / {FindIndex(len(tempTargetFormuls) + 50 - 2)}{FirstFreePosition}'''+
            f''';0)''')
            # Количество проданных билетов за день
            tempTargetFormuls.append(
            f"=IFERROR(HLOOKUP(T{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(U{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(V{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(W{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(X{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(Y{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0)" )
            # Сумма проданных билетов за день
            tempTargetFormuls.append(
            f"=IFERROR(HLOOKUP(T{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(U{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(V{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(W{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(X{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(Y{FirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0)" )

            # Сумма потраченная на таргет за день
            tempTargetFormuls.append(
            f"=IFERROR(HLOOKUP(I{FirstFreePosition};'Техническая таблица 2'!B{32 + i * 13}:OK{33 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(J{FirstFreePosition};'Техническая таблица 2'!B{32 + i * 13}:OK{33 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(K{FirstFreePosition};'Техническая таблица 2'!B{32 + i * 13}:OK{33 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(L{FirstFreePosition};'Техническая таблица 2'!B{32 + i * 13}:OK{33 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(M{FirstFreePosition};'Техническая таблица 2'!B{32 + i * 13}:OK{33 + i * 13};2;FALSE);0)")

            # Средняя стоимость билета за день
            tempTargetFormuls.append(f'''=IF({FindIndex(len(tempTargetFormuls) + 50 - 4)}{FirstFreePosition} > 0;''' +
            f'''{FindIndex(len(tempTargetFormuls) + 50 - 2)}{FirstFreePosition} / {FindIndex(len(tempTargetFormuls) + 50 - 4)}{FirstFreePosition}'''+
            f''';0)''') # 52 позиция элемента BZ от которого начинается поиск 
            
    SAMPLE_RANGE_NAME = f"Таргет 2!BX{FirstFreePosition}:CCQ{FirstFreePosition}"
    lib_update = {'values':[tempTargetFormuls]}
    responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    return FirstFreePosition


# Обновление шаблона концерта
def UpdateConcertTemplateSellTable(name, city, concert_date, spreadSheetPositon):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()

    concert_date = concert_date.strftime('%Y;%m;%d')
    tempConcertDate = f"=DATE({concert_date})"
    tempFirstFreePosition = str(spreadSheetPositon)
    tempName = str(name)
    tempCity = str(city)
    lib_update = {'values': [[tempFirstFreePosition, tempName, tempCity, tempConcertDate]]}
    SAMPLE_RANGE_NAME = f"Продажи 2!A{spreadSheetPositon}:D{spreadSheetPositon}"
    # Обновление шаблона продажи
    responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    # Обновление шаблона таргет
    SAMPLE_RANGE_NAME = f"Таргет 2!A{spreadSheetPositon}:D{spreadSheetPositon}"
    responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    # Обновление продаж концерта
    temp = concert_date.split(";")
    value = (datetime(int(temp[0]),int(temp[1]),int(temp[2])) - datetime(2022,9,1)).days
    tempSellsFormuls = []
    if value >= 0:
        for i in range(value + 1):
            tempSellsFormuls.append(
            f"=IFERROR(HLOOKUP(AN{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AO{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AP{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AQ{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AR{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AS{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0)" 
            )
            tempSellsFormuls.append(
            f"=IFERROR(HLOOKUP(AN{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AO{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AP{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AQ{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AR{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(AS{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0)" 
            )
    SAMPLE_RANGE_NAME = f"Продажи 2!CX{tempFirstFreePosition}:CDQ{tempFirstFreePosition}"
    lib_update = {'values':[tempSellsFormuls]}
    responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    value = (datetime(int(temp[0]),int(temp[1]),int(temp[2])) - datetime(2022,9,5)).days
    tempTargetFormuls = []
    if value >= 0:
        for i in range(value + 1):
            if i > 0 and i % 7 == 0:
                # Освоенно денег за неделю
                tempTargetFormuls.append(
                f"={FindIndex(len(tempTargetFormuls) + 50 - 3)}{tempFirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 7)}{tempFirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 11)}{tempFirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 15)}{tempFirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 19)}{tempFirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 23)}{tempFirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 27)}{tempFirstFreePosition}"
                )
                # Количество продаж за неделю
                tempTargetFormuls.append(
                f"={FindIndex(len(tempTargetFormuls) + 50 - 6)}{tempFirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 10)}{tempFirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 14)}{tempFirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 18)}{tempFirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 22)}{tempFirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 26)}{tempFirstFreePosition}+"
                f"{FindIndex(len(tempTargetFormuls) + 50 - 30)}{tempFirstFreePosition}"
                )
                # Стоимость лида за неделю
                tempTargetFormuls.append(f'''=IF({FindIndex(len(tempTargetFormuls) + 50 - 2)}{tempFirstFreePosition} > 0;''' +
            f'''{FindIndex(len(tempTargetFormuls) + 50 - 3)}{tempFirstFreePosition} / {FindIndex(len(tempTargetFormuls) + 50 - 2)}{tempFirstFreePosition}'''+
            f''';0)''')
            # Количество проданных билетов за день
            tempTargetFormuls.append(
            f"=IFERROR(HLOOKUP(T{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(U{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(V{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(W{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(X{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(Y{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};2;FALSE);0)" )
            # Сумма проданных билетов за день
            tempTargetFormuls.append(
            f"=IFERROR(HLOOKUP(T{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(U{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(V{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(W{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(X{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0) +" +
            f"IFERROR(HLOOKUP(Y{tempFirstFreePosition};'Техническая таблица 2'!B{25 + i * 13}:OK{28 + i * 13};3;FALSE);0)" )

            # Сумма потраченная на таргет за день
            tempTargetFormuls.append(
            f"=IFERROR(HLOOKUP(I{tempFirstFreePosition};'Техническая таблица 2'!B{32 + i * 13}:OK{33 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(J{tempFirstFreePosition};'Техническая таблица 2'!B{32 + i * 13}:OK{33 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(K{tempFirstFreePosition};'Техническая таблица 2'!B{32 + i * 13}:OK{33 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(L{tempFirstFreePosition};'Техническая таблица 2'!B{32 + i * 13}:OK{33 + i * 13};2;FALSE);0) +" +
            f"IFERROR(HLOOKUP(M{tempFirstFreePosition};'Техническая таблица 2'!B{32 + i * 13}:OK{33 + i * 13};2;FALSE);0)")

            # Средняя стоимость билета за день
            tempTargetFormuls.append(f'''=IF({FindIndex(len(tempTargetFormuls) + 50 - 4)}{tempFirstFreePosition} > 0;''' +
            f'''{FindIndex(len(tempTargetFormuls) + 50 - 2)}{tempFirstFreePosition} / {FindIndex(len(tempTargetFormuls) + 50 - 4)}{tempFirstFreePosition}'''+
            f''';0)''') # 52 позиция элемента BZ от которого начинается поиск 
    SAMPLE_RANGE_NAME = f"Таргет 2!BZ{tempFirstFreePosition}:CCQ{tempFirstFreePosition}"
    lib_update = {'values':[tempTargetFormuls]}
    responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    return

# Очистка шаблона концерта
def ClearConcertTemplateSellTable(spreadSheetPositon):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    lib_update = {'values': [["" for element in range(2149)]]}
    SAMPLE_RANGE_NAME = f"Продажи 2!A{spreadSheetPositon}:CDQ{spreadSheetPositon}"
    responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    lib_update = {'values': [["" for element in range(2123)]]}
    SAMPLE_RANGE_NAME = f"Таргет 2!A{spreadSheetPositon}:CCQ{spreadSheetPositon}"
    responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    return


# Подключение аккаунта Qtickets
# Возвращаем номер подключенного аккаунта
def CreateConnectQticketsAccount(qticketsConcertID, spreadSheetPositon):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
    SAMPLE_RANGE_NAME = f"Продажи 2!AN{spreadSheetPositon}:AS{spreadSheetPositon}"
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    result = service.get(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    if len(values) == 0:
        # Подключенный аккаунт №1 Продажи
        tempQticketsID = f'''="{qticketsConcertID}" '''
        tempCountTicket = f'''=IFERROR(HLOOKUP($AN${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;2;FALSE);0) '''
        tempSumTicket = f'''=IFERROR(HLOOKUP($AN${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;3;FALSE);0) '''
        tempRefundCountTicket = f'''=IFERROR(HLOOKUP($AN${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;4;FALSE);0) '''
        tempRefundSumTicket = f'''=IFERROR(HLOOKUP($AN${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;5;FALSE);0) '''
        tempCountDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($AN${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;6;FALSE);0) '''
        tempSumDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($AN${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;7;FALSE);0) '''
        tempFreeTicket = f'''=IFERROR(HLOOKUP($AN${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;8;FALSE);0) '''

        lib_update = {'values': [[tempQticketsID, None, None, None, None, None,
        tempCountTicket, tempSumTicket, tempRefundCountTicket, tempRefundSumTicket,
        tempCountDeleteWithoutRefund, tempSumDeleteWithoutRefund, tempFreeTicket]]}
        SAMPLE_RANGE_NAME = f"Продажи 2!AN{spreadSheetPositon}:AZ{spreadSheetPositon}"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

        # Подключенный аккаунт №1 Таргет
        tempQticketsID = f'''="{qticketsConcertID}" '''
        tempCountTicket = f'''=IFERROR(HLOOKUP($T${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;2;FALSE);0) '''
        tempSumTicket = f'''=IFERROR(HLOOKUP($T${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;3;FALSE);0) '''
        tempRefundCountTicket = f'''=IFERROR(HLOOKUP($T${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;4;FALSE);0) '''
        tempRefundSumTicket = f'''=IFERROR(HLOOKUP($T${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;5;FALSE);0) '''
        tempCountDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($T${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;6;FALSE);0) '''
        tempSumDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($T${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;7;FALSE);0) '''
        tempFreeTicket = f'''=IFERROR(HLOOKUP($T${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;8;FALSE);0) '''

        lib_update = {'values': [[tempQticketsID, None, None, None, None, None,
        tempCountTicket, tempSumTicket, tempRefundCountTicket, tempRefundSumTicket,
        tempCountDeleteWithoutRefund, tempSumDeleteWithoutRefund, tempFreeTicket]]}
        SAMPLE_RANGE_NAME = f"Таргет 2!T{spreadSheetPositon}:AF{spreadSheetPositon}"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

        # Шаблон для сбора данных со всех аккаунтов Продажи
        tempQticketsCountOverall = f"=CO{spreadSheetPositon} - CQ{spreadSheetPositon}"
        tempQticketsSumOverall = f"=CP{spreadSheetPositon} - CR{spreadSheetPositon}"
        tempOverallCount = f"=AT{spreadSheetPositon} + BA{spreadSheetPositon} + BH{spreadSheetPositon} + BO{spreadSheetPositon} + BV{spreadSheetPositon} + CC{spreadSheetPositon}"
        tempOverallSum = f"=AU{spreadSheetPositon} + BB{spreadSheetPositon} + BI{spreadSheetPositon} + BP{spreadSheetPositon} + BW{spreadSheetPositon} + CD{spreadSheetPositon}"
        tempRefundOverallCount = f"=AV{spreadSheetPositon} + BC{spreadSheetPositon} + BJ{spreadSheetPositon} + BQ{spreadSheetPositon} + BX{spreadSheetPositon} + CE{spreadSheetPositon}"
        tempRefundOverallSum = f"=AW{spreadSheetPositon} + BD{spreadSheetPositon} + BK{spreadSheetPositon} + BR{spreadSheetPositon} + BY{spreadSheetPositon} + CF{spreadSheetPositon}"
        tempDeleteWithoutRefundOverallCount = f"=AX{spreadSheetPositon} + BE{spreadSheetPositon} + BL{spreadSheetPositon} + BS{spreadSheetPositon} + BZ{spreadSheetPositon} + CG{spreadSheetPositon}"
        tempDeleteWithoutRefundOverallSum = f"=AY{spreadSheetPositon} + BF{spreadSheetPositon} + BM{spreadSheetPositon} + BT{spreadSheetPositon} + CA{spreadSheetPositon} + CH{spreadSheetPositon}"
        tempFreeTicketOverall = f"=AZ{spreadSheetPositon} + BG{spreadSheetPositon} + BN{spreadSheetPositon} + BU{spreadSheetPositon} + CB{spreadSheetPositon} + CI{spreadSheetPositon}"
        tempCountTotal = f"=CM{spreadSheetPositon}+AK{spreadSheetPositon}"
        tempSumTotal = f"=CN{spreadSheetPositon} + AL{spreadSheetPositon}"

        lib_update = {'values': [[tempQticketsCountOverall, tempQticketsSumOverall, tempOverallCount,
        tempOverallSum, tempRefundOverallCount, tempRefundOverallSum, tempDeleteWithoutRefundOverallCount,
        tempDeleteWithoutRefundOverallSum, tempFreeTicketOverall, tempCountTotal, tempSumTotal]]}
        SAMPLE_RANGE_NAME = f"Продажи 2!CM{spreadSheetPositon}:CW{spreadSheetPositon}"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

        # Шаблон для сбора данных со всех аккаунтов Таргет
        tempQticketsCountOverall = f"=BT{spreadSheetPositon} - BU{spreadSheetPositon}"
        tempOverallCount = f"=Z{spreadSheetPositon} + AG{spreadSheetPositon} + AN{spreadSheetPositon} + AU{spreadSheetPositon} + BB{spreadSheetPositon} + BI{spreadSheetPositon}"
        tempRefundOverallCount = f"=AB{spreadSheetPositon} + AI{spreadSheetPositon} + AP{spreadSheetPositon} + AW{spreadSheetPositon} + BD{spreadSheetPositon} + BK{spreadSheetPositon}"
        tempDeleteWithoutRefundOverallCount = f"=AD{spreadSheetPositon} + AK{spreadSheetPositon} + AR{spreadSheetPositon} + AY{spreadSheetPositon} + BF{spreadSheetPositon} + BM{spreadSheetPositon}"
        tempFreeTicketOverall = f"=AF{spreadSheetPositon} + AM{spreadSheetPositon} + AT{spreadSheetPositon} + BA{spreadSheetPositon} + BH{spreadSheetPositon} + BO{spreadSheetPositon}"

        lib_update = {'values': [[tempQticketsCountOverall, tempOverallCount,
        tempRefundOverallCount, tempDeleteWithoutRefundOverallCount, tempFreeTicketOverall]]}
        SAMPLE_RANGE_NAME = f"Таргет 2!BS{spreadSheetPositon}:BW{spreadSheetPositon}"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

        return 1

    else:
        if len(values[0]) == 1:
            # Подключенный аккаунт №2 Продажи
            tempQticketsID = f'''="{qticketsConcertID}" '''
            tempCountTicket = f'''=IFERROR(HLOOKUP($AO${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;2;FALSE);0) '''
            tempSumTicket = f'''=IFERROR(HLOOKUP($AO${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;3;FALSE);0) '''
            tempRefundCountTicket = f'''=IFERROR(HLOOKUP($AO${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;4;FALSE);0) '''
            tempRefundSumTicket = f'''=IFERROR(HLOOKUP($AO${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;5;FALSE);0) '''
            tempCountDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($AO${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;6;FALSE);0) '''
            tempSumDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($AO${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;7;FALSE);0) '''
            tempFreeTicket = f'''=IFERROR(HLOOKUP($AO${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;8;FALSE);0) '''

            lib_update = {'values': [[tempQticketsID, None, None, None, None,
            None, None, None, None, None, None, None,
            tempCountTicket, tempSumTicket, tempRefundCountTicket, tempRefundSumTicket,
            tempCountDeleteWithoutRefund, tempSumDeleteWithoutRefund, tempFreeTicket]]}
            SAMPLE_RANGE_NAME = f"Продажи 2!AO{spreadSheetPositon}:BG{spreadSheetPositon}"
            responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

            # Подключенный аккаунт №2 Таргет
            tempQticketsID = f'''="{qticketsConcertID}" '''
            tempCountTicket = f'''=IFERROR(HLOOKUP($U${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;2;FALSE);0) '''
            tempSumTicket = f'''=IFERROR(HLOOKUP($U${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;3;FALSE);0) '''
            tempRefundCountTicket = f'''=IFERROR(HLOOKUP($U${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;4;FALSE);0) '''
            tempRefundSumTicket = f'''=IFERROR(HLOOKUP($U${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;5;FALSE);0) '''
            tempCountDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($U${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;6;FALSE);0) '''
            tempSumDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($U${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;7;FALSE);0) '''
            tempFreeTicket = f'''=IFERROR(HLOOKUP($U${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;8;FALSE);0) '''

            lib_update = {'values': [[tempQticketsID, None, None, None, None,
            None, None, None, None, None, None, None,
            tempCountTicket, tempSumTicket, tempRefundCountTicket, tempRefundSumTicket,
            tempCountDeleteWithoutRefund, tempSumDeleteWithoutRefund, tempFreeTicket]]}
            SAMPLE_RANGE_NAME = f"Таргет 2!U{spreadSheetPositon}:AM{spreadSheetPositon}"
            responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

            return 2

        elif len(values[0]) == 2:
            # Подключенный аккаунт №3 Продажи
            tempQticketsID = f'''="{qticketsConcertID}" '''
            tempCountTicket = f'''=IFERROR(HLOOKUP($AP${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;2;FALSE);0) '''
            tempSumTicket = f'''=IFERROR(HLOOKUP($AP${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;3;FALSE);0) '''
            tempRefundCountTicket = f'''=IFERROR(HLOOKUP($AP${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;4;FALSE);0) '''
            tempRefundSumTicket = f'''=IFERROR(HLOOKUP($AP${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;5;FALSE);0) '''
            tempCountDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($AP${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;6;FALSE);0) '''
            tempSumDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($AP${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;7;FALSE);0) '''
            tempFreeTicket = f'''=IFERROR(HLOOKUP($AP${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;8;FALSE);0) '''

            lib_update = {'values': [[tempQticketsID, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            tempCountTicket, tempSumTicket, tempRefundCountTicket, tempRefundSumTicket,
            tempCountDeleteWithoutRefund, tempSumDeleteWithoutRefund, tempFreeTicket]]}
            SAMPLE_RANGE_NAME = f"Продажи 2!AP{spreadSheetPositon}:BN{spreadSheetPositon}"
            responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

            # Подключенный аккаунт №3 Таргет
            tempQticketsID = f'''="{qticketsConcertID}" '''
            tempCountTicket = f'''=IFERROR(HLOOKUP($V${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;2;FALSE);0) '''
            tempSumTicket = f'''=IFERROR(HLOOKUP($V${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;3;FALSE);0) '''
            tempRefundCountTicket = f'''=IFERROR(HLOOKUP($V${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;4;FALSE);0) '''
            tempRefundSumTicket = f'''=IFERROR(HLOOKUP($V${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;5;FALSE);0) '''
            tempCountDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($V${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;6;FALSE);0) '''
            tempSumDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($V${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;7;FALSE);0) '''
            tempFreeTicket = f'''=IFERROR(HLOOKUP($V${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;8;FALSE);0) '''

            lib_update = {'values': [[tempQticketsID, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            tempCountTicket, tempSumTicket, tempRefundCountTicket, tempRefundSumTicket,
            tempCountDeleteWithoutRefund, tempSumDeleteWithoutRefund, tempFreeTicket]]}
            SAMPLE_RANGE_NAME = f"Таргет 2!V{spreadSheetPositon}:AT{spreadSheetPositon}"
            responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

            return 3

        elif len(values[0]) == 3:
            # Подключенный аккаунт №4 Продажи
            tempQticketsID = f'''="{qticketsConcertID}" '''
            tempCountTicket = f'''=IFERROR(HLOOKUP($AQ${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;2;FALSE);0) '''
            tempSumTicket = f'''=IFERROR(HLOOKUP($AQ${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;3;FALSE);0) '''
            tempRefundCountTicket = f'''=IFERROR(HLOOKUP($AQ${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;4;FALSE);0) '''
            tempRefundSumTicket = f'''=IFERROR(HLOOKUP($AQ${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;5;FALSE);0) '''
            tempCountDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($AQ${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;6;FALSE);0) '''
            tempSumDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($AQ${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;7;FALSE);0) '''
            tempFreeTicket = f'''=IFERROR(HLOOKUP($AQ${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;8;FALSE);0) '''

            lib_update = {'values': [[tempQticketsID, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            tempCountTicket, tempSumTicket, tempRefundCountTicket, tempRefundSumTicket,
            tempCountDeleteWithoutRefund, tempSumDeleteWithoutRefund, tempFreeTicket]]}
            SAMPLE_RANGE_NAME = f"Продажи 2!AQ{spreadSheetPositon}:BU{spreadSheetPositon}"
            responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

            # Подключенный аккаунт №4 Таргет
            tempQticketsID = f'''="{qticketsConcertID}" '''
            tempCountTicket = f'''=IFERROR(HLOOKUP($W${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;2;FALSE);0) '''
            tempSumTicket = f'''=IFERROR(HLOOKUP($W${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;3;FALSE);0) '''
            tempRefundCountTicket = f'''=IFERROR(HLOOKUP($W${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;4;FALSE);0) '''
            tempRefundSumTicket = f'''=IFERROR(HLOOKUP($W${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;5;FALSE);0) '''
            tempCountDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($W${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;6;FALSE);0) '''
            tempSumDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($W${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;7;FALSE);0) '''
            tempFreeTicket = f'''=IFERROR(HLOOKUP($W${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;8;FALSE);0) '''

            lib_update = {'values': [[tempQticketsID, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            tempCountTicket, tempSumTicket, tempRefundCountTicket, tempRefundSumTicket,
            tempCountDeleteWithoutRefund, tempSumDeleteWithoutRefund, tempFreeTicket]]}
            SAMPLE_RANGE_NAME = f"Таргет 2!W{spreadSheetPositon}:BA{spreadSheetPositon}"
            responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
            return 4

        elif len(values[0]) == 4:
            # Подключенный аккаунт №5 Продажи
            tempQticketsID = f'''="{qticketsConcertID}" '''
            tempCountTicket = f'''=IFERROR(HLOOKUP($AR${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;2;FALSE);0) '''
            tempSumTicket = f'''=IFERROR(HLOOKUP($AR${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;3;FALSE);0) '''
            tempRefundCountTicket = f'''=IFERROR(HLOOKUP($AR${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;4;FALSE);0) '''
            tempRefundSumTicket = f'''=IFERROR(HLOOKUP($AR${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;5;FALSE);0) '''
            tempCountDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($AR${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;6;FALSE);0) '''
            tempSumDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($AR${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;7;FALSE;0) '''
            tempFreeTicket = f'''=IFERROR(HLOOKUP($AR${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;8;FALSE);0) '''

            lib_update = {'values': [[tempQticketsID, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            tempCountTicket, tempSumTicket, tempRefundCountTicket, tempRefundSumTicket,
            tempCountDeleteWithoutRefund, tempSumDeleteWithoutRefund, tempFreeTicket]]}
            SAMPLE_RANGE_NAME = f"Продажи 2!AR{spreadSheetPositon}:CB{spreadSheetPositon}"
            responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

            # Подключенный аккаунт №5 Таргет
            tempQticketsID = f'''="{qticketsConcertID}" '''
            tempCountTicket = f'''=IFERROR(HLOOKUP($X${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;2;FALSE);0) '''
            tempSumTicket = f'''=IFERROR(HLOOKUP($X${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;3;FALSE);0) '''
            tempRefundCountTicket = f'''=IFERROR(HLOOKUP($X${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;4;FALSE);0) '''
            tempRefundSumTicket = f'''=IFERROR(HLOOKUP($X${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;5;FALSE);0) '''
            tempCountDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($X${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;6;FALSE);0) '''
            tempSumDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($X${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;7;FALSE);0) '''
            tempFreeTicket = f'''=IFERROR(HLOOKUP($X${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;8;FALSE);0) '''

            lib_update = {'values': [[tempQticketsID, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            tempCountTicket, tempSumTicket, tempRefundCountTicket, tempRefundSumTicket,
            tempCountDeleteWithoutRefund, tempSumDeleteWithoutRefund, tempFreeTicket]]}
            SAMPLE_RANGE_NAME = f"Таргет 2!X{spreadSheetPositon}:BH{spreadSheetPositon}"
            responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
            return 5

        elif len(values[0]) == 5:
            # Подключенный аккаунт №6 Продажи
            tempQticketsID = f'''="{qticketsConcertID}" '''
            tempCountTicket = f'''=IFERROR(HLOOKUP($AS${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;2;FALSE);0) '''
            tempSumTicket = f'''=IFERROR(HLOOKUP($AS${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;3;FALSE);0) '''
            tempRefundCountTicket = f'''=IFERROR(HLOOKUP($AS${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;4;FALSE);0) '''
            tempRefundSumTicket = f'''=IFERROR(HLOOKUP($AS${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;5;FALSE);0) '''
            tempCountDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($AS${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;6;FALSE);0) '''
            tempSumDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($AS${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;7;FALSE);0) '''
            tempFreeTicket = f'''=IFERROR(HLOOKUP($AS${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;8;FALSE);0) '''

            lib_update = {'values': [[tempQticketsID,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            tempCountTicket, tempSumTicket, tempRefundCountTicket, tempRefundSumTicket,
            tempCountDeleteWithoutRefund, tempSumDeleteWithoutRefund, tempFreeTicket]]}
            SAMPLE_RANGE_NAME = f"Продажи 2!AS{spreadSheetPositon}:CI{spreadSheetPositon}"
            responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

            # Подключенный аккаунт №6 Таргет
            tempQticketsID = f'''="{qticketsConcertID}" '''
            tempCountTicket = f'''=IFERROR(HLOOKUP($Y${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;2;FALSE);0) '''
            tempSumTicket = f'''=IFERROR(HLOOKUP($Y${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;3;FALSE);0) '''
            tempRefundCountTicket = f'''=IFERROR(HLOOKUP($Y${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;4;FALSE);0) '''
            tempRefundSumTicket = f'''=IFERROR(HLOOKUP($Y${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;5;FALSE);0) '''
            tempCountDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($Y${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;6;FALSE);0) '''
            tempSumDeleteWithoutRefund = f'''=IFERROR(HLOOKUP($Y${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;7;FALSE);0) '''
            tempFreeTicket = f'''=IFERROR(HLOOKUP($Y${spreadSheetPositon};'Техническая таблица 2'!$B$5:$OK$12;8;FALSE);0) '''

            lib_update = {'values': [[tempQticketsID,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            None, None, None, None, None, None, None,
            tempCountTicket, tempSumTicket, tempRefundCountTicket, tempRefundSumTicket,
            tempCountDeleteWithoutRefund, tempSumDeleteWithoutRefund, tempFreeTicket]]}
            SAMPLE_RANGE_NAME = f"Таргет 2!Y{spreadSheetPositon}:BQ{spreadSheetPositon}"
            responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
            return 6
    return 0


def ChangeConnectQticketsAccount(qticketsConcertID, spreadSheetPositon, spreadSheetQticketsPosition):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
    SAMPLE_RANGE_NAME = f"Продажи 2!AN{spreadSheetPositon}:AS{spreadSheetPositon}"
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    result = service.get(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if spreadSheetQticketsPosition == 1:
        tempQticketsID = f'''="{qticketsConcertID}" '''
        SAMPLE_RANGE_NAME = f"Продажи 2!AN{spreadSheetPositon}"
        lib_update = {'values': [[tempQticketsID]]}
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    elif spreadSheetQticketsPosition == 2:
        tempQticketsID = f'''="{qticketsConcertID}" '''
        SAMPLE_RANGE_NAME = f"Продажи 2!AO{spreadSheetPositon}"
        lib_update = {'values': [[tempQticketsID]]}
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    elif spreadSheetQticketsPosition == 3:
        tempQticketsID = f'''="{qticketsConcertID}" '''
        SAMPLE_RANGE_NAME = f"Продажи 2!AP{spreadSheetPositon}"
        lib_update = {'values': [[tempQticketsID]]}
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    elif spreadSheetQticketsPosition == 4:
        tempQticketsID = f'''="{qticketsConcertID}" '''
        SAMPLE_RANGE_NAME = f"Продажи 2!AQ{spreadSheetPositon}"
        lib_update = {'values': [[tempQticketsID]]}
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    elif spreadSheetQticketsPosition == 5:
        tempQticketsID = f'''="{qticketsConcertID}" '''
        SAMPLE_RANGE_NAME = f"Продажи 2!AR{spreadSheetPositon}"
        lib_update = {'values': [[tempQticketsID]]}
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    elif spreadSheetQticketsPosition == 6:
        tempQticketsID = f'''="{qticketsConcertID}" '''
        SAMPLE_RANGE_NAME = f"Продажи 2!AS{spreadSheetPositon}"
        lib_update = {'values': [[tempQticketsID]]}
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    if spreadSheetQticketsPosition == 1:
        tempQticketsID = f'''="{qticketsConcertID}" '''
        SAMPLE_RANGE_NAME = f"Таргет 2!T{spreadSheetPositon}"
        lib_update = {'values': [[tempQticketsID]]}
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    elif spreadSheetQticketsPosition == 2:
        tempQticketsID = f'''="{qticketsConcertID}" '''
        SAMPLE_RANGE_NAME = f"Таргет 2!U{spreadSheetPositon}"
        lib_update = {'values': [[tempQticketsID]]}
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    elif spreadSheetQticketsPosition == 3:
        tempQticketsID = f'''="{qticketsConcertID}" '''
        SAMPLE_RANGE_NAME = f"Таргет 2!V{spreadSheetPositon}"
        lib_update = {'values': [[tempQticketsID]]}
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    elif spreadSheetQticketsPosition == 4:
        tempQticketsID = f'''="{qticketsConcertID}" '''
        SAMPLE_RANGE_NAME = f"Таргет 2!W{spreadSheetPositon}"
        lib_update = {'values': [[tempQticketsID]]}
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    elif spreadSheetQticketsPosition == 5:
        tempQticketsID = f'''="{qticketsConcertID}" '''
        SAMPLE_RANGE_NAME = f"Таргет 2!X{spreadSheetPositon}"
        lib_update = {'values': [[tempQticketsID]]}
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    elif spreadSheetQticketsPosition == 6:
        tempQticketsID = f'''="{qticketsConcertID}" '''
        SAMPLE_RANGE_NAME = f"Таргет 2!Y{spreadSheetPositon}"
        lib_update = {'values': [[tempQticketsID]]}
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

def ClearConnectQticketsAccount(spreadSheetPositon, spreadSheetQticketsPosition):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
    SAMPLE_RANGE_NAME = f"Продажи 2!AN{spreadSheetPositon}:AS{spreadSheetPositon}"
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    result = service.get(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    # Удаление данных об аккаунте в таблице Продаж
    if spreadSheetQticketsPosition == 1:
        SAMPLE_RANGE_NAME = f"Продажи 2!AN{spreadSheetPositon}:AZ{spreadSheetPositon}"
        lib_update = {'values': [["", None, None, None, None, None, "", "", "", "", "", "", ""]]}
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
        lib_update = {'values': [["", "", "", "", "", "", "", "", "", "", ""]]}
        SAMPLE_RANGE_NAME = f"Продажи 2!CM{spreadSheetPositon}:CW{spreadSheetPositon}"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    elif spreadSheetQticketsPosition == 2:
        lib_update = {'values': [["", None, None, None, None, None, None, None, None, None, None, None, "", "", "", "", "", "", ""]]}
        SAMPLE_RANGE_NAME = f"Продажи 2!AO{spreadSheetPositon}:BG{spreadSheetPositon}"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    elif spreadSheetQticketsPosition == 3:
        lib_update = {'values': [["", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "", "", "", "", "", "", ""]]}
        SAMPLE_RANGE_NAME = f"Продажи 2!AP{spreadSheetPositon}:BN{spreadSheetPositon}"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    elif spreadSheetQticketsPosition == 4:
        lib_update = {'values': [["", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "", "", "", "", "", "", ""]]}
        SAMPLE_RANGE_NAME = f"Продажи 2!AQ{spreadSheetPositon}:BU{spreadSheetPositon}"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    elif spreadSheetQticketsPosition == 5:
        lib_update = {'values': [["", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "", "", "", "", "", "", ""]]}
        SAMPLE_RANGE_NAME = f"Продажи 2!AR{spreadSheetPositon}:CB{spreadSheetPositon}"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    elif spreadSheetQticketsPosition == 6:
            lib_update = {'values': [["", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "", "", "", "", "", "", ""]]}
            SAMPLE_RANGE_NAME = f"Продажи 2!AS{spreadSheetPositon}:CI{spreadSheetPositon}"
            responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    # Удаление данных об аккаунте в таблице Таргет
    if spreadSheetQticketsPosition == 1:
        SAMPLE_RANGE_NAME = f"Таргет 2!T{spreadSheetPositon}:AF{spreadSheetPositon}"
        lib_update = {'values': [["", None, None, None, None, None, "", "", "", "", "", "", ""]]}
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
        lib_update = {'values': [["", "", "", "", ""]]}
        SAMPLE_RANGE_NAME = f"Таргет 2!BS{spreadSheetPositon}:BW{spreadSheetPositon}"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    elif spreadSheetQticketsPosition == 2:
        lib_update = {'values': [["", None, None, None, None, None, None, None, None, None, None, None, "", "", "", "", "", "", ""]]}
        SAMPLE_RANGE_NAME = f"Таргет 2!U{spreadSheetPositon}:AM{spreadSheetPositon}"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    elif spreadSheetQticketsPosition == 3:
        lib_update = {'values': [["", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "", "", "", "", "", "", ""]]}
        SAMPLE_RANGE_NAME = f"Таргет 2!V{spreadSheetPositon}:AT{spreadSheetPositon}"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    elif spreadSheetQticketsPosition == 4:
        lib_update = {'values': [["", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "", "", "", "", "", "", ""]]}
        SAMPLE_RANGE_NAME = f"Таргет 2!W{spreadSheetPositon}:BU{spreadSheetPositon}"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    elif spreadSheetQticketsPosition == 5:
        lib_update = {'values': [["", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "", "", "", "", "", "", ""]]}
        SAMPLE_RANGE_NAME = f"Таргет 2!X{spreadSheetPositon}:BH{spreadSheetPositon}"
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

    elif spreadSheetQticketsPosition == 6:
            lib_update = {'values': [["", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, "", "", "", "", "", "", ""]]}
            SAMPLE_RANGE_NAME = f"Таргет 2!Y{spreadSheetPositon}:BO{spreadSheetPositon}"
            responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME, valueInputOption = 'USER_ENTERED', body = lib_update).execute()


# Подключение аккаунта Таргет

def CreateConnectTargetAccount(targetCompanyID, spreadSheetPositon):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
    SAMPLE_RANGE_NAME_SELL = f"Продажи 2!H{spreadSheetPositon}:L{spreadSheetPositon}"
    SAMPLE_RANGE_NAME_TARGET = f"Таргет 2!I{spreadSheetPositon}:M{spreadSheetPositon}"
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    result = service.get(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range=SAMPLE_RANGE_NAME_SELL).execute()
    values = result.get('values', [[]])
    if '' in values[0]:
        result = values[0].index("") + 1
        values[0][values[0].index("")] = targetCompanyID
        lib_update = {'values': values}
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME_SELL, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
        responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME_TARGET, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

        return result
    else:
        if len(values) < 5:
            values[0].append(f'''="{targetCompanyID}"''')
            lib_update = {'values': values}
            responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME_SELL, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
            responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME_TARGET, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
            return(len(values[0]))
    return 0

def ChangeConnectTargetAccount(targetCompanyID, spreadSheetPositon, spreadSheetTargetPosition):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
    SAMPLE_RANGE_NAME_SELL = f"Продажи 2!H{spreadSheetPositon}:L{spreadSheetPositon}"
    SAMPLE_RANGE_NAME_TARGET = f"Таргет 2!I{spreadSheetPositon}:M{spreadSheetPositon}"
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    lib_update = {'values': [[None for i in range(5)]]}
    lib_update['values'][0][spreadSheetTargetPosition - 1] = targetCompanyID
    responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME_SELL, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME_TARGET, valueInputOption = 'USER_ENTERED', body = lib_update).execute()

def ClearConcertTemplateTargetTable(targetCompanyID, spreadSheetPositon, spreadSheetTargetPosition):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
    SAMPLE_RANGE_NAME_SELL = f"Продажи 2!H{spreadSheetPositon}:L{spreadSheetPositon}"
    SAMPLE_RANGE_NAME_TARGET = f"Таргет 2!I{spreadSheetPositon}:M{spreadSheetPositon}"
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    lib_update = {'values': [[None for i in range(5)]]}
    lib_update['values'][0][spreadSheetTargetPosition - 1] = ""
    responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_SALE, range = SAMPLE_RANGE_NAME_SELL, valueInputOption = 'USER_ENTERED', body = lib_update).execute()
    responce =  service.update(spreadsheetId = SAMPLE_SPREADSHEET_ID_TARGET, range = SAMPLE_RANGE_NAME_TARGET, valueInputOption = 'USER_ENTERED', body = lib_update).execute()




