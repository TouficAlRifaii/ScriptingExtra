import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
import csv
import time
from pwinput import pwinput

# the webdriver is returning error that the chromedriver version is not compatible with the current browser version
# Thus I am autoUpdating the chromedriver if it needs update each time I run the code, else I will skip
# and continue the code
chromedriver_autoinstaller.install()  # check if the chromedriver needs any update and update it directly.


def getCredentials():
    credentials = []
    username = input("Enter your username: ")
    password = pwinput("Enter your password: ", "*")
    credentials.append(username)
    credentials.append(password)
    return credentials


def getOffering(credentials):
    driver = webdriver.Chrome()  # Generate the Browser
    driver.get("https://banweb.lau.edu.lb/")  # Go to the lau banner

    driver.find_element(by="id", value="username").send_keys(credentials[0])  # Find the username and password filed
    driver.find_element(by="id", value="password").send_keys(
        credentials[1])  # and Then insert the credentials automatically
    driver.find_element(by=By.CSS_SELECTOR, value='[type="submit"]').click()  # then click the login button

    driver.get("https://banweb.lau.edu.lb/prod/bwskfcls.p_sel_crse_search")
    term = Select(driver.find_element(by="id", value="term_input_id"))
    term.select_by_visible_text("Fall 2023 (View only)")
    driver.find_element(by=By.CSS_SELECTOR, value='[value="Submit"]').click()
    driver.find_element(by=By.CSS_SELECTOR, value='[value="Advanced Search"]').click()
    major = Select(driver.find_element(by="id", value="subj_id"))
    major.select_by_visible_text("Computer Science")
    campus = Select(driver.find_element(by="id", value="camp_id"))
    campus.select_by_visible_text("Byblos")
    driver.find_element(by=By.CSS_SELECTOR, value='[value="Section Search"]').click()
    time.sleep(15)
    offering = bs(driver.page_source, "html.parser").prettify()
    return offering


def getRows(html_offering):
    soup = bs(html_offering, "html.parser")
    table = soup.find("table", {"class": "datadisplaytable"})
    # print(table)
    table_rows = list()
    for row in table.findAll("tr"):
        table_rows.append(row)
    return table_rows


def parseToCSV(table_rows):
    with open("output.csv", "w") as file:
        writer = csv.writer(file)
        headers = table_rows[1]
        headerCells = list()
        for cell in headers.findAll(["td", "th"]):
            if headers.findAll(["td", "th"]).index(cell) != 0 and headers.findAll(["td", "th"]).index(cell) < 20:
                if cell.string:
                    headerCells.append(cell.string.strip())
                else:
                    children = cell.findAll()
                    for i in children:
                        headerCells.append(i.string.strip())

        writer.writerow(headerCells)
        for i in range(2, len(table_rows)):
            cells = list()
            row = table_rows[i]
            for cell in row.findAll(["td", "th"]):
                if row.findAll(["td", "th"]).index(cell) != 0 and row.findAll(["td", "th"]).index(
                        cell) < 20:
                    if cell.string:
                        cells.append(cell.string.strip())
                    else:
                        children = cell.findAll()
                        for i in children:
                            cells.append(i.string.strip())
            if len(cells) > 4:
                if eval(cells[4]) == 2:
                    writer.writerow(cells)
            # else:
            #     writer.writerow(cells)


userCredentials = getCredentials()
course_offering = getOffering(userCredentials)
rows = getRows(course_offering)
parseToCSV(rows)
