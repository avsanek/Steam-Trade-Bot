import requests
import time
import io
import traceback
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timedelta



secondary_items = []
gray_items = []
secondary_gray_items = []
delete_gray_items = []

def take_orders(steamLoginSecure, sessionid):  # get a complete list of orders
    while True:
        start = 0
        items_orders = []  # here save our orders
        try:
            url_orders = "https://steamcommunity.com/market/mylistings"
            querystring_orders = {"start": start, "count": "100"}
            headers_orders = {
                "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
                "Accept-Language": "en-US,en;q=1",
                "Connection": "keep-alive",
                "Cookie": f"ActListPageSize=30; sessionid={sessionid}; timezoneOffset=10800,0; browserid=2934724684930533469; steamCurrencyId=5; Steam_Language=english; app_impressions=753@2_100100_100101_100106|730@2_9_100006_100202|269670@2_100300_100500__100503|377160@2_100300_100500__100506|570@2_100300_100500__100509|2532550@2_100300_100500__100503|1850570@2_100300_100500__100503|730@2_100100_100101_100106; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A0%2C%22time_checked%22%3A1708012020%7D; recentlyVisitedAppHubs=730%2C1568590; steamCountry=BY%7Cee1052d42c86071b49adc409234aa2c0; steamLoginSecure={steamLoginSecure}; strInventoryLastContext=570_2",
                "Referer": "https://steamcommunity.com/market/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "X-KL-kfa-Ajax-Request": "Ajax_Request",
                "X-Prototype-Version": "1.7",
                "X-Requested-With": "XMLHttpRequest",
                "sec-ch-ua": "^\^Not_A",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "^\^Windows^^"
            }
            response = requests.request("GET", url_orders, headers=headers_orders, params=querystring_orders)
            if response.status_code != 200:
                print(f'response.status_code != 200 time.sleep(10) {response.status_code}')
                time.sleep(10)
                continue
            response_json = response.json()
            soup = BeautifulSoup(response_json['results_html'], 'lxml')
            items_orders_dirty = soup.find_all('div', class_='my_listing_section market_content_block market_home_listing_table')  # take the block with orders
            for take_need_block in items_orders_dirty:  # sometimes show block "My listings awaiting confirmation" and need pick another block with orders
                block_name = take_need_block.find('span', class_='my_market_header_active').text.strip()
                if block_name == "My buy orders":
                    items_orders_dirty = take_need_block
            classes = ['market_listing_row', 'market_recent_listing_row']
            items_orders_dirty = items_orders_dirty.find_all('div', class_=classes)  # receive every order
            for item in items_orders_dirty:  # clear every order and take need info
                item_id = item.get('id').strip().replace("mybuyorder_", "")  # item_id is needed to delete an item
                item_name = item.find(class_='market_listing_item_name_link').text.strip()
                if 'Unknown item:' in item_name:
                    item_name = item_name.replace("Unknown item: ", '')
                item_game = item.find(class_='market_listing_game_name').text.strip()
                item_price = item.find(class_='market_listing_price').contents[-1].text.strip()
                item_price = float(item_price.replace(",", ".").replace(" pуб.", ""))
                items_orders.append([item_name, item_game, item_price, item_id])
            return items_orders
        except (ValueError, requests.exceptions.ConnectionError):
            print('ValueError take_orders')
            time.sleep(10)
        except:
            buffer = io.StringIO()
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(f"Error in take_orders, status_code {response}: {buffer.getvalue()}\n")
            traceback.print_exc()
            # time.sleep(30)



