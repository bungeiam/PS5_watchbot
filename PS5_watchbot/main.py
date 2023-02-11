# main #
import os
import random
import time
import datetime

# whatsapp notification
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# scanning
import requests
from bs4 import BeautifulSoup
from urls import dna, elisa, gigantti, telia, vk, prisma

r = requests


def screen_clear():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')


def Check_DNA(url):
    print("DNA:")
    response = r.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find("h1", {"data-testid": "product-page-name"})
    stock = soup.find("p", {"data-testid": "webshop-availability-text"})
    return title.text, stock.text


def Check_prisma(url):
    print("PRISMA:")
    response = r.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find("h1", class_='productTitle')
    stock = soup.find("button", class_='add-to-cart')
    return title.text.strip(), stock.text.strip()


def Check_VK(url):
    print("VERKKOKAUPPA.COM:")
    response = r.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find("h1", class_='hiTsuG')
    stock = soup.find("div", class_='shipment-details__ready-for-shipment')
    return title.text, stock.text


def Check_Elisa(url):
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_argument("--window-size=1400x1000")
    options.add_experimental_option("excludeSwitches", ['enable-logging'])
    options.add_experimental_option("detach", True)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/84.0.4147.125 Safari/537.36")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    cookies = wait.until(EC.element_to_be_clickable((
        By.XPATH, '/html/body/div[4]/div/div[1]/div[2]/button')))
    cookies.click()
    _html = driver.page_source
    soup = BeautifulSoup(_html, features="html.parser")
    title = soup.find("h1", class_='ea-h2 t-product-name')
    stock = soup.find_all("div", class_='description ea-bodytext')
    driver.quit()
    print("ELISA:")
    return title.text, stock[1].text


def notification(p, url):
    # Absolute path to chromedriver
    options = Options()
    options.add_argument("user-data-dir=C:\\Users\\joona\\AppData\\Local\\Google\\Chrome\\Selenium data")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 600)

    # Message
    string = str(p) + " löytynyt osoitteesta:  " + str(url)

    time.sleep(3)
    name = "//*[@id='pane-side']/div[1]/div/div/div[11]/div/div/div[2]/div[1]/div[1]/span/span"
    name_clickable = wait.until(EC.presence_of_element_located((
        By.XPATH, name)))
    name_clickable.click()
    inp_xpath = '//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]'
    input_box = wait.until(EC.presence_of_element_located((
        By.XPATH, inp_xpath)))
    for i in range(1):
        input_box.send_keys(string + Keys.ENTER)
        time.sleep(1)
        driver.quit()


scanning = True
dna_scan = 1
elisa_scan = 1
vk_scan = 1
prisma_scan = 1

if __name__ == '__main__':
    while scanning:
        screen_clear()
        print("Scan paused for 5 seconds...")
        time.sleep(5)
        screen_clear()
        print("Starting a new scan..")
        # DNA
        for url in dna.values():
            if dna_scan == 1:
                result = Check_DNA(url)
                print(result, "\n")
                if "loppu" in result[1]:
                    pass
                else:
                    dna_scan = 0
                    notification(result[0], url)  # CALL WHATSAPP NOTIFICATION

        # # ELISA
        # for url in elisa.values():
        #     if elisa_scan == 1:
        #         try:
        #             result = Check_Elisa(url)
        #             print(result, "\n")
        #             if "Ei" in result[1]:
        #                 pass
        #             else:
        #                 elisa_scan = 0
        #                 notification(result[0], url)     # CALL WHATSAPP NOTIFICATION
        #         except:
        #             pass

        # VERKKOKAUPPA
        for url in vk.values():
            if vk_scan == 1:
                result = Check_VK(url)
                print(result, "\n")
                if "Lähetettävissä" in result[1]:
                    notification(result[0], url)  # CALL WHATSAPP NOTIFICATION
                    vk_scan = 0
                else:
                    pass

        # PRISMA
        for url in prisma.values():
            if prisma_scan == 1:
                result = Check_prisma(url)
                print(result, "\n")
                if "Ei" in result[1]:
                    pass
                else:
                    prisma_scan = 0
                    notification(result[0], url)  # CALL WHATSAPP NOTIFICATION
        time.sleep(10)
