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

options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=./User_Data')

driver = webdriver.Chrome(
    "D:/Projects/WhatsApp auto attach/chromedriver.exe", options=options)
driver.get('https://web.whatsapp.com/')
input('Press enter after scanning QR code.')

failFileName = 'Fails - ' + str(date.today().strftime("%b-%d-%Y")) + '.csv'
#filepath = "D:/Libraries/Downloads/newyear_poster.jfif"
msg = "Insert message to send here."
sentCount = count = 0

with open('latest_list.csv') as csv_file:
    phones_csv = csv.reader(csv_file, delimiter=',')
    print("Sending messages...")
    country_code = "974"

    for row in phones_csv:
        count += 1

        name = (row[0].strip()).title()
        number = row[1].strip()

        driver.get('https://web.whatsapp.com/send?phone=' +
                   country_code + number)
        input("Press enter after chat loads.")

        try:
            # If the number is on WhatsApp
            print("Attempting send: #" + str(count))

            # Sending text
            msg_box = driver.find_element_by_xpath(
                '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')

            for part in ("*Dear " + name + "*,\n\n" + msg).split('\n'):
                msg_box.send_keys(part)
                ActionChains(driver).key_down(Keys.SHIFT).key_down(
                    Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()

            send_button = driver.find_element_by_xpath(
                '//span[@data-icon="send"]')
            send_button.click()

            # Sending poster image
            # attachment_box = driver.find_element_by_xpath(
            #   '//div[@title = "Attach"]')
            # attachment_box.click()

            # image_box = driver.find_element_by_xpath(
            #    '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
            # image_box.send_keys(filepath)

            # sleep(3)

            # send_button = driver.find_element_by_xpath(
            #    '//span[@data-icon="send"]')
            # send_button.click()

            sleep(3)

            sentCount += 1

        except NoSuchElementException:
            try:
                ok_button = driver.find_element_by_class_name('_30EVj')
                ok_button.click()
            except:
                pass

            print("#" + str(count) + " failed.")

            # Writing failed contact info to fails csv file
            with open(failFileName, mode='a', newline='') as fails_file:
                fails_writer = csv.writer(fails_file, delimiter=',')
                fails_writer.writerow([name, number])

            continue

        except UnexpectedAlertPresentException:
            print("#" + str(count) + " failed.")

            # Writing failed contact info to fails csv file
            with open(failFileName, mode='a', newline='') as fails_file:
                fails_writer = csv.writer(fails_file, delimiter=',')
                fails_writer.writerow([name, number])

            sleep(5)
            continue

    print("Message successfully sent to " + str(sentCount) + " numbers.")