def get_item(steamLoginSecure, sessionid, item_name, price_total, appid):  # do a new order with a new price
    global secondary_items
    while True:
        try:
            url_get_item = "https://steamcommunity.com/market/createbuyorder"
            payload_get_item = f"sessionid={sessionid}&currency=5&appid={appid}&market_hash_name={item_name}&price_total={price_total}&quantity=1&=billing_state%3D&save_my_address=0"
            headers_get_item = {
                "Accept": "*/*",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": f"ActListPageSize=30; buy_orders=false; undefined=false; sessionid={sessionid}; timezoneOffset=10800,0; browserid=2934724684930533469; steamCurrencyId=5; Steam_Language=english; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A0%2C%22time_checked%22%3A1708012020%7D; steamCountry=BY%7C069a6323cb9105cab301fa93bf30bc11; recentlyVisitedAppHubs=730%2C1568590%2C570; app_impressions=753@2_100100_100101_100106|730@2_9_100006_100202|269670@2_100300_100500__100503|377160@2_100300_100500__100506|570@2_100300_100500__100509|2532550@2_100300_100500__100503|1850570@2_100300_100500__100503|730@2_100100_100101_100106|570@2_9_100000_|570@2_9_100000_; strInventoryLastContext=730_2; steamLoginSecure={steamLoginSecure}; tsTradeOffersLastRead=1683694588",
                "Origin": "https://steamcommunity.com",
                "Referer": "https://steamcommunity.com/market/listings/730/M4A4%20%7C%20Etch%20Lord%20%28Battle-Scarred%29",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "X-KL-kfa-Ajax-Request": "Ajax_Request",
                "sec-ch-ua": "^\^Not_A",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "^\^Windows^^"
            }

            response = requests.request("POST", url_get_item, data=payload_get_item.encode('utf-8'), headers=headers_get_item)
            if response.status_code != 200:
                print(f"get_item != 200 {response.status_code} {item_name}")
                time.sleep(5)
                continue
            response_json = response.json()
            if response.status_code == 200 and response_json["success"] == 1:
                return response_json["success"]
            elif response.status_code == 200 and response_json["success"] == 25:  # if we have orders more than we can afford, we remove secondary_items
                if secondary_items == []:
                    return 1
                secondary_items_to_remove = secondary_items[:10]
                secondary_items = secondary_items[10:]
                for item_to_remove in secondary_items_to_remove:
                    status_remove = remove_item(steamLoginSecure, sessionid, item_to_remove[0], item_to_remove[1])
                    print(f'пошло удаление {status_remove}')
            elif response.status_code == 200 and response_json["success"] == 29:  # we already have an active buy order for this item
                return 1
            elif response.status_code == 200 and response_json["success"] in [16, 40]:
                time.sleep(5)
                print(f"Error in get_item {item_name}: {response_json}, response.status_code {response.status_code}\n")
                continue
            else:
                with open('errors.txt', 'a') as logi:
                    logi.write(f"Error in get_item {item_name}: {response_json}, response.status_code {response.status_code}\n")
        except:
            buffer = io.StringIO()
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(
                    f"Error in get_item: {buffer.getvalue()}, response.status_code {response.status_code}\n")
            traceback.print_exc()

def remove_item(steamLoginSecure, sessionid, buy_orderid, item_name):
    while True:
        try:
            url_remove_item = "https://steamcommunity.com/market/cancelbuyorder"
            payload_remove_item = f"sessionid={sessionid}&buy_orderid={buy_orderid}"
            headers_remove_item = {
                "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "Connection": "keep-alive",
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": f"ActListPageSize=30; buy_orders=false; undefined=false; sessionid={sessionid}; timezoneOffset=10800,0; browserid=2934724684930533469; steamCurrencyId=5; Steam_Language=english; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A0%2C%22time_checked%22%3A1708012020%7D; steamCountry=BY%7C069a6323cb9105cab301fa93bf30bc11; recentlyVisitedAppHubs=730%2C1568590%2C570; app_impressions=753@2_100100_100101_100106|730@2_9_100006_100202|269670@2_100300_100500__100503|377160@2_100300_100500__100506|570@2_100300_100500__100509|2532550@2_100300_100500__100503|1850570@2_100300_100500__100503|730@2_100100_100101_100106|570@2_9_100000_|570@2_9_100000_; strInventoryLastContext=730_2; steamLoginSecure={steamLoginSecure}",
                "Origin": "https://steamcommunity.com",
                "Referer": "https://steamcommunity.com/market/listings/730/M4A4%20%7C%20Etch%20Lord%20%28Battle-Scarred%29",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "X-KL-kfa-Ajax-Request": "Ajax_Request",
                "X-Prototype-Version": "1.7",
                "X-Requested-With": "XMLHttpRequest",
                "sec-ch-ua": "^\^Not_A",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "^\^Windows^^"
            }

            response = requests.request("POST", url_remove_item, data=payload_remove_item, headers=headers_remove_item)
            if response.status_code != 200:
                print(f"remove_item != 200 {response.status_code} {item_name}")  ##  проблема в запросе сверху, он встаёт, пропустить его отдельно, если нет, думаем что с ним сделать
                time.sleep(5)
                continue
            response_json = response.json()
            if response.status_code == 200 and response_json["success"] == 1:
                return response_json["success"]
            elif response_json["success"] in [29, 79]:  # don't have order, don't have order
                return 1
            elif response_json["success"] in [16, 10]:  # batched request timeout
                print(response_json)
                continue
            else:
                with open('errors.txt', 'a') as logi:
                    logi.write(f"Error in remove_item {item_name}: {response_json}, response.status_code {response.status_code}\n")
        except:
            buffer = io.StringIO()
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(
                    f"Error in remove_item: {buffer.getvalue()}, response.status_code {response.status_code}\n")
            traceback.print_exc()



