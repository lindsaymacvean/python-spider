#! bin/python

import csv
import getpass
import pickle
import time
import os.path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.binary_location = '/usr/bin/google-chrome'
driver = webdriver.Chrome('/usr/bin/chromedriver',
    chrome_options=options)

inputFile = open("list.csv", 'r+')
outputFile = open("output.csv", 'wb')
inputReader = csv.reader(inputFile)
inputWriter = csv.writer(inputFile)
outputWriter = csv.writer(outputFile)
next(inputReader, None)
if not os.path.isfile('Cookies.pkl'):
    username = raw_input("What is your linkedin username: ")
    password = getpass.getpass("What is your linkedin password: ")
    driver.get("https://www.linkedin.com/uas/login")
    usernameField = driver.find_element_by_id("session_key-login")
    passwordField = driver.find_element_by_id("session_password-login")
    usernameField.send_keys(username)
    passwordField.send_keys(password)
    driver.find_element_by_id("btn-primary").click()
    time.sleep(5)
    elem = driver.find_element_by_xpath('//*[@data-control-name="identity_welcome_message"]')
    print(elem.text)
    pickle.dump(driver.get_cookies() , open("Cookies.pkl","wb"))

for row in inputReader:
    if row[5] != '':
        outputWriter.writerow(row)
        continue
    print row[1]
    driver.get(row[7])
    for cookie in pickle.load(open("Cookies.pkl", "rb")):
        driver.add_cookie(cookie)
    time.sleep(5)
    driver.find_element_by_id('org-about-company-module__show-details-btn').click()
    time.sleep(5)
    elem = None
    try:
        if elem is None:
            elem = driver.find_element_by_xpath('//*/p[contains(@class, "org-about-company-module__specialities")]')
    except NoSuchElementException:
        print("Cannot find the Specialties")
        row[5] = ''
        outputWriter.writerow(row)
        continue
    print(elem.text)
    row[5] = elem.text
    inputWriter.writerow(row)
    outputWriter.writerow(row)



driver.close()
