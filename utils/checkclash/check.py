import requests
import json


def check(alive, proxy, apiurl, sema, timeout, testurl):
    try:
        r = requests.get(url=apiurl + '/proxies/' + str(proxy['name']) + '/delay?url='+testurl+'&timeout=' + str(timeout), timeout=10)
        print('text ='+str(r.text)+'\n')
        response = json.loads(r.text)
        if response['delay'] > 0:
            alive.append(proxy)
    except:
        pass
    sema.release()
