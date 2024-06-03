from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from steam_totp import generate_twofactor_code_for_time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
from start_set import start_steam, start_trade, swipe_game, new_swipe_game
from auto_buy import main

# settings for search range of items
tradeback_set = {}
tradeback_set['Ot_buy'] = '0.5'    # from how many dollars
tradeback_set['Ot_prof'] = '-3'     # from percentage profit
tradeback_set['Do_prof'] = ''    # before percentage profit
tradeback_set['Weak'] = '250'      # from how many sales a week

game_set = {}
game_set['buy_in_Hour'] = 20       # how much is the maximum sales percentage per hour
game_set['Dota_prof'] = 1.7        # profit percentage Dota
game_set['CS_GO_prof'] = 2.5       # profit percentage CS_GO


options = Options()
# options.add_argument('--headless')  # work window is hidden
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(1)  # waiting for an ellement to be searched in 1 second
cookies = start_steam(browser, load_dotenv, By, os, generate_twofactor_code_for_time, "USERNAME_3", "PASSWORD_3", "two_key_3")  # login steam and take cookie


windows = {}  # remember main windows to use

elements = start_trade(browser, By, WebDriverWait, EC, windows, tradeback_set)  # set the search settings on the parser site

# settings for search range of items (from how many dollars, up to how many dollars, from percentage profit, profit percentage Dota, profit percentage CS_GO, status of calculate)
spisoc_range_prof = [['0.4', '0.5', '0', 0.6, 0.9, 'numbers'],
                     ['0.3', '0.4', '0', 0.5, 0.75, 'numbers'],
                     ['0.1', '0.3', '0', 0.4, 0.6, 'numbers'],
                     ['0', '0.1', '4', 0.4, 0.6, 'numbers'],
                     ['0.5', '1000', '-3', 1.7, 2.5, 'procent']]



print(len(elements), 'how many dota 2 items')  # оставить для видоса, потом для гита удалить
game_prof = game_set['Dota_prof']
main(browser, windows, elements, By, cookies, game_set['buy_in_Hour'], game_prof, 'procent', 0.85)  # need dota 0.5 +

elements = swipe_game(browser, By, WebDriverWait, EC)
game_prof = game_set['CS_GO_prof']
main(browser, windows, elements, By, cookies, game_set['buy_in_Hour'], game_prof, 'procent', 1.25)  # need cs  0.5 +
print(len(elements), 'сколько итемов cs 2')


while True:  # The eternal cycle
    for range_prof in spisoc_range_prof:  # scrolling through the search range settings
        elements = new_swipe_game(browser, By, WebDriverWait, EC, range_prof[0], range_prof[1], range_prof[2])  # sets the settings - pick dota and the range of searching for specific things, get the found elements
        print(len(elements), range_prof, 'dota_check')
        main(browser, windows, elements, By, cookies, game_set['buy_in_Hour'], range_prof[3], range_prof[5], 0.85)  # the main function of determining the advantageous item
        elements = swipe_game(browser, By, WebDriverWait, EC)  # sets the settings - pick cs, get the found elements
        print(len(elements), range_prof, 'cs_check')
        main(browser, windows, elements, By, cookies, game_set['buy_in_Hour'], range_prof[4], range_prof[5], 1.25)  # the main function of determining the advantageous item







