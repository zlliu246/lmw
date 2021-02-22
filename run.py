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

sleep(2)

thead = driver.find_element_by_class_name("sd-head")

header = []

for tr in thead.find_elements_by_tag_name("tr"):

    header.append([])

    for th in tr.find_elements_by_tag_name("th"):

        header[-1].append(th.text)

tbody = driver.find_element_by_class_name("sd-body")

body = []

for tr in tbody.find_elements_by_tag_name("tr"):

    body.append([])

    for th in tr.find_elements_by_tag_name("th"):
        body[-1].append(th.text)

    if len(body[-1]) > 0:
        body.append([])

    for td in tr.find_elements_by_tag_name("td"):
        body[-1].append(td.text)

new = []

for row in body:

    try:
        a, b = [],[]
        for item in row:
            aa,bb = item.split("\n")
            a.append(aa)
            b.append(bb)
        
        new.append(a)
        new.append(b)

    except:
        new.append(row)

# for row in new:
#     print(row)

DELIMITER = "\t"

with open("data.tsv", "w") as f:
    for segment in [header, new]:
        for row in segment:
            print("len of row",len(row))
            string = DELIMITER.join(row).replace("-","0")
            f.write(string + "\n")

print("written to tsv")

driver.close()