def refresh_data_base():  #  if data_base_items refresh, we resreshing our data_base
    with open('output_dota.txt', 'r', encoding='utf-8') as file:
        item_nameid_dota = json.load(file)
    with open('output_cs_go.txt', 'r', encoding='utf-8') as file:
        item_nameid_cs_go = json.load(file)

with open('output_dota.txt', 'r', encoding='utf-8') as file:
    item_nameid_dota = json.load(file)
with open('output_cs_go.txt', 'r', encoding='utf-8') as file:
    item_nameid_cs_go = json.load(file)

def take_item_nameid(item_name, game_name):  # get item_nameid of item for checking relevance of item
    while True:
        try:
            if game_name == 'Dota 2':
                # with open('output_dota.txt', 'r', encoding='utf-8') as file:
                #     item_nameid_dota = json.load(file)
                    return item_nameid_dota[item_name]
            elif game_name == 'Counter-Strike 2':
                # with open('output_cs_go.txt', 'r', encoding='utf-8') as file:
                #     item_nameid_cs_go = json.load(file)
                    return item_nameid_cs_go[item_name]
        except KeyError:
            print(f"Error in take_item_nameid item {item_name, game_name} - continue")
            with open('errors.txt', 'a') as logi:
                logi.write(f"Error in take_item_nameid item {item_name, game_name} - continue \n")
            return None
        except:
            buffer = io.StringIO()
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(f"Error in take_item_nameid: {buffer.getvalue()}\n")
            traceback.print_exc()
            return None




def buy_in_hour(cookies, name, game_id):  # number of purchases per day
    while True:
        try:
            coookies = {'steamLoginSecure': cookies}
            link = f"https://steamcommunity.com/market/pricehistory/?country=DE&currency=3&appid={game_id}&market_hash_name={name}"
            response = requests.get(link, cookies=coookies)
            if response.status_code != 200:
                continue
            site = response.json()  ## if site == []: continue
            if site == []:
                continue
            data_1 = site['prices'][-25:]
            now = datetime.now()
            interval = now - timedelta(hours=27)
            interval = interval.replace(minute=0, second=0, microsecond=0)
            for i in data_1:
                if interval >= datetime.strptime(i[0][0:14], '%b %d %Y %H'):
                    index = data_1.index(i)
                else:
                    break
            data = data_1[index+1:]
            all_item = 0
            solo_items = []
            for i in data:
                all_item += int(i[2])
                solo_items.append(int(i[2]))
            procent_items = []
            for i in solo_items:
                procent_items.append(round(i / (all_item / 100), 2))
            if any(i > 20 for i in procent_items):
                return False
            return all_item
        except:
            buffer = io.StringIO()
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(f"Error in buy_in_hour: {buffer.getvalue()} , response {response}\n")
            return None

def game_id(game_name):
    if game_name == 'Dota 2':
        return 570
    elif game_name == 'Counter-Strike 2':
        return 730

def coef_game(game_name):  # min_coef - min coefficient for don't kick order, max_coef - good coefficient for replace order, min_prof - need to calculate dop price
    if game_name == 'Dota 2':
        return 1.4, 1.7, 0.85
    elif game_name == 'Counter-Strike 2':
        return 2.2, 2.5, 1.25

