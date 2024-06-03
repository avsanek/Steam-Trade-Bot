import sys
import io
import traceback
import requests
import time
import json
from bs4 import BeautifulSoup
from test_delay import response_myhistory, take_assetid, take_item_nameid, calculate_price, sell_item

steamLoginSecure = ""
sessionid = ""



response = response_myhistory(steamLoginSecure, sessionid)  # get json myhistory trade


def add_to_the_intermediate_base(row, current_base, status=None):  # add to the intermediate data_base purchased or
    item_name = row.find('span', class_='market_listing_item_name').text.strip()                         #  sold item
    item_price = row.find('span', class_='market_listing_price').text.strip()
    item_price = float(item_price.replace(",", ".").replace(" pуб.", ""))
    item_info = [item_name, item_price]
    if status == "add_item":  # it's need what li find out which db need use - cs_2 or dota
        item_game_name = row.find('span', class_='market_listing_game_name').text.strip()
        item_info.append(item_game_name)
    print(text_buy_or_sell_item, item_info[0], item_info[1])
    current_base.append(item_info)


def update_base(our_total_count, total_count=None, status=None):  # update base
    if status == 'Old':  # if we need update only count of transactions
        our_total_count['total_count'] = total_count
    elif status == 'New':  # if we need to do a new_base
        our_total_count['total_count'] = total_count
        our_total_count['assets'] = {}
        our_total_count['make_money'] = 0
    with open('main_base.txt', 'w', encoding='utf-8') as file:
        json.dump(our_total_count, file, ensure_ascii=False)


with open('main_base.txt', 'r', encoding='utf-8') as file:  # checking have whether new base
    our_total_count = json.load(file)
    if our_total_count['total_count'] == "New_base":
        update_base(our_total_count, response['total_count'], 'New')

count = 0
while True:  # here main objective it's check to changes response['total_count'] and after we look this was a buy
    response = response_myhistory(steamLoginSecure, sessionid)                                     #  or sold items
    with open('main_base.txt', 'r', encoding='utf-8') as file:
        our_total_count = json.load(file)
        count_items_for_check = response['total_count'] - our_total_count['total_count']
        print('item for checking', count_items_for_check)
        # count_items_for_check = 5  # plug
        if count_items_for_check:
            if count_items_for_check < 500:  # if < 500 we do check so much new transactions we have
                update_base(our_total_count, response['total_count'], 'Old')
            elif count_items_for_check > 500:  # if > 500 transactions we can't process so more and we do refresh
                update_base(our_total_count, response['total_count'], 'New')                           #  the base
                time.sleep(15)
                continue
        else:
            time.sleep(15)
            continue  # if don't have more a new transactions look again

    soup = BeautifulSoup(response['results_html'], 'lxml')
    purchased_items = []
    sold_items = []

    for row in soup.find_all('div', class_='market_recent_listing_row')[:count_items_for_check]:  # takes all rows of myhisory
        text_buy_or_sell_item = row.find('div', class_='market_listing_gainorloss').text.strip()  # found sold or purchased items
        if text_buy_or_sell_item in ['+', '-']:
            if text_buy_or_sell_item == '+':  # add to the intermediate data_base purchased item
                add_to_the_intermediate_base(row, purchased_items, "add_item")
            else:
                add_to_the_intermediate_base(row, sold_items)  # add to the intermediate data_base sold item


    if sold_items:
        for item in sold_items:  # delete sold items and measure profit
            if item[0] in our_total_count["assets"]:
                if len(our_total_count["assets"][item[0]]) == 1:
                    our_total_count["make_money"] = our_total_count["make_money"] + item[1] - our_total_count["assets"][item[0]][0]
                    our_total_count["assets"].pop(item[0], None)
                else:
                    our_total_count["make_money"] = our_total_count["make_money"] + item[1] - max(our_total_count["assets"][item[0]])
                    index_max_item = our_total_count["assets"][item[0]].index(max(our_total_count["assets"][item[0]]))
                    our_total_count["assets"][item[0]].pop(index_max_item)
        update_base(our_total_count)  # make changes

    for item in purchased_items:  # put the purchased item up for sale
        assetid = take_assetid(item[0], steamLoginSecure, sessionid, item[2]) #  get assetid item from inventory for selling to market
        print(item, f'assetid {assetid}')  # assetid[0] = assetid, assetid[1] = market_hash_name
        if assetid is None:
            continue
        item_nameid = take_item_nameid(assetid[1], item[2])  # get item_nameid of item for calculate the price for selling
        print(f'item_nameid {item_nameid}')
        count += 1
        price_to_sell = calculate_price(steamLoginSecure, sessionid, item_nameid, item[1], item[0])  # calculate price for selling
        print(f'price_to_sell {price_to_sell}', count)
        if price_to_sell is None:
            with open('logi.txt', 'a') as logi:
                logi.write(f'{item[0]} item_nameid {item_nameid} price_to_sell None \n')
            continue
        status_sell_item = sell_item(steamLoginSecure, sessionid, item[2], assetid[0], price_to_sell)  # put item to steam market place
        if status_sell_item is True:
            if item[0] not in our_total_count["assets"]:
                our_total_count["assets"].update({item[0]: [item[1]]})
            else:
                our_total_count["assets"][item[0]].append(item[1])
            update_base(our_total_count)
            print(f'sell item {item[0]} for {price_to_sell}')


