from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

s = Service(ChromeDriverManager().install())


def get_browser():
    """
    Получение браузера в объект browser, страница https://www.instagram.com/
    :return: browser
    """
    browser = webdriver.Chrome(service=s)
    browser.maximize_window()
    browser.get('https://www.instagram.com/')

    return browser