def change_price(item_price):  # api_steam after point of price always to do 2 number and we need to do samething
    price_for_sell = str(item_price).split('.')
    if len(price_for_sell[-1]) == 1:
        price_for_sell[-1] = price_for_sell[-1] + '0'
    price_for_sell = ''.join(price_for_sell)
    return price_for_sell

def new_order(current_order_item, profit, min_prof):  # if current price good we do a new order with add price
    dop_price = profit // min_prof
    if dop_price <= 1:
        dop_price = 0.1
    elif dop_price <= 11:
        dop_price = 0.1 * dop_price
    else:
        dop_price = 0.1 * 11
    new_order_ = round(current_order_item + dop_price, 2)
    return new_order_

def coef_day_and_sell_items(response_json, steamLoginSecure, item_name, game_name):  # dividing all_sell_items by per_day
    try:
        all_sell_items_dirty = re.search(r'>(\d+)<', response_json['sell_order_summary'])
        all_sell_items = int(all_sell_items_dirty.group(1))  # the total number sell items
        per_day = buy_in_hour(steamLoginSecure, item_name, game_id(game_name))  # number of purchases per day
        if per_day is False:
            return False
        coef_day_and_sell_items = (round(all_sell_items / per_day, 2))
        return coef_day_and_sell_items
    except:
        buffer = io.StringIO()
        traceback.print_exc(file=buffer)
        with open('errors.txt', 'a') as logi:
            logi.write(f"Error in coef_day_and_sell_items - return 1.5: {buffer.getvalue()}\n")
        return 1.5

def relevance_of_item(response_json, price_item, min_coef, steamLoginSecure, sessionid, buy_orderid, item_name, game_name, Status=None):  # check current profit
    for sell_order in response_json['sell_order_graph']:
        if sell_order[1] >= 3:  # check third item
            price_without_taxe = round(sell_order[0] / 1.15, 2)
            profit = price_without_taxe - price_item
            coef_profit = round(profit / (price_item / 100), 2)
            if coef_profit < min_coef:  # if current profit less "min_coef" - clearing the order
                print(f'Убираем coef_profit {coef_profit} < {min_coef} %')
                gray_items.append([item_name, game_name])  # when item doesn't have good profit and the price has not dropped much, we will check him and use him when him stay a good again
                return remove_item(steamLoginSecure, sessionid, buy_orderid, item_name)  # if we have a not good profit we remove order
            else:
                print(f'Оставляем coef_profit {coef_profit} > {min_coef} %')
                if Status == 'base_off':  # add to base not relevant of items to when need kick them
                    print('В базу на отмену')
                    if [buy_orderid, item_name] not in secondary_items:
                        secondary_items.append([buy_orderid, item_name])
                return 1

def rearranging_the_item(response_json, current_order_item, max_coef, price_item, min_coef, steamLoginSecure, sessionid, buy_orderid, item_name, min_prof, game_name, check_till):  # check of item for have profit to rearrange it
    for sell_order in response_json['sell_order_graph']:
        price_without_taxe = round(sell_order[0] / 1.15, 2)
        profit = round(price_without_taxe - current_order_item, 2)
        coef_profit = round(profit / (current_order_item / 100), 2)
        if coef_profit >= max_coef:  # if have profit -  rearrange it
            print(f'Переставляем {coef_profit} >= {max_coef}')
            remove_item_status = remove_item(steamLoginSecure, sessionid, buy_orderid, item_name)  # if we found a good item with good profit we remove old order
            if remove_item_status == 1:
                new_order_ = new_order(current_order_item, profit, min_prof)  # if current price good we do a new order with add price
                change_price_ = change_price(new_order_)  # api_steam after point of price always to do 2 number and we need to do samething
                return get_item(steamLoginSecure, sessionid, item_name, change_price_, game_id(game_name))  # do a new order with a new price
            break
        if sell_order[1] >= check_till:  # if haven't profit - check profit with old price
            print(f'Нету {max_coef} %')
            return relevance_of_item(response_json, price_item, min_coef, steamLoginSecure, sessionid, buy_orderid, item_name, game_name, Status='base_off')


