import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from my_login import user_pass, user_name

s = Service(ChromeDriverManager().install())

browser = webdriver.Chrome(service=s)
browser.maximize_window()

browser.get('https://www.instagram.com/')
time.sleep(5)

button_login = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
button_login.send_keys(user_name)

button = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
button.send_keys(user_pass)



time.sleep(500)