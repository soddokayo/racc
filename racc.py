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
fout = open('out.txt', 'w', encoding='utf8')

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
        if cnt>10:
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
            text0 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="form"]/span[@class="input"]/input'))
            )
        finally:
            msg0 = 'ㄴㅈ'
            text0.send_keys(msg0)
            text0.send_keys(Keys.RETURN)
            #driver.find_element((By.XPATH, '//div[@class="form"]/span[@class="submit"]/button'))
        # wait for chatting

        driver.implicitly_wait(10)

        # wait for stranger's escape
        try:
            start1 = WebDriverWait(driver, 60).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, 'v_close'))
            )
        finally:
            try:
                msg1 = driver.find_element((By.XPATH, '//div[@class="v_area v_area_scroll"]/div[@class="v_area_in"]'))
                fout.write(msg1.get_attribute('innerHTML'))
            except Exception as e:
                print(e)
            # log the last msg
            # try:
            #     msg1 = WebDriverWait(driver, 5).until(
            #         EC.presence_of_element_located((By.CLASS_NAME, 'msg msg_stranger'))
            #     )
            # finally:
            #     fout.write(msg1.get_attribute('innerHTML'))

fout.close()

driver.close()
driver.quit()