def calculate_relevance(steamLoginSecure, sessionid, item_nameid, price_item, game_name, item_name, buy_orderid):  # checking relevance of item
    url_item = "https://steamcommunity.com/market/itemordershistogram"
    querystring_item = {"country":"RU","language":"english","currency":"5","item_nameid":item_nameid,"two_factor":"0"}
    headers_item = {
        "cookie": "steamCountry=BY%257C37617d356840b5e6028fa9489d09881a; Steam_Language=english",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=1",
        "Connection": "keep-alive",
        "Cookie": f"ActListPageSize=30; buy_orders=false; sessionid={sessionid}; timezoneOffset=10800,0; browserid=2934724684930533469; steamCurrencyId=5; recentlyVisitedAppHubs=730; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A0%2C%22time_checked%22%3A1706258439%7D; app_impressions=753@2_100100_100101_100106|730@2_9_100006_100202|269670@2_100300_100500__100503|377160@2_100300_100500__100506|570@2_100300_100500__100509|2532550@2_100300_100500__100503|1850570@2_100300_100500__100503; Steam_Language=english; strInventoryLastContext=570_2; steamCountry=BY%7C99c08b4ef12a3151750bffe797e12e19; steamLoginSecure={steamLoginSecure}",
        "If-Modified-Since": "Thu, 08 Feb 2024 17:11:20 GMT",
        "Referer": "https://steamcommunity.com/market/listings/570/Scales%20of%20Incandescent%20Liturgy",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "X-KL-kfa-Ajax-Request": "Ajax_Request",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "^\^Not_A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\^Windows^^"
    }
    while True:
        try:
            response = requests.request("GET", url_item, headers=headers_item, params=querystring_item)
            response_json = response.json()
            if response_json["success"] in [16, 10]:  # bad response
                continue
            min_coef, max_coef, min_prof = coef_game(game_name)  # min_coef - min coefficient for don't kick order, max_coef - good coefficient for replace order
            current_order_item = response_json['buy_order_graph'][0][0]  # first sell_order of item
            my_order = round(price_item + 0.04, 2)  # our order with dop price
            coef_day_and_sell_items_ = coef_day_and_sell_items(response_json, steamLoginSecure, item_name, game_name)  # dividing all_sell_items by per_day
            if coef_day_and_sell_items_ is False:
                print("coef_day_and_sell_items_ > 35 remove_item")
                return remove_item(steamLoginSecure, sessionid, buy_orderid, item_name)
            if my_order < current_order_item:  # if our order less "first sell_order of item" at 0.04
                if coef_day_and_sell_items_ <= 1.2:  # if coef less 1.2 then we use a less strict algorithm
                    print('Меньше 1.2 кф', coef_day_and_sell_items_)
                    return rearranging_the_item(response_json, current_order_item, max_coef, price_item, min_coef, steamLoginSecure, sessionid, buy_orderid, item_name, min_prof, game_name, check_till=3)  # check of item for have profit to rearrange it
                else:
                    print('Больше 1.2 кф', coef_day_and_sell_items_)
                    return rearranging_the_item(response_json, current_order_item, max_coef, price_item, min_coef, steamLoginSecure, sessionid, buy_orderid, item_name, min_prof, game_name, check_till=1)  # check of item for have profit to rearrange it
            else:
                return relevance_of_item(response_json, price_item, min_coef, steamLoginSecure, sessionid, buy_orderid, item_name, game_name)  # check current profit


        except (ConnectionResetError, requests.exceptions.ConnectionError, TimeoutError):
            print('ConnectionResetError def error we good processed')
            time.sleep(10)
        except:
            buffer = io.StringIO()
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(f"Error in calculate_relevance: {buffer.getvalue()}, response.status_code {response.status_code} response {response.text}\n")
            traceback.print_exc()
            return None


