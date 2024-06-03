import time
import traceback
import io


def start_steam(browser, load_dotenv, By, os, generate_twofactor_code_for_time, USERNAME, PASSWORD, TWO_KEY):  # login steam and take cookie
    try:
        browser.get('https://steamcommunity.com/login/home/?goto=')  # login page
        load_dotenv()  # Loads environment variables from the .env file into the system
        browser.find_element(By.CSS_SELECTOR, 'input[type="text"]._2eKVn6g5Yysx9JmutQe7WV').send_keys(os.getenv(USERNAME))  # enter USERNAME
        browser.find_element(By.CSS_SELECTOR, 'input[type="password"]._2eKVn6g5Yysx9JmutQe7WV').send_keys(os.getenv(PASSWORD))  # enter PASSWORD
        browser.find_element(By.CSS_SELECTOR, 'button._2QgFEj17t677s3x299PNJQ').click()  # click to login button
        while True:
            steam_Code = generate_twofactor_code_for_time(shared_secret=os.getenv(TWO_KEY))  # get twofactor code
            browser.find_element(By.CSS_SELECTOR, 'input[tabindex="0"]:nth-child(1)').send_keys(steam_Code)  # enter twofactor code
            error_key = len(browser.find_elements(By.CSS_SELECTOR, 'div._1Mcy9wnDnt1Q72FijsNtHC'))  #  if we get error with bad twofactor code
            if error_key > 0:
                time.sleep(0.5)
                continue
            time.sleep(2)
            cookies = browser.get_cookies()  # get all the cookies
            return cookies[2]['value']  # take only steamLoginSecure
    except:
        buffer = io.StringIO()  # write the error to a file
        traceback.print_exc(file=buffer)
        with open('errors.txt', 'a') as logi:
            logi.write(f"Error in start_steam: {buffer.getvalue()} \n")
        traceback.print_exc()


