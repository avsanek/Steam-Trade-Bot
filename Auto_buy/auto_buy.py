import requests
from datetime import datetime, timedelta
import traceback
import time
import io
from selenium.common.exceptions import NoSuchElementException

def buy_in_hour(cookies, name, game_id, buy_in_Hour):
    while True:
        try:
            count = 0
            coookies = {'steamLoginSecure': cookies}
            link = f"https://steamcommunity.com/market/pricehistory/?country=DE&currency=3&appid={game_id}&market_hash_name={name}"
            site = requests.get(link, cookies=coookies).json()
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
                procent_items.append(round(i/(all_item/100), 2))
            print(procent_items)
            if any(i > buy_in_Hour for i in procent_items):
                return False
            else:
                return procent_items
        except:
            count += 1
            buffer = io.StringIO()
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(f'Error in buy_in_hour: {buffer.getvalue()} \n')
            traceback.print_exc()
            if count > 3:
                return False


def error_max(browser, windows, By):
    try:
        browser.execute_script(f"window.open('')")
        windows['error_max'] = browser.window_handles[-1]
        browser.switch_to.window(windows['error_max'])
        browser.get('https://steamcommunity.com/market/')
        full_orders = browser.find_elements(By.CSS_SELECTOR, 'div.my_listing_section.market_content_block.market_home_listing_table:nth-child(n+4) span.item_market_action_button_contents')
        count_orders = 0
        for order in full_orders:
            order.click()
            count_orders += 1
            if count_orders == 10:
                break
        browser.close()
        del windows['error_max']
        browser.switch_to.window(windows['steam_auto'])
        print('error_max_srabotal')
        with open('errors.txt', 'a') as logi:
            logi.write(f'Error max srabotal \n')
    except:
        buffer = io.StringIO()
        traceback.print_exc(file=buffer)
        with open('errors.txt', 'a') as logi:
            logi.write(f'Error in error_max: {buffer.getvalue()} \n')
        traceback.print_exc()

def not_spisoc(browser, By, cookies, item, buy_in_Hour, game_prof, status, min_prof):
    while True:
        try:
            order = browser.find_element(By.CSS_SELECTOR, '#market_commodity_buyrequests span.market_commodity_orders_header_promote:nth-child(2)').text
            order = float(order.replace(",", ".").replace(" pуб.", ""))
            # order = float(order.replace("$", ""))
            print(order, 'order')
            sell = browser.find_element(By.CSS_SELECTOR, '#market_commodity_forsale_table table.market_commodity_orders_table tr:nth-child(2) td[align="right"]:nth-child(1)').text
            sell = float(sell.replace(",", ".").replace(" pуб.", ""))
            # sell = float(sell.replace("$", ""))
            print(sell, 'sell')
            sell_wik = round(sell / 1.15, 2)
            print(sell_wik, 'sell_wik')
            profit = round(sell_wik - order, 2)
            procent = profit
            print(profit, 'profit')
            if status == 'procent':
                procent = round(profit / (order / 100), 2)
                print(procent, 'procent')
            if procent >= game_prof:
                print(f'сработал профит в {game_prof}')
                parts = item.split('/')
                procent_items = buy_in_hour(cookies, parts[-1], parts[-2], buy_in_Hour)
                if procent_items:
                    browser.find_element(By.CSS_SELECTOR, '#market_commodity_order_spread div:nth-child(2) div div.market_commodity_orders_header a span').click()
                    browser.find_element(By.CSS_SELECTOR, '#market_buy_commodity_input_price').clear()
                    min_a = profit
                    coef_min = min_a // min_prof
                    if coef_min < 1:
                        plus_order = 0.05
                    elif coef_min <= 11:
                        plus_order = 0.1 * coef_min
                    else:
                        plus_order = 0.1 * 11
                    print(f'min_prof {min_a}, coef_min {coef_min} plus_order {plus_order}')
                    browser.find_element(By.CSS_SELECTOR, '#market_buy_commodity_input_price').send_keys(order + round(plus_order, 2))
                    browser.find_element(By.CSS_SELECTOR, '#market_buyorder_dialog_accept_ssa').click()
                    browser.find_element(By.CSS_SELECTOR, '#market_buyorder_dialog_purchase').click()
                    return [order, sell_wik, profit, procent, procent_items]
            break
        except (ValueError, NoSuchElementException):
            print('not_spisoc обновляем')
            time.sleep(5)
            browser.refresh()
        except:
            buffer = io.StringIO()
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(f"Error in not_spisoc: {buffer.getvalue()} , {item.split('/')[-1]} \n")
            traceback.print_exc()


