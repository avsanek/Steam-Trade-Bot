from start_set import take_orders, take_item_nameid, calculate_relevance, check_sell_or_buy_items, check_gray_items

steamLoginSecure = ""
sessionid = ""

import time
start = time.time()  ##
count_total = 0  ##
count_gray_items = 0
time_to_sleep = 5.1


while True:
    items_orders = take_orders(steamLoginSecure, sessionid)  # get a complete list of orders
    for item in items_orders:
        print(item)
        item_nameid = take_item_nameid(item[0], item[1])  #  get item_nameid of item for checking relevance of item
        if item_nameid is None:
            continue
        calculate_relevance_ = calculate_relevance(steamLoginSecure, sessionid, item_nameid, item[2], item[1], item[0], item[3])  # checking relevance of item
        count_total += 1
        print(f'Time norm_item: {(time.time() - start):.03f}s', count_total)
        print(item, item_nameid, calculate_relevance_)
        time.sleep(time_to_sleep)

    check_sell_or_buy_items_ = check_sell_or_buy_items(steamLoginSecure, sessionid, start, count_total, time_to_sleep)  # check purchased or sold items for good profit
    count_total = check_sell_or_buy_items_[1]
    print('check_sell_or_buy_items_', check_sell_or_buy_items_[0], count_total)

    count_gray_items += 1
    if count_gray_items == 2:  # every second iteration we do this
        check_gray_items_ = check_gray_items(steamLoginSecure, sessionid, start, count_total, time_to_sleep)  # check gray_items to good profit or if have min need profit
        count_total = check_gray_items_[1]
        print('check_gray_items_', check_gray_items_, count_total)
        count_gray_items = 0



