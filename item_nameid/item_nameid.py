import time
import re
import requests
import json
import traceback

# you need set your steamLoginSecure
# go to https://steamcommunity.com/ - devtools - Application - Cookies - steamLoginSecure
steamLoginSecure = "76561198091105943%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MEQxMV8yMzA1QTFFNl84QTk3RiIsICJzdWIiOiAiNzY1NjExOTgwOTExMDU5NDMiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MDQ5NzIyMjIsICJuYmYiOiAxNjk2MjQ0NjYzLCAiaWF0IjogMTcwNDg4NDY2MywgImp0aSI6ICIwRTM0XzIzQzc3Q0I5XzJFNkJCIiwgIm9hdCI6IDE2OTIzNDE1NDEsICJydF9leHAiOiAxNzEwNDY0Mzg5LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiMzcuMjEyLjIwLjIwNSIsICJpcF9jb25maXJtZXIiOiAiMzcuMjEyLjIwLjIwNSIgfQ.sKB89VIRFXcfFWHPwNQdAAW03TIQLfG829nuZcvcqI_H2H6fSG3uM9iovUeMKFcNhkSc7L_HMYkpvnwi4EgKBg"
headers = {
    "cookie": "steamCountry=BY%257C5a7b253bec88d2d69b60d1946be18e62",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=1",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": f"ActListPageSize=10; enableSIH=true; sessionid=895ddab0d7669d9abfc2e400; timezoneOffset=10800,0; browserid=2944855789164494751; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A0%2C%22time_checked%22%3A1703081493%7D; steamCurrencyId=5; strInventoryLastContext=730_2; recentlyVisitedAppHubs=1966720%2C730; app_impressions=1966720@2_9_100000_|730@2_9_100006_100202|730@2_9_100006_100202|730@2_100100_100101_100106|1966720@2_9_100006_100202|730@2_9_100006_100202|730@2_9_100006_100202; steamCountry=BY%7C9e868d2c50e6f579dd7e8f980dd99e2e; steamLoginSecure={steamLoginSecure}",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "sec-ch-ua": "^\^Not_A",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\^Windows^^"
}
gameID = '570'  # if you need dota items
# gameID = '730'       # if you need cs 2 items
start = 0


def add_name_id(item, dictionaries):  # adds a new item in our dictionary
    try:
        url = f'https://steamcommunity.com/market/listings/{gameID}/{item}'  # link added item
        while True:
            response = requests.get(url, headers=headers)
            if response.status_code == 429:  # if many requests - pause
                print('429 code - pause 620')
                time.sleep(620)
                continue
            break
        html_cont = response.text
        need_item = re.search(r'Market_LoadOrderSpread.+? (\d+) ', html_cont)
        dictionaries.update({item: need_item.group(1)})  # if we found nameid of item adds him
        print('we found a new item', item, need_item.group(1))
    except AttributeError:  # in another case it's item don't sell
        dictionaries.update({item: 'There are no listings for this item.'})
        print(item, 'There are no listings for this item.')
    except:  # errors i don't encountered
        traceback.print_exc()
        print(response.status_code, 'except')


while True:  # looking for max count items
    total_count = requests.get(
        'https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc'
        '&appid=' + gameID + '&norender=1&start=0&count=100',
        headers=headers)
    total_count = total_count.json()
    if len(total_count['results']) == 0:  # if we have a bad response - repeat
        continue
    total_count = total_count['total_count']
    print(total_count)
    break

with open('output_dota.txt', 'r', encoding='utf-8') as file:  # if you need work with dota items
    allItemNames = json.load(file)  # takes current items

# with open('output_cs_go.txt', 'r', encoding='utf-8') as file:  # if you need work with cs_2 items
#     allItemNames = json.load(file)

while True:  # look every 50 items and add new
    allItemsGet = requests.get(
        'https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc'
        '&appid=' + gameID + f'&norender=1&start={start}&count=100',
        headers=headers)
    allItems = allItemsGet.json()
    try:
        if total_count <= start:  # if we looks fully items - break
            break
        if allItemsGet.status_code == 429:  # if many requests - pause
            time.sleep(61)
            print(allItemsGet.status_code, '61')
            continue
        if len(allItems['results']) == 0:  # if we have a bad response - repeat
            continue
        for item in allItems['results']:  # sorting through 50 received items
            if item['hash_name'] in allItemNames:  # checking the item for it's presence on sale
                if allItemNames[item['hash_name']] == 'There are no listings for this item.':
                    add_name_id(item['hash_name'], allItemNames)
            else:
                add_name_id(item['hash_name'], allItemNames)  # adds a new item
        start += 50
        print(allItemsGet.status_code, start)
    except:  # errors that I have not encountered
        print(allItemsGet.status_code, allItems)
        time.sleep(7000)

with open('output_dota.txt', 'w', encoding='utf-8') as file:  # if you work with dota items
    json.dump(allItemNames, file, ensure_ascii=False)  # write down a new items

# with open('output_cs_go.txt', 'w', encoding='utf-8') as file:  # if you work with cs2 items
#     json.dump(allItemNames, file, ensure_ascii=False)

print(allItemNames, '\n', len(allItemNames))
