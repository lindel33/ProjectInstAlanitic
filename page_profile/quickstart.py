import datetime
import time

from selenium.common.exceptions import NoSuchElementException, InvalidElementStateException
from selenium.webdriver.common.by import By

from DataBase.data import (add_new_profile, get_column,
                           check_ok, subscribe_ok,
                           wait_list_unsub, get_to_unsubscribe,
                           delete_subscript)
from global_set import settings
from global_set.global_set import get_browser
from delay_time import daley_press

browser = get_browser()


class ObjectMixin:
    @staticmethod
    def get_xpath_object(path_html):
        """
        Принимает путь XPath элемента HTML
        Возвращает объект(ссылку)
        :param path_html:
        """
        button_or_form = browser.find_element(By.XPATH, path_html)

        if button_or_form:
            return button_or_form

        else:
            return 'Ошибка Xpath'


class LoginUser(ObjectMixin):
    def log_in(self):
        """
        Функция авторизации
        :param:
        :return:    1 if crash
                    0 if success connect
        """
        form_login = '//*[@id="loginForm"]/div/div[1]/div/label/input'
        form_pass = '//*[@id="loginForm"]/div/div[2]/div/label/input'
        button_login = '//*[@id="loginForm"]/div/div[3]'

        next_page_url = 'https://www.instagram.com/accounts/onetap/?next=%2F'

        count_auth = 1
        time.sleep(2)

        while browser.current_url != next_page_url:
            print('Попытка авторизации: ', count_auth)
            count_auth += 1
            try:
                time.sleep(settings.wait_open_new_page)

                self.get_xpath_object(form_login).clear()
                self.get_xpath_object(form_pass).clear()

                time.sleep(2)

                self.get_xpath_object(form_login).send_keys(settings.user_name)
                self.get_xpath_object(form_pass).send_keys(settings.user_pass)
                self.get_xpath_object(button_login).click()

                time.sleep(settings.wait_open_new_page)

            except NoSuchElementException:
                pass

        print('Авторизация прошла успешно!')
        return 0


class Scrolling(ObjectMixin):
    def __scroll(self):
        """
        Функция пролистывания списка подписчиков
        :return:
        """

        block_to_scroll = browser.find_element(By.CLASS_NAME, 'isgrP')
        script = "arguments[0].scrollTop = arguments[0].scrollHeight"

        end_scroll = True
        try:
            time.sleep(2)

            browser.execute_script(script, block_to_scroll)
            return 0

        except NoSuchElementException:
            if not end_scroll:
                return 1
            else:
                time.sleep(5)
                self.__scroll()
            return 0.5

    def wait_scroll(self, number_to_scroll, button):
        """
        Нажимаем на кнопку подписчиков и листаем на установленное количесво раз
        :return:
        """
        try:
            time.sleep(2)
            self.get_xpath_object(button).click()
            time.sleep(2)

            number_scroll_local = 0
            count = 0
            time_wait = 0
            end = True
            while end:
                number_scroll_local += 1
                count += int(self.__scroll())

                if time_wait == 10:
                    time.sleep(3)

                if count == 3 or number_scroll_local == number_to_scroll:
                    break

                time_wait += 1
        except:
            return 0


