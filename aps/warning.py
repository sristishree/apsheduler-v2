import requests


def sendWarning(diagID):
    data = {
        "diagnosticsid" : diagID
    }
    url = 'http://mlapi2-svc/UI?caller=scheduler'
    res = requests.post(url, headers=headers, data=data)