def response_myhistory(steamLoginSecure, sessionid):  # get json myhistory trade
    url_myhistory = "https://steamcommunity.com/market/myhistory"
    querystring_myhistory = {"count": "500"}
    headers_myhistory = {
        "cookie": "steamCountry=BY%257C37617d356840b5e6028fa9489d09881a; Steam_Language=english",
        "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
        "Accept-Language": "en-US,en;q=1",
        "Connection": "keep-alive",
        "Cookie": f"ActListPageSize=10; enableSIH=true; sessionid={sessionid}; timezoneOffset=10800,0; browserid=2944855789164494751; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A0%2C%22time_checked%22%3A1703081493%7D; steamCurrencyId=5; strInventoryLastContext=730_2; recentlyVisitedAppHubs=1966720%2C730; app_impressions=1966720@2_9_100000_|730@2_9_100006_100202|730@2_9_100006_100202|730@2_100100_100101_100106|1966720@2_9_100006_100202|730@2_9_100006_100202|730@2_9_100006_100202; steamCountry=BY%7C9e868d2c50e6f579dd7e8f980dd99e2e; steamLoginSecure={steamLoginSecure}",
        "Referer": "https://steamcommunity.com/market/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-KL-kfa-Ajax-Request": "Ajax_Request",
        "X-Prototype-Version": "1.7",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "^\^Not_A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\^Windows^^"
    }
    while True:
        try:
            response = requests.request("GET", url_myhistory, headers=headers_myhistory, params=querystring_myhistory)
            response = response.json()
            if response['assets'] == []:
                print('response_myhistory durit')
                time.sleep(5)
                continue
            return response
        except (ConnectionResetError, ConnectionError, requests.exceptions.JSONDecodeError, requests.exceptions.ConnectionError):
            print('ConnectionResetError def error')
            buffer = io.StringIO()
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(f"ConnectionResetError def error in response_myhistory: {buffer.getvalue()}\n")
            time.sleep(30)
        except:
            buffer = io.StringIO()
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(f"Error in response_myhistory: {buffer.getvalue()}\n")
            traceback.print_exc()
            time.sleep(30)


def relevance_of_gray(response_json, current_order_item, min_coef, item_name, game_name, Status_remove=None, Status=None):  # check 7 add more item for min_profit
    for sell_order in response_json['sell_order_graph']:
        if sell_order[1] >= 7:  # check third item
            price_without_taxe = round(sell_order[0] / 1.15, 2)
            profit = price_without_taxe - current_order_item
            coef_profit = round(profit / (current_order_item / 100), 2)
            if coef_profit < min_coef:  # if current profit less "min_coef" - skip this
                print(f'Убираем coef_profit {coef_profit} < {min_coef} %')
                if Status_remove == "do it":  # we memorize gray item which need to delete
                    delete_gray_items.append([item_name, game_name])
                return 1
            else:
                print(f'Оставляем coef_profit {coef_profit} > {min_coef} %')
                if Status == 'base_off':  # add to base of gray items with min_profit (we check them after)
                    secondary_gray_items.append([item_name, game_name])
                return 1


def rearranging_the_gray(response_json, current_order_item, max_coef, min_coef, steamLoginSecure, sessionid, item_name, min_prof, game_name, Status_remove, Status, check_till):  # check of item for have profit to order it
    for sell_order in response_json['sell_order_graph']:
        price_without_taxe = round(sell_order[0] / 1.15, 2)
        profit = round(price_without_taxe - current_order_item, 2)
        coef_profit = round(profit / (current_order_item / 100), 2)
        if coef_profit >= max_coef:  # if have profit -  get order
            print(f'Переставляем {coef_profit} >= {max_coef}')
            new_order_ = new_order(current_order_item, profit, min_prof)  # if current price good we do a new order with add price
            change_price_ = change_price(new_order_)  # api_steam after point of price always to do 2 number and we need to do samething
            if Status_remove == "do it":  # we memorize gray item which need to delete
                delete_gray_items.append([item_name, game_name])
            return get_item(steamLoginSecure, sessionid, item_name, change_price_, game_id(game_name))  # do a new order with a new price
        if sell_order[1] >= check_till:  # if haven't profit - check profit for min profit to stay it's item
            print(f'Нету {max_coef} %')
            return relevance_of_gray(response_json, current_order_item, min_coef, item_name, game_name, Status_remove, Status)