class UserInfo(ObjectMixin):
    def __init__(self, url_user):
        self.url_user = url_user

    def get_info_user(self):
        """
        Функция возвращает информацию со страницы профиля
        :return data_return = [posts_user, name_user, num_followers[0], number_sub, number_posts]
                            [Список постов, ник, кол-во подписчиков, кол-во подписок, кол-во постов]
        """

        browser.get(self.url_user)
        time.sleep(4)
        try:
            block_name = '//*[@id="react-root"]/section/main/div/header/section/div[1]/h2'
            block_followers = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span'

            name_user = self.get_xpath_object(block_name).text
            no_filter_followers = self.get_xpath_object(block_followers).text

            # Проверка на наличя слова тыс в кол-во подписчиков
            num_followers = []
            if 'т' in no_filter_followers:
                num_followers.append(no_filter_followers[0:3] + '000')

            elif ' ' in no_filter_followers:
                x = no_filter_followers.split()
                res = x[0] + x[1]
                num_followers.append(res)

            else:
                num_followers.append(no_filter_followers)

            try:
                number_sub = self.get_xpath_object('//*[@id="react-root"]/section/main/'
                                                   'div/header/section/ul/li[3]/span/span').text
            except:
                number_sub = self.get_xpath_object('//*[@id="react-root"]/section/main/'
                                                   'div/header/section/ul/li[3]/a/span').text
            try:
                number_posts = self.get_xpath_object('//*[@id="react-root"]/section/main/'
                                                     'div/header/section/ul/li[1]/span/span').text
            except:
                number_posts = self.get_xpath_object('//*[@id="react-root"]/section/main/'
                                                     'div/header/section/ul/li[2]/a/span').text

            # Фильтрация кол-во подписок
            if ' ' in number_sub:
                number = number_sub.split()
                number_subscript = number[0] + number[1]
            else:
                number_subscript = number_sub

            posts_user = self.__get_user_posts()
            data_return = {'posts_user': str(posts_user),
                           'name_user': str(name_user),
                           'num_followers': str(num_followers[0]),
                           'number_subscript': str(number_subscript),
                           'number_posts': str(number_posts),
                           'url_user': str(self.url_user)}

            return data_return
        except:
            return 404

    @staticmethod
    def __get_user_posts():
        # Получение списка постов(ссылки)
        links = browser.find_elements(By.CLASS_NAME, 'v1Nh3.kIKUG._bz0w')
        posts_user = []
        for el in links:
            post = el.find_element(By.TAG_NAME, 'a').get_attribute('href')
            posts_user.append(post)
        return posts_user

    def __get_followers_links(self):
        """
        Получение списка ссылок на подписчиков пользователя
        :return: all_followers
        """

        # Находим поле с подписчиками
        followers = browser.find_elements(By.CSS_SELECTOR, 'body>div.RnEpo.Yx5HN>div>div>div.isgrP>ul>div>li')

        all_followers = []
        for follower in followers:
            post = follower.find_element(By.TAG_NAME, 'a').get_attribute('href')
            all_followers.append(post)
        self.get_xpath_object('/html/body/div[6]/div/div/div[1]/div/div[2]/button').click()
        return str(all_followers)

    def __get_subscript_links(self):
        """
        Получение списка ссылок на подписки пользователя
        :return: all_sub
        """
        try:
            number_sub = self.get_xpath_object('//*[@id="react-root"]/section/main/div/header/'
                                               'section/ul/li[3]/span/span').text

        except:
            number_sub = self.get_xpath_object('//*[@id="react-root"]/section/main/div/header/'
                                               'section/ul/li[3]/a/span').text

        if number_sub != '0':
            # Находим поле с подписками
            subscript = browser.find_elements(By.CSS_SELECTOR, 'body>div.RnEpo.Yx5HN>div>div>div.isgrP>ul>div')

            all_subscript = []
            for sub in subscript:
                post = sub.find_element(By.TAG_NAME, 'a').get_attribute('href')
                all_subscript.append(post)

            self.get_xpath_object('/html/body/div[6]/div/div/div[1]/div/div[2]/button').click()

            return str(all_subscript)
        else:
            pass

    def get_dict_profile(self):
        scroll = Scrolling()
        xpath_follower_window = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'
        xpath_subscript_window = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'

        try:
            profile_info = self.get_info_user()

            scroll.wait_scroll(settings.number_scroll_followers, xpath_follower_window)
            all_followers_user = self.__get_followers_links()

            scroll.wait_scroll(settings.number_scroll_subscripts, xpath_subscript_window)
            all_subscripts_user = self.__get_subscript_links()

            # Чистка 1 000 от пробела (подписчики)
            if profile_info == 404:
                return 404
            clear_number = profile_info['number_posts']
            if ' ' in clear_number:
                clear_number = profile_info['number_posts'].split()
                clear_number = int(clear_number[0] + clear_number[1])

            data = {'user_name': profile_info['name_user'],
                    'user_link': profile_info['url_user'],
                    'user_sub': all_subscripts_user,
                    'user_followers': all_followers_user,
                    'user_posts': profile_info['posts_user'],
                    'number_sub': profile_info['number_subscript'],
                    'number_followers': profile_info['num_followers'],
                    'number_posts': clear_number,
                    }

            return data
        except InvalidElementStateException:
            return 404


class NewSubscript(ObjectMixin):
    """
    Удаление/Подписка на пользователей
    """

    def new_subscript(self):
        """
        Подписка на пользователей
        :return:
        """
        data = get_column(name_column='user_link', sub_max=1_000, follower_max=1_000)
        for user_link in data:
            print(user_link)

            try:
                browser.get(user_link[1])
                self.__subscript_button()
                subscribe_ok(user_link[0])
                today = datetime.date.today()
                tomorrow = today + datetime.timedelta(days=1)
                data = {'name_user': user_link[1],
                        'date_sub': datetime.date.today(),
                        'date_unsub': tomorrow}

                wait_list_unsub(data)
                daley_press('ожидание после подписки')
            except:
                pass

    def __subscript_button(self):
        try:
            button_subscript = '//*[@id="react-root"]/section/main' \
                               '/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button'
            self.get_xpath_object(button_subscript).click()
        except NoSuchElementException:
            pass

    @staticmethod
    def delete_sub():
        response_db = get_to_unsubscribe()
        time.sleep(2)

        # link = ['id', 'url-профиля']
        for link in response_db:
            link = list(link)
            print(link)
            try:
                browser.get(link[1])
                time.sleep(settings.wait_open_new_page)

                button_unsubscribe = '_5f5mN.-fzfL._6VtSN.yZn4P'
                browser.find_element(By.CLASS_NAME, button_unsubscribe).click()
                time.sleep(1)

                button_unsubscribe_ok = 'aOOlW.-Cab_'
                browser.find_element(By.CLASS_NAME, button_unsubscribe_ok).click()

                delete_subscript(link[0])
                wait_list_unsub('Ожидание после отписки')

            except:
                print(link[0], 'не удалось')


class InitProgram:
    list_check_profile = []
    list_links = get_column()

    def __init__(self):
        self.login = LoginUser()
        self.login.log_in()
        self.sub = NewSubscript()

    def check_profiles(self):
        for link in self.list_links:
            for profile in link[1]:
                try:
                    profile_user = UserInfo(profile)
                    profile_user = profile_user.get_dict_profile()
                except:
                    profile_user = 404

                if profile_user == 404:
                    pass
                else:
                    add_new_profile(profile_user)
            self.list_check_profile.append(link[0])
            check_ok(link[0])

    def new_subs(self):
        self.sub.new_subscript()


init = InitProgram()
init.sub.new_subscript()
time.sleep(500)
