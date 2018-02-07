#! bin/python

import csv
import getpass
import pickle
import time
import os.path
import urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print "downloading input csv with urllib2"
f = urllib2.urlopen('https://docs.google.com/spreadsheets/d/e/2PACX-1vRwSXoVVf6h-LeadAx_gUDCSuUCw_YJSHhdko9jq9qQqis2CW8JXaeIh6aUJzhjgK7rmONbVU_BMSmJ/pub?gid=28561824&single=true&output=csv')
data = f.read()
with open("list.csv", "w+") as code:
    code.write(data)
code.close()

def wait_for_correct_current_url(desired_url):
	wait.until(lambda driver: desired_url in driver.current_url)

options = webdriver.ChromeOptions()
options.binary_location = '/usr/bin/google-chrome'
driver = webdriver.Chrome('/usr/bin/chromedriver',
    chrome_options=options)

inputFile = open("list.csv", 'r+')
outputFile = open("output.csv", 'wb')
inputReader = csv.reader(inputFile)
inputWriter = csv.writer(inputFile)
outputWriter = csv.writer(outputFile)
if not os.path.isfile('Cookies.pkl'):
    #username = raw_input("What is your username: ")
    username = 'lindsay.macvean@invotra.com'
    #password = getpass.getpass("What is your linkedin password: ")
    password = '1PatOL8iFu24'
    driver.get("https://www.gartner.com/login/loginInitAction.do?method=initialize&login=mkhdr")
    usernameField = driver.find_element_by_id("username")
    passwordField = driver.find_element_by_id("password")
    usernameField.send_keys(username)
    passwordField.send_keys(password)
    driver.find_element_by_xpath('//*[@id="gLogin"]/input[10]').click()
    time.sleep(5)
    pickle.dump(driver.get_cookies() , open("Cookies.pkl","wb"))

print "Set the Cookies"
driver.get('https://gartner.com')
for cookie in pickle.load(open("Cookies.pkl", "rb")):
	driver.add_cookie(cookie)
driver.get('https://gartner.com')

print "Get the Research URL"
for row in inputReader:
	if row[10] != '':
		outputWriter.writerow(row)
		continue
	driver.get(row[11])
	elem = None
	try:
		if elem is None:
			elem = driver.find_element_by_class_name('linktoSearchQid')
	except NoSuchElementException:
		print("Cannot find the url")
		outputWriter.writerow(row)
		continue
	row[10] = elem.get_attribute('href')
	inputWriter.writerow(row)
	outputWriter.writerow(row)

inputFile.seek(0)
outputFile.seek(0)
print "Get the Document URL"
for row in inputReader:
	if row[9] != '':
		outputWriter.writerow(row)
		continue
	url = None
	try:
		driver.get(row[10])
		if url is None:
			wait = WebDriverWait(driver, 100)
			desired_url = 'document'
			wait_for_correct_current_url(desired_url)
			url = driver.current_url.split("?")[0]
			print url
	except Exception as e:
		print("Cannot find the url")
		outputWriter.writerow(row)
		continue
	row[9] = url
	inputWriter.writerow(row)
	outputWriter.writerow(row)

driver.close()
exit(1)


# Get the Document Title
for row in inputReader:
    if row[8] != '':
        outputWriter.writerow(row)
        continue
    driver.get(row[9])
    elem = None
    try:
        if elem is None:
            elem = driver.find_element_by_class_name('linktoSearchQid')
    except NoSuchElementException:
        print("Cannot find the url")
        outputWriter.writerow(row)
        continue
    row[3] = elem.get_attribute('href')
    inputWriter.writerow(row)
    outputWriter.writerow(row)

driver.close()