def calculate_relevance_gray(steamLoginSecure, sessionid, item_nameid, game_name, item_name, Status_remove=None, Status=None):  # checking relevance of gray item
    url_item = "https://steamcommunity.com/market/itemordershistogram"
    querystring_item = {"country":"RU","language":"english","currency":"5","item_nameid":item_nameid,"two_factor":"0"}
    headers_item = {
        "cookie": "steamCountry=BY%257C37617d356840b5e6028fa9489d09881a; Steam_Language=english",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=1",
        "Connection": "keep-alive",
        "Cookie": f"ActListPageSize=30; buy_orders=false; sessionid={sessionid}; timezoneOffset=10800,0; browserid=2934724684930533469; steamCurrencyId=5; recentlyVisitedAppHubs=730; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A0%2C%22time_checked%22%3A1706258439%7D; app_impressions=753@2_100100_100101_100106|730@2_9_100006_100202|269670@2_100300_100500__100503|377160@2_100300_100500__100506|570@2_100300_100500__100509|2532550@2_100300_100500__100503|1850570@2_100300_100500__100503; Steam_Language=english; strInventoryLastContext=570_2; steamCountry=BY%7C99c08b4ef12a3151750bffe797e12e19; steamLoginSecure={steamLoginSecure}",
        "If-Modified-Since": "Thu, 08 Feb 2024 17:11:20 GMT",
        "Referer": "https://steamcommunity.com/market/listings/570/Scales%20of%20Incandescent%20Liturgy",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "X-KL-kfa-Ajax-Request": "Ajax_Request",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "^\^Not_A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\^Windows^^"
    }
    while True:
        try:
            response = requests.request("GET", url_item, headers=headers_item, params=querystring_item)
            response_json = response.json()
            if response_json["success"] == 16:  # bad response
                continue
            min_coef, max_coef, min_prof = coef_game(game_name)  # min_coef - min coefficient for don't kick order, max_coef - good coefficient for replace order
            current_order_item = response_json['buy_order_graph'][0][0]  # first sell_order of item
            print(item_name, game_name, current_order_item)
            coef_day_and_sell_items_ = coef_day_and_sell_items(response_json, steamLoginSecure, item_name, game_name)  # dividing all_sell_items by per_day
            if coef_day_and_sell_items_ is False and Status_remove == 'do it':
                delete_gray_items.append([item_name, game_name])
                return 1
            elif not coef_day_and_sell_items_ and Status_remove == 'base_off':
                return 1
            if coef_day_and_sell_items_ <= 1.2:  # if coef less 1.2 then we use a less strict algorithm
                print('Меньше 1.2 кф', coef_day_and_sell_items_)
                return rearranging_the_gray(response_json, current_order_item, max_coef, min_coef, steamLoginSecure, sessionid, item_name, min_prof, game_name, Status_remove, Status, check_till=3)  # check of item for have profit to get order
            else:
                print('Больше 1.2 кф', coef_day_and_sell_items_)
                return rearranging_the_gray(response_json, current_order_item, max_coef, min_coef, steamLoginSecure, sessionid, item_name, min_prof, game_name, Status_remove, Status, check_till=1)  # check of item for have profit to get order


        except (ConnectionResetError, TimeoutError, requests.exceptions.ConnectionError):
            buffer = io.StringIO()
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(f"Error in calculate_relevance_gray - we good processed: {buffer.getvalue()}, response.status_code {response.status_code}\n")
            traceback.print_exc()
            print('we good processed')
            time.sleep(10)
        except:
            buffer = io.StringIO()
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(f"Error in calculate_relevance_gray: {buffer.getvalue()}, response.status_code {response.status_code}\n")
            traceback.print_exc()
            return None

def hash_items(purchased_sold_items, response, game_name):  #  check api_hisory and take hash_name of item
    count = 0
    max_count = len(purchased_sold_items) - 1
    hash_items_ = []
    for item_history_info in response['assets'][str(game_id(game_name))]['2'].values():
        if item_history_info['status'] == 4 and item_history_info['name'] == purchased_sold_items[count]:
            hash_items_.append(item_history_info['market_hash_name'])
            count += 1
            if max_count < count:
                break
    return hash_items_

def update_base(our_total_count, total_count=None):  # update base
    our_total_count['total_count'] = total_count
    with open('main_base.txt', 'w', encoding='utf-8') as file:
        json.dump(our_total_count, file, ensure_ascii=False)