def spisoc(browser, By, cookies, item, buy_in_Hour, game_prof, status, min_prof):
    while True:
        try:
            order = browser.find_element(By.CSS_SELECTOR,
                                         '#market_commodity_buyrequests span.market_commodity_orders_header_promote:nth-child(2)').text
            order = float(order.replace(",", ".").replace(" pуб.", ""))
            print(order, 'order')
            sell_wik = browser.find_elements(By.CSS_SELECTOR, 'span.market_listing_price.market_listing_price_without_fee')
            sell_wik = [browser.execute_script('return arguments[0].textContent;', sell) for sell in sell_wik]
            sell_wik = [float(sell.strip().replace(',', '.').split()[0]) for sell in sell_wik] # 10 цен преобразуем к рабочему виду
            print(sell_wik, 'sell_wik')
            profit = [round(i - order, 2) for i in sell_wik]
            procent = profit      # это profit который отработает если у нас нету status == 'procent'
            print(profit, 'profit')
            if status == 'procent':
                procent = [round(i / (order / 100), 2) for i in profit]
                print(procent, 'procent')
            if all(i >= game_prof for i in procent):
                print(f'сработал профит в {game_prof}')
                parts = item.split('/')
                procent_items = buy_in_hour(cookies, parts[-1], parts[-2], buy_in_Hour)
                if procent_items:
                    browser.find_element(By.CSS_SELECTOR,
                                         'a.btn_green_white_innerfade.btn_medium.market_noncommodity_buyorder_button span').click()
                    browser.find_element(By.CSS_SELECTOR, '#market_buy_commodity_input_price').clear()
                    min_a = min(profit)
                    coef_min = min_a // min_prof
                    if coef_min < 1:
                        plus_order = 0.05
                    elif coef_min <= 11:
                        plus_order = 0.1 * coef_min
                    else:
                        plus_order = 0.1 * 11
                    print(f'min_prof {min_a}, coef_min {coef_min} plus_order {plus_order}')
                    browser.find_element(By.CSS_SELECTOR, '#market_buy_commodity_input_price').send_keys(order + round(plus_order, 2))
                    browser.find_element(By.CSS_SELECTOR, '#market_buyorder_dialog_accept_ssa').click()
                    browser.find_element(By.CSS_SELECTOR, '#market_buyorder_dialog_purchase').click()
                    return [order, sell_wik, profit, procent, procent_items]
            break
        except (ValueError, NoSuchElementException):
            print('spisoc обновляем')
            time.sleep(5)
            browser.refresh()
        except:
            buffer = io.StringIO()
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(f"Error in spisoc: {buffer.getvalue()} , {item.split('/')[-1]} \n")
            traceback.print_exc()



