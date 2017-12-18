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
    if row[2] != '':
        outputWriter.writerow(row)
        continue
    if "twitter" in row[2]:
        row[2] = ''
        inputWriter.writerow(row)
        outputWriter.writerrow(row)
        continue
    driver.get(row[1])
    elem = None
    try:
        if elem is None:
            elem = driver.find_element_by_xpath('//*[@id="node-86421"]/div/div[1]/div/div/div/table/tbody/tr[3]/td[2]/a')
        if elem is None:
            elem = driver.find_element_by_xpath('//*[@id="node-86421"]/div/div[1]/div/div/div/table/tbody/tr[2]/td[2]/a')
        if elem is None:
            elem = driver.find_element_by_xpath('//*[@id="node-86421"]/div/div[1]/div/div/div/table/tbody/tr[3]/td[2]/a')
        if elem is None:
            input("there is no elements")
    except NoSuchElementException:
        print("Cannot find the url")
        outputWriter.writerow(row)
        continue
    if "twitter" in row[2]:
        print("A twitter link was found instead of url")
        outputWriter.writerow(row)
        continue
    row[2] = elem.get_attribute('href')
    inputWriter.writerow(row)
    outputWriter.writerow(row)

print("\nnow we can check for linkedin URLs")
inputFile.seek(0)
outputFile.seek(0)
for row in inputReader:
    if row[3] != '':
        outputWriter.writerow(row)
        continue
    driver.get(row[2])
    try:
        elem = driver.find_element_by_xpath("//a[contains(@href,'linkedin')]")
    except NoSuchElementException:
        print("No Linkedin URL found for "+row[3])
        row[3] = "NA"
        outputWriter.writerow(row)
        continue
    url = elem.get_attribute('href')
    row[3] = url
    inputWriter.writerow(row)
    outputWriter.writerow(row)

print("\nnow we can check for employee count")
inputFile.seek(0)
outputFile.seek(0)
for row in inputReader:
    if 4 not in row:
        row.append('0')
    if row[3] == 'NA':
        print("No Linkedin page for "+row[0])
        outputWriter.writerow(row)
        continue
    if row[4] != '0':
        print(row[0]+" already has "+row[4])
        outputWriter.writerow(row)
        continue
    print(row[3])
    driver.get(row[3])
    for cookie in pickle.load(open("Cookies.pkl", "rb")):
        driver.add_cookie(cookie)
    try: 
        elem = driver.find_element_by_xpath("//*[contains(text(), 'See all ') and contains(text(), 'employees on LinkedIn')]")
    except NoSuchElementException:
        print("No employee count found")
        row[4] = "NA"
        outputWriter.writerow(row)
        continue
    string = elem.text.replace(',', '')
    numbers = [int(s) for s in string.split() if s.isdigit()]
    employeeCount = numbers[0]
    row[4] = employeeCount
    inputWriter.writerow(row)
    outputWriter.writerow(row)



#assert "Python" in driver.title
#elem = driver.find_element_by_name("q")
#elem.clear()
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
driver.close()
