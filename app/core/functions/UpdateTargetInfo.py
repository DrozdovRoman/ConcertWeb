from .TargetFunctions.TargetSetTemplate import TargetDataInfoYesterday, TargetDataInfoOverall, TargetDataInfoDate
from .TargetFunctions.GetTargetVK import GetTargetVK
from .AccountInfo.TokenVkApi import targetTockentInfo

def GetTarget(targetInfo, date):

    account_dict = {}
    for element in targetInfo:
        if account_dict.get(element['targetAccountID']):
            account_dict[element['targetAccountID']].append(element['targetCompanyID'])
        else:
            account_dict[element['targetAccountID']] = [element['targetCompanyID']]

    result_date = []
    result_overall = []
    for cabinetID, CompanyArrID in account_dict.items():
        date_temp = TargetDataInfoDate(int(cabinetID), CompanyArrID, date)
        overall_temp = TargetDataInfoOverall(int(cabinetID), CompanyArrID)
        result_date.extend(GetTargetVK(targetTockentInfo, date_temp))
        result_overall.extend(GetTargetVK(targetTockentInfo, overall_temp))
    print(result_date)
    print("xxx")
    for x in result_date:
        for y in targetInfo:
            if str(x[0]) == y['targetCompanyID']:
                y['sum_date'] = x[1]

    for x in result_overall:
        for y in targetInfo:
            if str(x[0]) == y['targetCompanyID']:
                y['sum_overall'] = x[1]
    return targetInfo