# потом try except добавить
def check_sell_or_buy_items(steamLoginSecure, sessionid, start, count_total, time_to_sleep):  # check purchased or sold items for good profit
    response = response_myhistory(steamLoginSecure, sessionid)  # here we check for have li a new transactions in api_history
    with open('main_base.txt', 'r', encoding='utf-8') as file:
        our_total_count = json.load(file)
        count_items_for_check = response['total_count'] - our_total_count['total_count']
        print('item for checking', count_items_for_check)  # потом убрать
        if count_items_for_check:
            if count_items_for_check < 500:  # if < 500 we do check so much new transactions we have
                update_base(our_total_count, response['total_count'])
            elif count_items_for_check > 500:  # if > 500 transactions we can't process so more and we do refresh
                update_base(our_total_count, response['total_count'])                           #  the base
                return 1, count_total
        else:
            return 1, count_total

    soup = BeautifulSoup(response['results_html'], 'lxml')
    purchased_sold_dota = []
    purchased_sold_cs = []
    for row in soup.find_all('div', class_='market_recent_listing_row')[:count_items_for_check]:  # takes all rows of myhisory
        text_buy_or_sell_item = row.find('div', class_='market_listing_gainorloss').text.strip()  # found sold or purchased items
        if text_buy_or_sell_item in ['+', '-']:  # take sold or purchased items
            item_name = row.find('span', class_='market_listing_item_name').text.strip()
            item_game_name = row.find('span', class_='market_listing_game_name').text.strip()
            if item_game_name == 'Dota 2':  # Dota items
                purchased_sold_dota.append(item_name)
            elif item_game_name == 'Counter-Strike 2':  # cs items
                purchased_sold_cs.append(item_name)

    hash_dota_items, hash_cs_items = [], []  # need for take a hash_name of item
    count_for_game = 0
    for purchased_sold_items in (purchased_sold_dota, purchased_sold_cs):  # api_history have 2 different column about that need work apart with dota and cs items
        count_for_game += 1
        if purchased_sold_items:
            if count_for_game == 1:
                hash_dota_items = hash_items(purchased_sold_items, response, 'Dota 2')  # check api_hisory and take hash_name of item
            elif count_for_game == 2:
                hash_cs_items = hash_items(purchased_sold_items, response, 'Counter-Strike 2')  # check api_hisory and take hash_name of item

    hash_dota_items, hash_cs_items = list(set(hash_dota_items)), list(set(hash_cs_items))  # delete same items
    hash_dota_items = [[item, 'Dota 2'] for item in hash_dota_items]  # add to item him game_name
    hash_cs_items = [[item, 'Counter-Strike 2'] for item in hash_cs_items]  # add to item him game_name
    print(hash_dota_items, hash_cs_items, 'hash_dota_cs_items')

    for hash_gray_items in (hash_dota_items, hash_cs_items):  # check hash_dota_items, hash_cs_items to good profit or if have min need profit add to gray_items
        for hash_gray_item in hash_gray_items:
            count_total += 1  # убрать
            calculate_relevance_gray(steamLoginSecure, sessionid, take_item_nameid(hash_gray_item[0], hash_gray_item[1]), hash_gray_item[1], hash_gray_item[0], Status='base_off')
            print(f'Time hash_dota_cs_items: {(time.time() - start):.03f}s', count_total)
            time.sleep(time_to_sleep)

    return 1, count_total

def check_gray_items(steamLoginSecure, sessionid, start, count_total, time_to_sleep):  # check gray_items to good profit or if have min need profit
    global delete_gray_items, secondary_gray_items
    print(gray_items, 'gray_items')
    for gray_item in gray_items:
        count_total += 1  # убрать
        calculate_relevance_gray(steamLoginSecure, sessionid, take_item_nameid(gray_item[0], gray_item[1]), gray_item[1], gray_item[0], Status_remove='do it')
        print(f'Time gray_items: {(time.time() - start):.03f}s', count_total)
        time.sleep(time_to_sleep)

    for delete_item in delete_gray_items:  # delete used gray items
        gray_items.pop(gray_items.index(delete_item))
    delete_gray_items = []

    for secondary_gray_item in secondary_gray_items:  # add secondary_gray_items to gray_items
        gray_items.append(secondary_gray_item)
    secondary_gray_items = []

    print(gray_items, 'gray_items_after')
    print(secondary_items, gray_items, secondary_gray_items, delete_gray_items, 'Check for more have li some trables')

    return 1, count_total

