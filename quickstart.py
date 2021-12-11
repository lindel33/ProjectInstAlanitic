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
input_login = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
input_pass = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
input_login.send_keys(user_name)
input_pass.send_keys(user_pass)
button_login = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')
button_login.click()
time.sleep(5)
button_login = browser.find_element(By.XPATH, '//*[@id="react-root"]/'
                                              'div/div/section/main/div'
                                              '/div/div/section/div/button')
button_login.click()
time.sleep(3)
button_login = browser.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[3]/button[1]')
button_login.click()
time.sleep(3)
list_sub = browser.find_element(By.XPATH, '//*[@id="react-root"]/div/div/section/main/section/div/div/div')
time.sleep(3)

try:
    Follow_Button = browser.find_element("//*[text()='Подписаться']")
    Follow_Button.click()
except:
    pass

time.sleep(5000)
