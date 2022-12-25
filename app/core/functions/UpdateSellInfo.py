from .SellFunctions.QticketsAuth import CreateSession
from .AccountInfo.PasswordQtickets import QticketsAccountInfo
from .SellFunctions.QticketsGetSalesTotal import QticketsGetSalesTotal
from .SellFunctions.QticketsGetSalesDate import QticketsGetSalesDate
from datetime import datetime,timedelta

def GetSell(sellInfo, date):
    session = CreateSession(QticketsAccountInfo)
    QticketsSalesDict = dict()
    for element in sellInfo:
        if (QticketsSalesDict.get(element['qticketsAccountName'])):
            QticketsSalesDict[element['qticketsAccountName']].append({'sellId' : element['qticketsConcertID'], 'pushka' : False})
        else:
            QticketsSalesDict[element['qticketsAccountName']] = [{'sellId' : element['qticketsConcertID'], 'pushka' : False}]
    date = date.strftime('%d.%m.%Y')
    result_overall = QticketsGetSalesTotal(session,QticketsSalesDict)
    result_yesterday = QticketsGetSalesDate(session,QticketsSalesDict,date, date)
    for x in sellInfo:
        for y in result_overall[x['qticketsAccountName']]:
            if y['sellId'] == x['qticketsConcertID']:
                x['result_overall'] = y['sellInfo']

        for z in result_yesterday[x['qticketsAccountName']]:
            if z['sellId'] == x['qticketsConcertID']:
                x['result_date'] = z['sellInfo']

    return(sellInfo)


# [{'id': 1, 'qticketsConcertID': '272612', 'qticketsAccountName': 'admin11', 'cat_id': 2},
# {'id': 2, 'qticketsConcertID': '279249', 'qticketsAccountName': 'admin11', 'cat_id': 6},
# {'id': 3, 'qticketsConcertID': '262519', 'qticketsAccountName': 'domino.dya@mail.ru', 'cat_id': 6}]

# {'admin11': [{'sellId': '272612', 'sellInfo': {'totalResult': ['195', 304560], 'refundResult': [0, 0], 'delWhithoutRefundResult': ['8', 12528], 'giftTicketResult': [0, 0]}}, {'sellId': '279249', 'sellInfo': {'totalResult': ['47', 109668], 'refundResult': [0, 0], 'delWhithoutRefundResult': [0, 0], 'giftTicketResult': [0, 0]}}], 'domino.dya@mail.ru': [{'sellId': '262519', 'sellInfo': {'totalResult': ['404', 396265], 'refundResult': [0, 0], 'delWhithoutRefundResult': ['3', 3348], 'giftTicketResult': ['120', 0]}}], 'psu.ekm1-2@yandex.ru': []}