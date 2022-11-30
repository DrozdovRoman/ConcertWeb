import vk_api

# Входные Данные:
# Api Token клиента формата: 
    # targetTockentInfo = {
        #     "Unique Name" :
        #         {
        #         'version' : "Версия VK API",
        #         'token' : "Ваш VK API TOKEN" ,
        #         }
    # }
# Шаблон Запроса
    # targetDataInfo = {
        # "settings" : 
        # {
        #     "account_id": Аккаунт ID,
        #     "ids_type" : Тип запршиваемых объектов,
        #     "period" : Способ группировки данных по датам,
        #     "date_from" : Указание начальной даты отсчета,
        #     "date_to" : Указание конечной даты отчета,
        #     "ids" : ID кампании
        # }

# Выходные Данные:
    # Массив из двух элементов:
        # 1) ID кампании
        # 2) Сумма потраченная за указанный период

def GetTarget(targetTockentInfo, targetDataInfo):
    try:
        VK_API_TOKEN = targetTockentInfo["targetRoman"]["token"]
        session = vk_api.VkApi(token = VK_API_TOKEN)
        vkTargetSession = session.get_api()
        result = vkTargetSession.ads.getStatistics(account_id = targetDataInfo["settings"]["account_id"], ids_type = targetDataInfo["settings"]["ids_type"],
        period = targetDataInfo["settings"]["period"], date_from = targetDataInfo["settings"]["date_from"], date_to = targetDataInfo["settings"]["date_to"],
        ids = targetDataInfo["settings"]["ids"])
        spentSumArray = [[element["id"], float(element["stats"][0].get("spent",0))] if len(element["stats"]) != 0 else [element["id"], None] for element in result] 
        return spentSumArray
    except:
        return(["Error!","Error!"])

