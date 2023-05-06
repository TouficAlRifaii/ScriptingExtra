from selenium import webdriver
from selenium.webdriver.common.by import By


def getCredentials():
    credentials = []
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    credentials.append(username)
    credentials.append(password)
    return credentials


userCredentials = getCredentials()
driver = webdriver.Chrome("chromedriver")  # Generate the Browser
driver.get("https://banweb.lau.edu.lb/")  # Go to the lau banner

driver.find_element(by="id", value="username").send_keys(userCredentials[0])  # Find the username and password filed
driver.find_element(by="id", value="password").send_keys(userCredentials[1])  # and Then insert the credentials automatically
driver.find_element(by=By.CSS_SELECTOR, value='[type="submit"]').click()  # then click the login button
