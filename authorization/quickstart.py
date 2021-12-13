from global_set.settings import user_pass, user_name
from selenium.webdriver.common.by import By
from global_set.global_set import get_browser
import time


browser = get_browser()


def set_up(path_html):
    """
    Принимает путь XPath элемента HTML
    Возвращает объект(ссылку)
    :param path_html:
    :return:
    """
    button_or_form = browser.find_element(By.XPATH, path_html)

    if button_or_form:
        return button_or_form

    else:
        set_up(path_html)


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


log_in()
time.sleep(500)