def start_trade(browser, By, WebDriverWait, EC, windows, tradeback_set):  # set the search settings on the parser site
    try:
        time.sleep(1)
        browser.get( # get a parset page
            'https://tradeback.io/ru/comparison#{%22app%22:%22all%22,%22services%22:[%22steamcommunity.com%22,%22bitskins.com%22],%22updated%22:[],%22categories%22:[[%22normal%22],[%22normal%22]],%22hold_time_range%22:[8,8],%22price%22:[[],[]],%22count%22:[[],[]],%22profit%22:[[],[]]}')
        browser.find_element(By.CSS_SELECTOR, 'input.btn_green_white_innerfade').click()
        time.sleep(7)
        browser.find_element(By.CSS_SELECTOR, 'label[for="first-service-orders"]').click()
        browser.find_element(By.CSS_SELECTOR, 'div.dropdown-select:nth-child(3) div.title').click()
        browser.find_element(By.CSS_SELECTOR, 'div.menu.indent li[value="3"]').click()
        browser.find_element(By.CSS_SELECTOR,'div.dropdown-select:nth-child(4) div.title:nth-child(1)').click()  # off stickers
        browser.find_element(By.CSS_SELECTOR, 'label[for="filter-without-stickers"]').click()  # off stickers
        browser.find_element(By.CSS_SELECTOR, 'div.comparison-service:nth-child(2) div.title').click()
        browser.find_element(By.CSS_SELECTOR,'div.comparison-service:nth-child(2) div.menu.show li[value="steamcommunity.com"]').click()
        browser.find_element(By.CSS_SELECTOR,'div.range-filters.price-filters[data-column="first"] input[placeholder="От"]').send_keys(tradeback_set['Ot_buy'] )  # from how many dollars
        # browser.find_element(By.CSS_SELECTOR,'div.range-filters.price-filters[data-column="first"] input[placeholder="До"]').send_keys('0.5')
        browser.find_element(By.CSS_SELECTOR, '#more-filters.comparison-filters-btn').click()
        browser.find_element(By.CSS_SELECTOR, 'input.comparison-sales-input.sales-filter[data-key="s"]').clear()
        browser.find_element(By.CSS_SELECTOR, 'input.comparison-sales-input.sales-filter[data-key="s"]').send_keys(tradeback_set['Weak'])                      # from how many sales a week
        time.sleep(0.5)
        browser.find_element(By.CSS_SELECTOR, 'div[id="filters-modal"] a.iziModal-button.iziModal-button-close').click()
        time.sleep(0.5)
        browser.find_element(By.CSS_SELECTOR, 'div.dropdown-select:nth-child(6) div.title').click()
        browser.find_element(By.CSS_SELECTOR, 'label[for="auto-update-live"]').click()
        browser.find_element(By.CSS_SELECTOR,'th.center:nth-child(12) div.range-filters.profit-filters input[placeholder="От"]').send_keys(tradeback_set['Ot_prof']) # from percentage profit
        browser.find_element(By.CSS_SELECTOR,'th.center:nth-child(12) div.range-filters.profit-filters input[placeholder="До"]').send_keys(tradeback_set['Do_prof']) # before percentage profit
        browser.find_element(By.CSS_SELECTOR, 'div.column-profit.sort[data-column="first"]').click()
        time.sleep(4)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # swipe down to the bottom of the page to get all the elements.
        time.sleep(1)
        windows['tradeback'] = browser.current_window_handle  # remember the current window
        elements = WebDriverWait(browser, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td.field-link[data-link-key="steamcommunity"] a'))) # get a ellement
        elements = [ell.get_attribute("href") for ell in elements]  # get a need link
        return elements
    except:
        buffer = io.StringIO()  # write the error to a file
        traceback.print_exc(file=buffer)
        with open('errors.txt', 'a') as logi:
            logi.write(f"Error in start_trade: {buffer.getvalue()} \n")
        traceback.print_exc()


def swipe_game(browser, By, WebDriverWait, EC):  # sets the settings - pick cs, get the found elements
    while True:
        try:
            try:
                browser.find_element(By.CSS_SELECTOR, 'div.dropdown-select:nth-child(3) div.title').click()  # clicl to playlist
                browser.find_element(By.CSS_SELECTOR, f'div.menu.indent li[value="2"]').click()  # clicl a CS game
                browser.refresh()  # refresh page
                time.sleep(4)
                for i in range(15):
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll down 15 times
                time.sleep(1)
            except:  # If something goes wrong, we try again.
                browser.refresh()
                time.sleep(4)
                print("swipe_game browser.refresh() Error")
                continue
            try:
                elements = WebDriverWait(browser, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td.field-link[data-link-key="steamcommunity"] a')))  # get a ellement
            except:
                return []
            elements = [ell.get_attribute("href") for ell in elements]  # get a need link
            return elements
        except:
            buffer = io.StringIO()  # write the error to a file
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(f"Error in swipe_game: {buffer.getvalue()} \n")
            traceback.print_exc()
            print('error in swipe_game check monitor')


def new_swipe_game(browser, By, WebDriverWait, EC, range_1, range_2, prof_1):  # sets the settings - pick dota and the range of searching for specific things, get the found elements
    while True:
        try:
            try:
                browser.find_element(By.CSS_SELECTOR, 'div.dropdown-select:nth-child(3) div.title').click()  # clicl to playlist
                browser.find_element(By.CSS_SELECTOR, f'div.menu.indent li[value="3"]').click()  # clicl a Dota game
                browser.find_element(By.CSS_SELECTOR, 'div.range-filters.price-filters[data-column="first"] input[placeholder="От"]').clear()
                browser.find_element(By.CSS_SELECTOR, 'div.range-filters.price-filters[data-column="first"] input[placeholder="От"]').send_keys(range_1)  # from how many dollars
                browser.find_element(By.CSS_SELECTOR, 'div.range-filters.price-filters[data-column="first"] input[placeholder="До"]').clear()
                browser.find_element(By.CSS_SELECTOR, 'div.range-filters.price-filters[data-column="first"] input[placeholder="До"]').send_keys(range_2)  # before how many dollars
                browser.find_element(By.CSS_SELECTOR, 'th.center:nth-child(12) div.range-filters.profit-filters input[placeholder="От"]').clear()
                browser.find_element(By.CSS_SELECTOR, 'th.center:nth-child(12) div.range-filters.profit-filters input[placeholder="От"]').send_keys(prof_1)  # from percentage profit
                time.sleep(2)
                browser.refresh()  # refresh page
                time.sleep(4)
                for i in range(15):
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # scroll down 15 times
                time.sleep(1)
            except:  # If something goes wrong, we try again.
                traceback.print_exc()
                browser.refresh()
                time.sleep(4)
                print("new_swipe_game browser.refresh() Error")
                continue
            try:
                elements = WebDriverWait(browser, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td.field-link[data-link-key="steamcommunity"] a')))  # get a ellement
            except:
                return []
            elements = [ell.get_attribute("href") for ell in elements]  # get a need link
            return elements
        except:
            buffer = io.StringIO()  # write the error to a file
            traceback.print_exc(file=buffer)
            with open('errors.txt', 'a') as logi:
                logi.write(f"Error in new_swipe_game: {buffer.getvalue()} \n")
            traceback.print_exc()
            print('error in new_swipe_game check monitor')

