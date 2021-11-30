#racc.py

import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

# log
import time
FNAME = time.strftime("RACCLOG %Y-%m-%d-%H.%M.%S.txt")
fout = open(FNAME, 'w', encoding='utf8')
fout.close()

# tor setting
PROXY = "socks5://localhost:9050"

options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get("http://check.torproject.org")

# gagalive url setting
URL = 'http://www.gagalive.com/live/random_chat'

driver.get(url=URL)

# wait for loading randomchat
try:
    frame1 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//iframe[@src="/randomchat/"]'))
    )
finally:
    driver.switch_to.frame(frame1)

    # eternal crawling (cnt<50)
    cnt=0
    while True:
        if cnt>50:
            break

        # enter a ranchat room
        try:
            start1 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'start'))
            )
        finally:
            ActionChains(driver).move_to_element(start1).click(start1).perform()
            cnt+=1

        # simple chat bot
        text0=0
        try:
            # wait until loading
            text0 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="form"]/span[@class="input"]/input'))
            )
        finally:
            # initial msg
            msg0 = 'ㄴㅈ'
            text0.send_keys(msg0)
            text0.send_keys(Keys.RETURN)
        
        # recog spam detectection
        msg1 = driver.find_element(by=By.XPATH, value="//div[not(@id='room0')][@class='room']/table/tbody/tr/td/div/div")
        if 'SPAM' in msg1.get_attribute('innerHTML') or '스팸' in msg1.get_attribute('innerHTML'):
            print('spam detected')
            # NEED: VPN renew process
            # continue
            break

        # NEED: chatbot

        try:
            # wait for the stranger escapes
            close1 = WebDriverWait(driver, 70).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, 'v_close'))
            )
        except:
            # exit after 70 sec
            close1 = driver.find_element(by=By.CLASS_NAME, value='v_close')
            ActionChains(driver).move_to_element(close1).click(close1).perform()
        finally:
            try:
                # log
                fout = open(FNAME, 'a', encoding='utf8')
                msg1 = driver.find_element(by=By.XPATH, value="//div[not(@id='room0')][@class='room']/table/tbody/tr/td/div/div")
                fout.write('[' + str(cnt) + ']\n' + msg1.get_attribute('innerHTML') + '\n\n')
                fout.close()
            except Exception as e:
                print(e)

driver.close()
driver.quit()
