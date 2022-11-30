from bs4 import BeautifulSoup
import lxml

# Входные данные QticketsGetSalesDate:
    #   1)Словарь Авторизаций Аккаунтов формата:
    #       { "название аккаунта" : "переменная сессии аккаунта"}
    #   2)Словарь Данных Аккаунтов формата:
        # {
        #     "название аккаунта" : 
        # [
        #   { "sellid" : "номер id", "pushka" : "True/False"},
        #   { "sellid" : "номер id", "pushka" : "True/False"}, ...
        # ], ...
        # }
    #   3) Дата начала диапазона формата string : "01.01.2000"
    #   3) Дата конца диапазона формата string : "02.02.2002"

# Выходные данные QticketsGetSalesDate:
    # Словарь Продаж Билетов за все время формата:
    # { "название аккаунта" : 
    #   [
            # {
            # "sellId" : "номер id",
            # "sellInfo" : 
            #   {
                # Первые два пункта можно добавить при желании
                # "delWhithoutRefundResult" : [кол-во билетов, сумма билетов], - Кол-во билетов без возврата денежных средств
                # "giftTicketResult" : [кол-во билетов, сумма билетов] - Кол-во бесплатных билетов
                # "totalResult" : [кол-во билетов, сумма билетов], - Итоговое кол-во билетов
                # "refundResult" : [кол-во билетов, сумма билетов], - Кол-во возвратов билетов
            #   }
            # }, ...
    #   ], ...
    # }

def QticketsGetSalesDate(accountSessionDict, qticketsAccountData, dateFrom, dateTo):
    resultData = {}
    for accountName in accountSessionDict.keys(): # Проходимся по всем элементам словаря сессий
        resultData.update({accountName : None})
        dataArray = []
        accountIds = qticketsAccountData.get(accountName) # Запрашиваем концерты находящиеся в текущей сессии
        if (accountIds != None):
            for concertInfo in accountIds:
                link = "https://qtickets.app/stats/show/" + concertInfo["sellId"] + "?date_from=" + dateFrom + "&date_to=" + dateTo
                session = accountSessionDict[accountName]
                pageSoup = BeautifulSoup(session.get(link).text, 'lxml')
                dataArray.append({
                    "sellId" : concertInfo["sellId"],
                    "sellInfo" : getSalesInformation(pageSoup)
                })
        resultData[accountName] = dataArray
    return(resultData)


def QticketsGetSalesDateTicket(pageSoup):
    result = {
        "totalTicket" : 0,
        "refundTicket" : 0,
        "delWithoutRefundTicket" : 0,
        "giftTicket" : 0
    }

    try:
        findElement = pageSoup.find(class_ = "col-sm-6").find_all(style = "font-size: 16px; padding-bottom: 5px;")
        for element in findElement:
            if (element.text.split()[0] == "Продано" and element.text.split()[1] == "билетов:"):
                result["totalTicket"] = element.text.split()[2]
    except:
        result["totalTicket"] = "Error!"

    try:
        tempArrTicket = []
        tempArrElement = []
        findElement = pageSoup.find_all(class_ = "col-sm-6")[1].find_all(style="font-size: 18px; border-bottom: 1px solid silver; line-height: 32px; margin-bottom: 10px;")
        findTicket = pageSoup.find_all(class_ = "col-sm-6")[1].find_all(style="font-size: 16px; padding-bottom: 5px;")
        for element in findTicket:
            if (element.text.split()[0] == "Всего:"):
                tempArrTicket.append(element.text.split())
        for element in findElement:
            if ("Удалено без возврата" in element.text):
                tempArrElement.append("delWithoutRefundTicket")
            if ("Возвраты" in element.text):
                tempArrElement.append("refundTicket")
            if ("Продажи по пользователям" in element.text):
                tempArrElement.append("giftTicket")
        for i in range(len(tempArrTicket)):
            result[tempArrElement[i]] = tempArrTicket[i][1]
    except:
        result["refundTicket"] = "Error!"
        result["delWithoutRefundTicket"] = "Error!"
        result["giftTicket"] = "Error!"
    return result

def QticketsGetSalesDateSum(pageSoup):
    result = {
        "totalSum" : 0,
        "refundSum" : 0,
        "delWithoutRefundSum" : 0,
        "giftSum" : 0
    }

    try:
        totalSum = str()
        findElement = pageSoup.find(class_ = "col-sm-6").find_all(style = "font-size: 16px; padding-bottom: 5px;")
        for element in findElement:
            if (element.text.split()[0] == "Продано" and element.text.split()[1] == "билетов:"):
                arrSum = [temp for temp in element.text.split() if temp.isdigit()]
                for i in range(1,len(arrSum)):
                    totalSum += arrSum[i]
        result["totalSum"] = int(totalSum)
    except:
        result["totalSum"] = "Error!"

    try:
        tempArrSum = []
        tempArrElement = []
        findElement = pageSoup.find_all(class_ = "col-sm-6")[1].find_all(style="font-size: 18px; border-bottom: 1px solid silver; line-height: 32px; margin-bottom: 10px;")
        findSum = pageSoup.find_all(class_ = "col-sm-6")[1].find_all(style="font-size: 16px; padding-bottom: 5px;")
        for element in findSum:
            if (element.text.split()[0] == "Всего:"):
                arrSum = [temp for temp in element.text.split() if temp.isdigit()]
                tempArrSum.append(int("".join(arrSum[1:])))
        for element in findElement:
            if ("Удалено без возврата" in element.text):
                tempArrElement.append("delWithoutRefundSum")
            if ("Возвраты" in element.text):
                tempArrElement.append("refundSum")
            if ("Продажи по пользователям" in element.text):
                tempArrElement.append("giftSum")
        for i in range(len(tempArrSum)):
            result[tempArrElement[i]] = tempArrSum[i]
    except:
        result["refundSum"] = "Error!"
        result["delWithoutRefundSum"] = "Error!"
        result["giftSum"] = "Error!"
    return result

def getSalesInformation(pageSoup):
    dictTicketInformation = QticketsGetSalesDateTicket(pageSoup)
    dictSumInformation = QticketsGetSalesDateSum(pageSoup)
    dictTotalInformation = {
        # Пункты можно добавить при необходимости! (Но в реализации кутикетса указываются возвраты не за день, а за весь промежуток)
        # "delWhithoutRefundResult" : [dictTicketInformation["delWithoutRefundTicket"],dictSumInformation["delWithoutRefundSum"]],
        "totalResult" : [dictTicketInformation["totalTicket"],dictSumInformation["totalSum"]],
        "giftTicketResult" : [dictTicketInformation["giftTicket"],dictSumInformation["giftSum"]],
        "refundResult" : [dictTicketInformation["refundTicket"],dictSumInformation["refundSum"]]
    }
    return dictTotalInformation
