import datetime

def TargetDataInfoToday(account_id, idArray):
    ids = ",".join(idArray)
    targetDataInfo = {
        "settings" : 
        {
            "account_id": account_id,
            "ids_type" : "campaign",
            "period" : "day",
            "date_from" : str(datetime.date.today()),
            "date_to" : str(datetime.date.today()),
            "ids" : ids
        }
    }
    return targetDataInfo

def TargetDataInfoOverall(account_id, idArray):
    ids = ",".join(idArray)
    targetDataInfo = {
        "settings" : 
        {
            "account_id": account_id,
            "ids_type" : "campaign",
            "period" : "overall",
            "date_from" : "overall",
            "date_to" : "overall",
            "ids" : ids
        },
    }
    return targetDataInfo

def TargetDataInfoYesterday(account_id, idArray):
    ids = ",".join(idArray)
    targetDataInfo = {
        "settings" : 
        {
            "account_id": account_id,
            "ids_type" : "campaign",
            "period" : "day",
            "date_from" : str((datetime.date.today() - datetime.timedelta(days=1))),
            "date_to" : str((datetime.date.today() - datetime.timedelta(days=1))),
            "ids" : ids
        }
    }
    return targetDataInfo
    
