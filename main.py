import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# the webdriver is returning error that the chromedriver version is not compatible with the current browser version
# Thus I am autoUpdating the chromedriver if it needs update each time I run the code, else I will skip
# and continue the code
chromedriver_autoinstaller.install()  # check if the chromedriver needs any update and update it directly.


def getCredentials():
    credentials = []
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    credentials.append(username)
    credentials.append(password)
    return credentials


userCredentials = getCredentials()
driver = webdriver.Chrome()  # Generate the Browser
driver.get("https://banweb.lau.edu.lb/")  # Go to the lau banner

driver.find_element(by="id", value="username").send_keys(userCredentials[0])  # Find the username and password filed
driver.find_element(by="id", value="password").send_keys(userCredentials[1])  # and Then insert the credentials automatically
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
