import datetime
from pprint import pprint

from DataBase.data import add_new_profile
from global_set import settings
from selenium.webdriver.common.by import By
from global_set.global_set import get_browser
from serializers.serializer_db import serializer_data
import time

browser = get_browser()


class ObjectMixin:
    def set_up(self, path_html):
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
            self.set_up(path_html)


class LoginUser(ObjectMixin):
    def log_in(self):
        """
        Функция авторизации
        :param:
        :return:    1 if crash
                    0 if success connect
        """

        count_error = 0

        try:
            time.sleep(2)
            # Логин\пароль
            self.set_up('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(settings.user_name)
            self.set_up('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(settings.user_pass)

            # Кнопка войти
            time.sleep(1)
            xz = self.set_up('//*[@id="loginForm"]/div/div[3]').click()

            return 0
        except:
            count_error += 1

            # Чистка полей ввода
            self.set_up('//*[@id="loginForm"]/div/div[1]/div/label/input').clear()
            self.set_up('//*[@id="loginForm"]/div/div[2]/div/label/input').clear()
            self.log_in()

            if count_error == 5:
                print('5 ошибок аторизации')
                return 1


class Scrolling(ObjectMixin):

    def scroll(self):
        """
        Функция пролистывания списка подписчиков
        :return:
        """
        end_scroll = True
        try:
            time.sleep(2)
            scr1 = browser.find_element(By.XPATH, '/html/body/div[6]/div/div/div[2]')
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)
            return 0

        except None:
            if not end_scroll:
                return 1
            else:
                time.sleep(5)
                self.scroll()
            return 0.5

    def wait_scroll(self, number_to_scroll):
        """
        Нажимаем на кнопку подписчиков и листаем на установленное количесво раз
        :return:
        """
        time.sleep(2)
        self.set_up('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        time.sleep(2)

        number_scroll_local = 0
        count = 0
        time_wait = 0
        end = True
        while end:
            number_scroll_local += 1

            exit_count = self.scroll()
            count += int(exit_count)
            if time_wait == 10:
                time.sleep(3)
            if count == 3 or number_scroll_local == number_to_scroll:
                break
            time_wait += 1


class UserInfo(ObjectMixin):

    def get_posts_user(self, url_user):
        """
        Функция возвращает список данных на посты пользователя
        :param url_user:
        :return data_return = [posts_user, name_user, num_followers[0], num_sub, num_posts]
                                Список постов, ник, кол-во подписчиков, кол-во подписок, кол-во постов
        """
        time.sleep(5)
        browser.get(url_user)
        time.sleep(4)

        # links имя div в котором хранятся посты
        name_user = self.set_up('//*[@id="react-root"]/section/main/div/header/section/div[1]/h2').text
        no_filter = self.set_up('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text
        num_followers = []

        if 'т' in no_filter:
            num_followers.append(no_filter[0:3] + '000')
        print(no_filter)
        print(num_followers)

        num_sub = self.set_up(' //*[@id="react-root"]/section/main/div/header/section/ul/li[3]/span/span').text
        num_posts = self.set_up('//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span').text

        links = browser.find_elements(By.CLASS_NAME, 'v1Nh3.kIKUG._bz0w')
        posts_user = []
        for el in links:
            post = el.find_element(By.TAG_NAME, 'a').get_attribute('href')
            posts_user.append(post)

        data_return = [posts_user, name_user, num_followers[0], num_sub, num_posts, url_user]
        """
        //*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span - кол-во пдписчиков
        //*[@id="react-root"]/section/main/div/header/section/ul/li[3]/span/span - ко-во подписок
        //*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span - кол-во постов"""
        return data_return

    @staticmethod
    def get_followers_links():
        """
        Получение списка ссылок на подписчиков пользователя
        :return: all_sub
        """
        # Находим поле с подписчиками
        subscript = browser.find_elements(By.CSS_SELECTOR, 'body>div.RnEpo.Yx5HN>div>div>div.isgrP>ul>div>li')

        all_subscript = []
        for sub in subscript:
            post = sub.find_element(By.TAG_NAME, 'a').get_attribute('href')
            all_subscript.append(post)
        return all_subscript

    @staticmethod
    def get_dict_profile():
        post_user = UserInfo()
        profile_info = post_user.get_posts_user('https://www.instagram.com/astrogks/')

        # pprint(all_post_user)

        scroll = Scrolling()
        scroll.wait_scroll(settings.number_scroll_subscripts)
        # [posts_user, name_user, num_followers[0], num_sub, num_posts]

        today = str(datetime.date.today())
        all_subscript_user = post_user.get_followers_links()
        data = {'user_name': profile_info[1],
                'user_link': profile_info[5],
                'user_sub': all_subscript_user,
                'user_followers': profile_info[3],
                'user_posts': profile_info[0],
                'number_sub': 'Подписки',
                'number_followers': profile_info[2],
                'number_posts': profile_info[4],
                'date_save': today,

                }
        return data


class NewSubscribe(ObjectMixin):
    def new_subscribe(self, my_list):
        count = 0
        for link in my_list:
            browser.get(link)
            close_or_open = self.check_close_account()

            time.sleep(3)
            browser.find_element(By.CLASS_NAME, 'sqdOP.L3NKy.y3zKF').click()
            count += 1
            if count == settings.time_wait_press_subscribe:
                break

    @staticmethod
    def check_close_account():
        """
        Проверка открыт ли аккаунт
        :return:
        """
        try:
            browser.find_element(By.XPATH, '//*[@id="react-root"]/div/div/section/main/div/div/article/div[1]/div/h2')
            return False
        except:
            return True


login = LoginUser()
login.log_in()


info = UserInfo()
result = UserInfo.get_dict_profile()
pprint(result)
# add_new_profile(result)
# sub = NewSubscribe()
# sub.new_subscribe(x)
time.sleep(500)
