import datetime
import re
import sys

import requests

start_date_i = [int(i) for i in sys.argv[1].split("-")]
end_date_i = [int(i) for i in sys.argv[2].split("-")]
# 创建起始日期和结束日期
start_date = datetime.date(*start_date_i)
end_date = datetime.date(*end_date_i)
# 计算日期范围的时间间隔
time_delta = end_date - start_date

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}
rsp = requests.get("https://www.flickr.com").text
apiKey = re.search('flickr\.api\.site_key.*?=.*?"([0-9a-f]+?)"', rsp).group(1)
reqId = re.search('flickr\.request\.id.*?=.*?"([0-9a-f\-]+?)"', rsp).group(1)
print(apiKey, reqId)
params = {
    "extras": "",
    "per_page": 500,
    "page": 1,
    "date": "",
    "viewerNSID": "",
    "method": "flickr.interestingness.getList",
    "csrf": "",
    "api_key": apiKey,
    "format": "json",
    "hermes": "1",
    "hermesClient": "1",
    "reqId": reqId,
    "nojsoncallback": "1",
}
f = open("./result.log", "w", encoding="utf-8");
for i in range(time_delta.days + 1):
    current_date = start_date + datetime.timedelta(days=i)
    date = current_date.strftime("%Y-%m-%d")
    params["date"] = date
    try:
        resp = requests.get(
            "https://api.flickr.com/services/rest",
            params=params,
            headers=headers
        )
        resp.raise_for_status()
        respjson = resp.json()
        if respjson["stat"] == "ok":
            print(date, respjson["photos"]["total"], len(respjson["photos"]["photo"]), file=f)
        else:
            print(date, "err", file=f)
    except:
        print(date, "error", file=f)
f.close()
