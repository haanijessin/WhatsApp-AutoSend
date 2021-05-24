from selenium import webdriver
from time import sleep
from pathlib import Path
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import csv
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from datetime import date

options = webdriver.ChromeOptions();
options.add_argument('--user-data-dir=./User_Data')

driver = webdriver.Chrome("D:/Projects/WhatsApp auto attach/chromedriver.exe",options=options)
driver.get('https://web.whatsapp.com/')
input('Press enter after scanning QR code.')
count = 0

with open('not_messaged_init.csv') as csv_file:
    phones_csv = csv.reader(csv_file, delimiter=',')
    print("Checking sent messages...")

    for row in phones_csv:
        count+=1
        
        name = row[0].strip()
        number = row[1].strip()

        search_box = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]')

        search_box.send_keys(Keys.CONTROL, 'a')
        search_box.send_keys(Keys.BACKSPACE)
        
        search_box.send_keys(number)

        sleep(10)

        html_source = driver.page_source
        
        if 'No chats, contacts or messages found' in html_source:
            print('#' + str(count)+  ': ' + str(number) + ' not messaged.')
            with open('not_messaged.csv', mode='a', newline='') as not_messaged_file:
                not_messaged_writer = csv.writer(not_messaged_file, delimiter=',')
                not_messaged_writer.writerow([name,number])
        else:
            print('#' + str(count)+ ': ' + str(number) + ' found in sent messages.')
            continue
