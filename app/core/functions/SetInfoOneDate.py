from .UpdateTargetInfo import GetTarget
from .UpdateSellInfo import GetSell
from .GoogleSheetsFunctions.UpdateGoogleSheet import UpdateTable

def SetInfoOneDate(targetInfo, sellInfo, concertInfo, date):
    target = GetTarget(targetInfo, date)
    sell = GetSell(sellInfo, date)
    print(target)
    UpdateTable(target, sell, concertInfo, date)
    return ("Good")