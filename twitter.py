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
for row in inputReader:
    if row[3] != '':
        outputWriter.writerow(row)
        continue
    print row[7]
    driver.get(row[7])
    elem = None
    try:
        if elem is None:
            elem = driver.find_element_by_xpath('//*[contains(@class, "detailstable")]//a[contains(@href,"twitter")]')
    except NoSuchElementException:
        print("Cannot find the url")
        outputWriter.writerow(row)
        continue
    row[3] = elem.get_attribute('href')
    inputWriter.writerow(row)
    outputWriter.writerow(row)



driver.close()
