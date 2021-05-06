# xattr -d com.apple.quarantine /usr/local/bin/chromedriver

import pandas as pd
from time import sleep
from selenium import webdriver
import os

with open(".env") as f:
    USERNAME, PASSWORD, OS, *_ = [line.strip() for line in f]

# url = "https://myota.tradingacademy.com/MastermindCommunity/MastermindLevelsV2"
url = "https://myota.tradingacademy.com/Login"

driver = webdriver.Chrome(executable_path=f"{OS}/chromedriver")

driver.get(url)

sleep(2)

driver.find_element_by_id("txtUserName").send_keys(USERNAME)
driver.find_element_by_id("txtPassword").send_keys(PASSWORD)
driver.find_element_by_id("SubmitButton").click()

sleep(2)

url = "https://myota.tradingacademy.com/MastermindCommunity/MastermindLevelsV2"

driver.get(url)

sleep(4)

headers = [header.text.strip() for header in driver.find_elements_by_class_name("sd-market")]

print("headers:", headers, len(headers))
print()


raw = []

zoneclassnames = ["sdzone-SZ03", "sdzone-SZ02", "sdzone-SZ01", "sdzone-DZ01", "sdzone-DZ02", "sdzone-DZ03"]

for classname in zoneclassnames:
    row = [z.text for z in driver.find_elements_by_class_name(classname)]
    raw.append(row)

data = []
for row in raw:
    up, down = [], []
    for val in row:
        try:
            a,b = val.split("\n")
            up.append(a)
            down.append(b)

        except:
            up.append("ERROR")
            down.append("ERROR")
    up = up[:len(headers)]
    down = down[:len(headers)]

    data.extend([up,down])
    
data = pd.DataFrame(data)
data.columns = headers

print(data)

date = ""
try:
    date = driver.find_element_by_class_name("sd-date-input")
    date = date.find_element_by_tag_name("input").get_attribute("value")
    print("Date:", date)

except:
    print("Date NOT FOUND")

data.to_csv(f"data {date}.csv", index=False)

print("closing driver")
sleep(2)
driver.close()

