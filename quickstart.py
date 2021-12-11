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


