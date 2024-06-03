import requests
import time
import io
import traceback
import json


def game_id(game_name):
    if game_name == 'Dota 2':
        return '570'
    elif game_name == 'Counter-Strike 2':
        return '730'


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
                time.sleep(61)
                continue
            return response
        except (ConnectionResetError, requests.exceptions.ConnectionError):
            print('ConnectionResetError def error')
            time.sleep(10)
        except:
            buffer = io.StringIO()
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(f"Error in response_myhistory: {buffer.getvalue()}\n")
            traceback.print_exc()
            time.sleep(30)



def take_assetid(item, steamLoginSecure, sessionid, game_name):  #  get assetid item from inventory for selling to market
    url_inventory = f"https://steamcommunity.com/inventory/76561198091105943/{game_id(game_name)}/2"
    querystring_inventory = {"count": "2000", "market": "1"}  # maybe up to 5000
    headers_inventory = {
        "cookie": "steamCountry=BY%257C37617d356840b5e6028fa9489d09881a; Steam_Language=english",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=1",
        "Connection": "keep-alive",
        "Cookie": f"sessionid={sessionid}; timezoneOffset=10800,0; browserid=2934724684930533469; steamCurrencyId=5; recentlyVisitedAppHubs=730; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A0%2C%22time_checked%22%3A1706258439%7D; app_impressions=753@2_100100_100101_100106|730@2_9_100006_100202|269670@2_100300_100500__100503|377160@2_100300_100500__100506|570@2_100300_100500__100509|2532550@2_100300_100500__100503|1850570@2_100300_100500__100503; steamCountry=BY%7Ce146c3f7b82949c797ae81013bc373ed; steamLoginSecure={steamLoginSecure}; Steam_Language=english; strInventoryLastContext=570_2",
        "Referer": "https://steamcommunity.com/id/130840215/inventory?modal=1&market=1",
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
    try:
        while True:
            response = requests.request("GET", url_inventory, headers=headers_inventory, params=querystring_inventory)
            if response.status_code == 500:
                time.sleep(2)
                continue
            response = response.json()
            for info_inventory_item in response["descriptions"]:
                if "market_hash_name" in info_inventory_item:
                    if info_inventory_item["name"] == item:
                        index_inventory_item = response["descriptions"].index(info_inventory_item)
                        return response["assets"][index_inventory_item]["assetid"], info_inventory_item["market_hash_name"]
            return None
    except:
        buffer = io.StringIO()
        traceback.print_exc(file=buffer)
        with open('errors.txt', 'a') as logi:
            logi.write(f"Error in take_assetid: {buffer.getvalue()}\n")
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


def take_item_nameid(item_name, game_name):  # get item_nameid of item for calculate the price for selling
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
        refresh_data_base()
        if game_name == 'Dota 2':
                return item_nameid_dota[item_name]
        elif game_name == 'Counter-Strike 2':
                return item_nameid_cs_go[item_name]
    except:
        buffer = io.StringIO()
        traceback.print_exc(file=buffer)
        with open('errors.txt', 'a') as logi:
            logi.write(f"Error in take_item_nameid: {buffer.getvalue()}\n")
        traceback.print_exc()

def change_price(item_price):  # api_steam after point of price always to do 2 number and we need to do samething
    price_for_sell = item_price - 0.01  # for example 7.1 need to do 7.10
    price_for_sell = round(price_for_sell, 2)
    price_for_sell = str(price_for_sell).split('.')
    if len(price_for_sell[-1]) == 1:
        price_for_sell[-1] = price_for_sell[-1] + '0'
    price_for_sell = ''.join(price_for_sell)
    return price_for_sell

# mb check cookie if have some trables
def calculate_price(steamLoginSecure, sessionid, item_nameid, price_item, item_name):  # calculate price for selling
    # don't pay attention to the design, there was a lot of fine work here,
    # it was important for me to make it work correctly, because it's working with money.
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
    try:
        while True:
            response = requests.request("GET", url_item, headers=headers_item, params=querystring_item)
            response = response.json()
            if response["success"] == 16:  # bad response
                continue
            last_count = 0
            sell_order_graph = response['sell_order_graph']
            for item_prices in sell_order_graph:
                count_current_prices = item_prices[1] - last_count
                last_count = item_prices[1]
                price_without_taxe = round(item_prices[0] / 1.15, 2)
                profit = round(price_without_taxe - price_item, 2)
                print(count_current_prices, item_prices[0], round(item_prices[0] / 1.15, 2), round(profit, 2))
                if profit > 0:
                    if profit >= 0.5:
                        if count_current_prices >= 3:
                            print(item_prices, f'item_name: {item_name}')
                            print(f'counts: {count_current_prices}, price {item_prices[0]}, price_without_taxe {price_without_taxe}, price_item {price_item}, profit {profit} > 0.5 if count_current_prices >= 3: first')
                            with open('logi.txt', 'a') as logi:
                                logi.write(f'{item_prices}, item_name: {item_name} \ncounts: {count_current_prices}, price {item_prices[0]}, price_without_taxe {price_without_taxe}, price_item {price_item}, profit {profit} > 0.5 if count_current_prices >= 3: first\n')
                            return change_price(price_without_taxe)
                        elif count_current_prices == 2:
                            need_index = sell_order_graph.index(item_prices) + 1
                            second_price_without_taxe = round(sell_order_graph[need_index][0] / 1.15, 2)
                            second_profit = round(second_price_without_taxe - price_item, 2)
                            if profit * 3.24 <= second_profit:
                                print(item_prices, sell_order_graph[need_index], f'item_name: {item_name}')
                                print(f'counts: {count_current_prices}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, second_profit {second_profit} > 0.5 elif count_current_prices == 2: if profit * 3 second')
                                with open('logi.txt', 'a') as logi:
                                    logi.write(f'{item_prices}, {sell_order_graph[need_index]}, item_name: {item_name} \nsecond_price_without_taxe {second_price_without_taxe}, price_item {price_item}, second_profit {second_profit} > 0.5 elif count_current_prices == 2: if profit * 3 second\n')
                                return change_price(second_price_without_taxe)
                            else:
                                print(item_prices, sell_order_graph[need_index], f'item_name: {item_name}')
                                print(f'counts: {count_current_prices}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, profit {profit} > 0.5 elif count_current_prices == 2: else first')
                                with open('logi.txt', 'a') as logi:
                                    logi.write(f'{item_prices}, {sell_order_graph[need_index]}, item_name: {item_name} \nsecond_price_without_taxe {second_price_without_taxe}, price_item {price_item}, profit {profit} > 0.5 elif count_current_prices == 2: else first\n')
                                return change_price(price_without_taxe)
                        elif count_current_prices == 1:
                            need_index = sell_order_graph.index(item_prices) + 1
                            second_count = sell_order_graph[need_index][1] - last_count
                            if second_count >= 2:
                                second_price_without_taxe = round(sell_order_graph[need_index][0] / 1.15, 2)
                                second_profit = round(second_price_without_taxe - price_item, 2)
                                if profit * 1.8 <= second_profit:
                                    print(item_prices, sell_order_graph[need_index], f'item_name: {item_name}')
                                    print(f'counts: {count_current_prices}, second_count {second_count}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, second_profit {second_profit} > 0.5 elif count_current_prices == 1: if second_count >= 2: if profit * 1.8 second')
                                    with open('logi.txt', 'a') as logi:
                                        logi.write(
                                            f'{item_prices}, {sell_order_graph[need_index]}, item_name: {item_name} \ncounts: {count_current_prices}, second_count {second_count}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, second_profit {second_profit} > 0.5 elif count_current_prices == 1: if second_count >= 2: if profit * 1.8 second\n')
                                    return change_price(second_price_without_taxe)
                                else:
                                    print(item_prices, sell_order_graph[need_index], f'item_name: {item_name}')
                                    print(f'counts: {count_current_prices}, second_count {second_count}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, profit {profit} > 0.5 elif count_current_prices == 1: if second_count >= 2: else first')
                                    with open('logi.txt', 'a') as logi:
                                        logi.write(
                                            f'{item_prices}, {sell_order_graph[need_index]}, item_name: {item_name} \ncounts: {count_current_prices}, second_count {second_count}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, profit {profit} > 0.5 elif count_current_prices == 1: if second_count >= 2: else first\n')
                                    return change_price(price_without_taxe)
                            elif second_count == 1:
                                second_price_without_taxe = round(sell_order_graph[need_index][0] / 1.15, 2)
                                second_profit = round(second_price_without_taxe - price_item, 2)
                                if profit * 1.8 <= second_profit:
                                    third_price_without_taxe = round(sell_order_graph[need_index + 1][0] / 1.15, 2)
                                    profit_third = round(third_price_without_taxe - price_item, 2)
                                    if second_profit * 1.8 <= profit_third:
                                        print(item_prices, sell_order_graph[need_index], sell_order_graph[need_index + 1], f'item_name: {item_name}')
                                        print(f'counts: {count_current_prices}, second_count {second_count}, third_price {sell_order_graph[need_index + 1][0]}, third_price_without_taxe {third_price_without_taxe}, price_item {price_item}, profit_third {profit_third} > 0.5 elif count_current_prices == 1: elif second_count == 1: if profit * 1.8 third')
                                        with open('logi.txt', 'a') as logi:
                                            logi.write(
                                                f'{item_prices}, {sell_order_graph[need_index]}, {sell_order_graph[need_index + 1]} item_name: {item_name} \ncounts: {count_current_prices}, second_count {second_count}, third_price {sell_order_graph[need_index + 1][0]}, third_price_without_taxe {third_price_without_taxe}, price_item {price_item}, profit_third {profit_third} > 0.5 elif count_current_prices == 1: elif second_count == 1: if profit * 1.8 third\n')
                                        return change_price(third_price_without_taxe)
                                    else:
                                        print(item_prices, sell_order_graph[need_index], sell_order_graph[need_index + 1], f'item_name: {item_name}')
                                        print(f'counts: {count_current_prices}, second_count {second_count}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, second_profit {second_profit} > 0.5 elif count_current_prices == 1: elif second_count == 1: if profit * 1.8 second')
                                        with open('logi.txt', 'a') as logi:
                                            logi.write(
                                                f'{item_prices}, {sell_order_graph[need_index]}, {sell_order_graph[need_index + 1]} item_name: {item_name} \ncounts: {count_current_prices}, second_count {second_count}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, second_profit {second_profit} > 0.5 elif count_current_prices == 1: elif second_count == 1: if profit * 1.8 second\n')
                                        return change_price(second_price_without_taxe)
                                else:
                                    third_price_without_taxe = round(sell_order_graph[need_index + 1][0] / 1.15, 2)
                                    profit_third = round(third_price_without_taxe - price_item, 2)
                                    if profit * 3.24 <= profit_third:
                                        print(item_prices, sell_order_graph[need_index], sell_order_graph[need_index + 1], f'item_name: {item_name}')
                                        print(f'counts: {count_current_prices}, second_count {second_count}, third_price {sell_order_graph[need_index + 1][0]}, third_price_without_taxe {third_price_without_taxe}, price_item {price_item}, profit_third {profit_third} > 0.5 elif count_current_prices == 1: elif second_count == 1: else third')
                                        with open('logi.txt', 'a') as logi:
                                            logi.write(
                                                f'{item_prices}, {sell_order_graph[need_index]}, {sell_order_graph[need_index + 1]} item_name: {item_name} \ncounts: {count_current_prices}, second_count {second_count}, third_price {sell_order_graph[need_index + 1][0]}, third_price_without_taxe {third_price_without_taxe}, price_item {price_item}, profit_third {profit_third} > 0.5 elif count_current_prices == 1: elif second_count == 1: else third\n')
                                        return change_price(third_price_without_taxe)
                                    else:
                                        print(item_prices, sell_order_graph[need_index], sell_order_graph[need_index + 1], f'item_name: {item_name}')
                                        print(f'counts: {count_current_prices}, second_count {second_count}, third_price {sell_order_graph[need_index + 1][0]}, third_price_without_taxe {third_price_without_taxe}, price_item {price_item}, profit {profit} > 0.5 elif count_current_prices == 1: elif second_count == 1: else first')
                                        with open('logi.txt', 'a') as logi:
                                            logi.write(
                                                f'{item_prices}, {sell_order_graph[need_index]}, {sell_order_graph[need_index + 1]} item_name: {item_name} \ncounts: {count_current_prices}, second_count {second_count}, third_price {sell_order_graph[need_index + 1][0]}, third_price_without_taxe {third_price_without_taxe}, price_item {price_item}, profit {profit} > 0.5 elif count_current_prices == 1: elif second_count == 1: else first\n')
                                        return change_price(price_without_taxe)
                    elif profit < 0.5:
                        if count_current_prices >= 3:
                            print(item_prices, f'item_name: {item_name}')
                            print(f'counts: {count_current_prices}, price {item_prices[0]}, price_without_taxe {price_without_taxe}, price_item {price_item}, profit {profit} < 0.5 if count_current_prices >= 3: first')
                            with open('logi.txt', 'a') as logi:
                                logi.write(f'{item_prices}, item_name: {item_name} \ncounts: {count_current_prices}, price {item_prices[0]}, price_without_taxe {price_without_taxe}, price_item {price_item}, profit {profit} < 0.5 if count_current_prices >= 3: first\n')
                            return change_price(price_without_taxe)
                        elif count_current_prices == 2:
                            need_index = sell_order_graph.index(item_prices) + 1
                            second_price_without_taxe = round(sell_order_graph[need_index][0] / 1.15, 2)
                            second_profit = round(second_price_without_taxe - price_item, 2)
                            if second_profit >= 0.9:
                                print(item_prices, sell_order_graph[need_index], f'item_name: {item_name}')
                                print(f'counts: {count_current_prices}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, second_profit {second_profit} < 0.5 elif count_current_prices == 2: if profit >= 0.9: second')
                                with open('logi.txt', 'a') as logi:
                                    logi.write(
                                        f'{item_prices}, {sell_order_graph[need_index]}, item_name: {item_name} \ncounts: {count_current_prices}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, second_profit {second_profit} < 0.5 elif count_current_prices == 2: if profit >= 0.9: second\n')
                                return change_price(second_price_without_taxe)
                            else:
                                print(item_prices, sell_order_graph[need_index], f'item_name: {item_name}')
                                print(f'counts: {count_current_prices}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, profit {profit} < 0.5 elif count_current_prices == 2: else second')
                                with open('logi.txt', 'a') as logi:
                                    logi.write(
                                        f'{item_prices}, {sell_order_graph[need_index]}, item_name: {item_name} \ncounts: {count_current_prices}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, profit {profit} < 0.5 elif count_current_prices == 2: else second\n')
                                return change_price(price_without_taxe)
                        elif count_current_prices == 1:
                            need_index = sell_order_graph.index(item_prices) + 1
                            second_count = sell_order_graph[need_index][1] - last_count
                            if second_count >= 2:
                                second_price_without_taxe = round(sell_order_graph[need_index][0] / 1.15, 2)
                                second_profit = round(second_price_without_taxe - price_item, 2)
                                if second_profit >= 0.5:
                                    print(item_prices, sell_order_graph[need_index], f'item_name: {item_name}')
                                    print(f'counts: {count_current_prices}, second_count {second_count}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, second_profit {second_profit} < 0.5 elif count_current_prices == 1: if second_count >= 2: if profit >= 0.5 second')
                                    with open('logi.txt', 'a') as logi:
                                        logi.write(
                                            f'{item_prices}, {sell_order_graph[need_index]}, item_name: {item_name} \ncounts: {count_current_prices}, second_count {second_count}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, second_profit {second_profit} < 0.5 elif count_current_prices == 1: if second_count >= 2: if profit >= 0.5 second\n')
                                    return change_price(second_price_without_taxe)
                                else:
                                    print(item_prices, sell_order_graph[need_index], f'item_name: {item_name}')
                                    print(f'counts: {count_current_prices}, second_count {second_count}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, profit {profit} < 0.5 elif count_current_prices == 1: if second_count >= 2: else first')
                                    with open('logi.txt', 'a') as logi:
                                        logi.write(
                                            f'{item_prices}, {sell_order_graph[need_index]}, item_name: {item_name} \ncounts: {count_current_prices}, second_count {second_count}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, profit {profit} < 0.5 elif count_current_prices == 1: if second_count >= 2: else first\n')
                                    return change_price(price_without_taxe)
                            elif second_count == 1:
                                second_price_without_taxe = round(sell_order_graph[need_index][0] / 1.15, 2)
                                second_profit = round(second_price_without_taxe - price_item, 2)
                                if second_profit >= 0.5:
                                    third_price_without_taxe = round(sell_order_graph[need_index + 1][0] / 1.15, 2)
                                    profit_third = round(third_price_without_taxe - price_item, 2)
                                    if second_profit * 1.8 <= profit_third:
                                        print(item_prices, sell_order_graph[need_index], sell_order_graph[need_index+1], f'item_name: {item_name}')
                                        print(f'counts: {count_current_prices}, second_count {second_count}, third_price {sell_order_graph[need_index + 1][0]}, third_price_without_taxe {third_price_without_taxe}, price_item {price_item}, profit_third {profit_third} < 0.5 elif count_current_prices == 1: elif second_count == 1: if profit >= 0.5 third')
                                        with open('logi.txt', 'a') as logi:
                                            logi.write(
                                                f'{item_prices}, {sell_order_graph[need_index]}, {sell_order_graph[need_index+1]}, item_name: {item_name} \ncounts: {count_current_prices}, second_count {second_count}, third_price {sell_order_graph[need_index + 1][0]}, third_price_without_taxe {third_price_without_taxe}, price_item {price_item}, profit_third {profit_third} < 0.5 elif count_current_prices == 1: elif second_count == 1: if profit >= 0.5 third\n')
                                        return change_price(third_price_without_taxe)
                                    else:
                                        print(item_prices, sell_order_graph[need_index], sell_order_graph[need_index + 1], f'item_name: {item_name}')
                                        print(f'counts: {count_current_prices}, second_count {second_count}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, second_profit {second_profit} < 0.5 elif count_current_prices == 1: elif second_count == 1: if profit >= 0.5 second')
                                        with open('logi.txt', 'a') as logi:
                                            logi.write(
                                                f'{item_prices}, {sell_order_graph[need_index]}, {sell_order_graph[need_index+1]}, item_name: {item_name} \ncounts: {count_current_prices}, second_count {second_count}, second_price {sell_order_graph[need_index][0]}, second_price_without_taxe {second_price_without_taxe}, price_item {price_item}, second_profit {second_profit} < 0.5 elif count_current_prices == 1: elif second_count == 1: if profit >= 0.5 second\n')
                                        return change_price(second_price_without_taxe)
                                else:
                                    third_price_without_taxe = round(sell_order_graph[need_index + 1][0] / 1.15, 2)
                                    profit_third = round(third_price_without_taxe - price_item, 2)
                                    if profit_third >= 0.9:
                                        print(item_prices, sell_order_graph[need_index], sell_order_graph[need_index + 1], f'item_name: {item_name}')
                                        print(f'counts: {count_current_prices}, second_count {second_count}, third_price {sell_order_graph[need_index + 1][0]}, third_price_without_taxe {third_price_without_taxe}, price_item {price_item}, profit_third {profit_third} < 0.5 elif count_current_prices == 1: elif second_count == 1: else third')
                                        with open('logi.txt', 'a') as logi:
                                            logi.write(
                                                f'{item_prices}, {sell_order_graph[need_index]}, {sell_order_graph[need_index+1]}, item_name: {item_name} \ncounts: {count_current_prices}, second_count {second_count}, third_price {sell_order_graph[need_index + 1][0]}, third_price_without_taxe {third_price_without_taxe}, price_item {price_item}, profit_third {profit_third} < 0.5 elif count_current_prices == 1: elif second_count == 1: else third\n')
                                        return change_price(third_price_without_taxe)
                                    else:
                                        print(item_prices, sell_order_graph[need_index], sell_order_graph[need_index + 1], f'item_name: {item_name}')
                                        print(f'counts: {count_current_prices}, second_count {second_count}, third_price {sell_order_graph[need_index + 1][0]}, third_price_without_taxe {third_price_without_taxe}, price_item {price_item}, profit {profit} < 0.5 elif count_current_prices == 1: elif second_count == 1: else first')
                                        with open('logi.txt', 'a') as logi:
                                            logi.write(
                                                f'{item_prices}, {sell_order_graph[need_index]}, {sell_order_graph[need_index+1]}, item_name: {item_name} \ncounts: {count_current_prices}, second_count {second_count}, third_price {sell_order_graph[need_index + 1][0]}, third_price_without_taxe {third_price_without_taxe}, price_item {price_item}, profit {profit} < 0.5 elif count_current_prices == 1: elif second_count == 1: else first\n')
                                        return change_price(price_without_taxe)
    except:
        buffer = io.StringIO()
        traceback.print_exc(file=buffer)
        with open('errors.txt', 'a') as logi:
            logi.write(f"Error in calculate_price: {buffer.getvalue()}\n")
        traceback.print_exc()



def sell_item(steamLoginSecure, sessionid, game_name, assetid, price_to_sell):  # put item to steam market place
    url_sell = "https://steamcommunity.com/market/sellitem"
    payload_sell = f"sessionid={sessionid}&appid={game_id(game_name)}&contextid=2&assetid={assetid}&amount=1&price={price_to_sell}"
    headers_sell = {
        "cookie": "steamCountry=BY%257C37617d356840b5e6028fa9489d09881a; Steam_Language=english",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=1",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": f"ActListPageSize=30; sell_listings=false; sessionid={sessionid}; timezoneOffset=10800,0; browserid=2934724684930533469; steamCurrencyId=5; recentlyVisitedAppHubs=730; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A0%2C%22time_checked%22%3A1706258439%7D; Steam_Language=english; app_impressions=753@2_100100_100101_100106|730@2_9_100006_100202|269670@2_100300_100500__100503|377160@2_100300_100500__100506|570@2_100300_100500__100509|2532550@2_100300_100500__100503|1850570@2_100300_100500__100503|730@2_100100_100101_100106; steamCountry=BY%7C24e8cef0183178cdd21288000454bb5b; steamLoginSecure={steamLoginSecure}; strInventoryLastContext=730_2",
        "Origin": "https://steamcommunity.com",
        "Referer": "https://steamcommunity.com/profiles/76561198091105943/inventory",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "X-KL-kfa-Ajax-Request": "Ajax_Request",
        "sec-ch-ua": "^\^Not_A",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "^\^Windows^^"
    }
    while True:
        try:
            response = requests.request("POST", url_sell, data=payload_sell, headers=headers_sell)
            response_status = response.json()["success"]
            if response_status is True:
                return response_status
            else:
                print(f'response {response.status_code}, response_status{response_status}')
                time.sleep(10)
                continue
        except:
            buffer = io.StringIO()
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(f"Error in sell_item: {buffer.getvalue()}\n")
            traceback.print_exc()
            return None