def main(browser, windows, elements, By, cookies, buy_in_Hour, game_prof, status, min_prof):  # the main function of determining the advantageous item
    try:
        browser.execute_script(f"window.open('')")  # open a new window in the browser
        windows['steam_auto'] = browser.window_handles[-1]  # remember a new window
        browser.switch_to.window(windows['steam_auto'])  # switch the workspace

        for item in elements:  # sorting through the elements received earlier
            while True:
                browser.get(item)  # get a page of ellement
                error_def = len(
                    browser.find_elements(By.CSS_SELECTOR, '#searchResultsTable div.market_listing_table_message'))  # checking if there is a defolt bad page error
                if error_def > 0:  # if we have, we do refresh the page
                    continue
                error_time = len(browser.find_elements(By.CSS_SELECTOR, 'div.error_ctn'))  # checking if there is a error of more requests
                if error_time > 0:  # if we have, we do timeout 60s and after refresh the page
                    with open('errors.txt', 'a') as logi:
                        logi.write(f'Error time srabotal \n')
                    time.sleep(60)
                    continue


                #  an item can have 2 different pages (sales and purchase) and therefore the layout on them is different
                #  futher we determine what kind of page the item has
                spisok = len(browser.find_elements(By.CSS_SELECTOR,'span.market_listing_price.market_listing_price_without_fee'))   # drop-down list
                if spisok > 0:  # if we have this version, we work only with him
                    order_have = len(browser.find_elements(By.CSS_SELECTOR, 'div[class="my_listing_section market_content_block market_home_listing_table"] div.market_listing_row.market_recent_listing_row'))
                    if order_have:  # if the order is available now
                        break  # we skip this item
                    details_item = spisoc(browser, By, cookies, item, buy_in_Hour, game_prof, status, min_prof)  # we check if the item is profitable
                    if details_item:  # if yes, we do check further
                        time.sleep(0.5)
                        error_max_orders = browser.find_element(By.CSS_SELECTOR, 'span#market_buyorder_dialog_error_text').text  # checking for a error max orders
                        if len(error_max_orders) > 300:  # if yes, we do cancel more old orders
                            error_max(browser, windows, By)
                            continue  #  and refresh the page
                        with open('logi.txt', 'a') as logi:  # if we have not troubles, we write item at the logi.txt for more analyze if we need
                            logi.write(
                                f"order {details_item[0]} sell_wik {details_item[1]} profit {details_item[2]} procent_prof {details_item[3]} min_pt_prof {min(details_item[3])} procent_items {details_item[4]} max_item {max(details_item[4])} time_buy {datetime.now()} link {item}  \n")
                    break  # moving on to another item

                not_spisok = len(browser.find_elements(By.CSS_SELECTOR, '#market_commodity_forsale_table'))  # regular list
                if not_spisok > 0:  # if we have this version, we work only with him
                    order_have = len(browser.find_elements(By.CSS_SELECTOR, 'div[class="my_listing_section market_content_block market_home_listing_table"] div.market_listing_row.market_recent_listing_row'))
                    if order_have:  # if the order is available now
                        break  # we skip this item
                    details_item = not_spisoc(browser, By, cookies, item, buy_in_Hour, game_prof, status, min_prof)  # we check if the item is profitable
                    if details_item:  # if yes, we do check further
                        time.sleep(0.5)
                        error_max_orders = browser.find_element(By.CSS_SELECTOR, 'span#market_buyorder_dialog_error_text').text  # checking for a error max orders
                        if len(error_max_orders) > 300:  # if yes, we do cancel more old orders
                            error_max(browser, windows, By)
                            continue  #  and refresh the page
                        with open('logi.txt', 'a') as logi:  # if we have not troubles, we write item at the logi.txt for more analyze if we need
                            logi.write(
                                f"order {details_item[0]} sell_wik {details_item[1]} profit {details_item[2]} procent_prof {details_item[3]} procent_items {details_item[4]} max_item {max(details_item[4])} time_buy {datetime.now()} link {item}  \n")
                    break  # moving on to another item
        browser.close()  #  close current window
        del windows['steam_auto']  # del current window
        browser.switch_to.window(windows['tradeback'])  # switch to window with parser items

    except KeyboardInterrupt:
        print('Stopped by the user')
    except:
        buffer = io.StringIO()  # write the error to a file
        traceback.print_exc(file=buffer)
        with open('errors.txt', 'a') as logi:
            logi.write(f'Error in main: {buffer.getvalue()} \n')
        traceback.print_exc()

