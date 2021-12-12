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


def set_up(path_html):
    button_or_form = browser.find_element(By.XPATH, path_html)
    return button_or_form


def log_in():
    """
    Функция авторизации и закрытия первых push-сообщений
    :param:
    :return:    1 if crash
                0 if success connect
    """
    try:
        # Логин\пароль
        set_up('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(user_name)
        set_up('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(user_pass)
        # Кнопка войти
        time.sleep(1)
        set_up('//*[@id="loginForm"]/div/div[3]').click()
        # Первое уведомление
        time.sleep(4)
        set_up('//*[@id="react-root"]/div/div/section/main/div/div/div/section/div/button').click()
    except:
        log_in()



time.sleep(500)