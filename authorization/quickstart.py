from pprint import pprint

from selenium.webdriver import Keys
from selenium.webdriver.chrome import webdriver

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
        print(path_html)
        set_up(path_html)


def get_posts_user(url_user):
    time.sleep(3)
    browser.get(url_user)
    time.sleep(4)

    # links имя div в котором хранятся посты
    links = browser.find_elements(By.CLASS_NAME, 'v1Nh3.kIKUG._bz0w')
    all_posts_user = []
    for el in links:
        post = el.find_element(By.TAG_NAME, 'a').get_attribute('href')
        all_posts_user.append(post)

    time.sleep(2)
    set_up('//*[@id="react-root"]/div/div/section/main/div/header/section/ul/li[2]/a').click()
    time.sleep(2)

    FList = browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
    numberOfFollowersInList = len(FList.find_elements_by_css_selector('li'))

    FList.click()
    actionChain = webdriver.ActionChains(browser)
    time.sleep(3)

    while (numberOfFollowersInList < max):
        actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
        numberOfFollowersInList = len(FList.find_elements_by_css_selector('li'))
        time.sleep(0.4)
        print(numberOfFollowersInList)
        actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
        time.sleep(1)

    return all_posts_user




def log_in():
    """
    Функция авторизации и закрытия первых push-сообщений
    :param:
    :return:    1 if crash
                0 if success connect
    """
    try:
        time.sleep(2)
        # Логин\пароль
        set_up('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(user_name)
        set_up('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(user_pass)

        # Кнопка войти
        time.sleep(1)
        set_up('//*[@id="loginForm"]/div/div[3]').click()




    except:
        print('exceptError')


log_in()
zz = get_posts_user('https://www.instagram.com/astrogks/')
pprint(zz)

time.sleep(500)



