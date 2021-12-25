import datetime
from ast import literal_eval

from DataBase.data import add_new_profile, get_column, check_ok, subscribe_ok, to_wait, get_to_unsubscribe, \
    delete_subscript
from global_set import settings
from selenium.webdriver.common.by import By
from global_set.global_set import get_browser
import time

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

        count_error = 0

        time.sleep(2)
        try:

            self.get_xpath_object(form_login).send_keys(settings.user_name)
            self.get_xpath_object(form_pass).send_keys(settings.user_pass)
            self.get_xpath_object(button_login).click()
            time.sleep(4)
            return 0

        except NameError:
            count_error += 1

            self.get_xpath_object(form_login).clear()
            self.get_xpath_object(form_pass).clear()

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
        block_to_scroll_followers = '/html/body/div[6]/div/div/div[2]'
        block_to_scroll_sub = '/html/body/div[6]/div/div/div[3]'
        script = "arguments[0].scrollTop = arguments[0].scrollHeight"
        end_scroll = True
        try:
            time.sleep(2)
            try:
                scr1 = self.get_xpath_object(block_to_scroll_followers)
            except:
                scr1 = self.get_xpath_object(block_to_scroll_sub)
            browser.execute_script(script, scr1)
            return 0

        except None:
            if not end_scroll:
                return 1
            else:
                time.sleep(5)
                self.scroll()
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

                exit_count = self.scroll()
                count += int(exit_count)
                if time_wait == 10:
                    time.sleep(3)
                if count == 3 or number_scroll_local == number_to_scroll:
                    break
                time_wait += 1
        except:
            return 0


class UserInfo(ObjectMixin):

    def get_info_user(self, url_user):
        """
        Функция возвращает список данных на посты пользователя
        :param url_user:
        :return data_return = [posts_user, name_user, num_followers[0], number_sub, number_posts]
                            [Список постов, ник, кол-во подписчиков, кол-во подписок, кол-во постов]
        """

        browser.get(url_user)
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
            number_subscript = ''
            if ' ' in number_sub:
                number = number_sub.split()
                number_subscript = number[0] + number[1]
            else:
                number_subscript = number_sub

            # Получение списка постов(ссылки)
            links = browser.find_elements(By.CLASS_NAME, 'v1Nh3.kIKUG._bz0w')
            posts_user = []
            for el in links:
                post = el.find_element(By.TAG_NAME, 'a').get_attribute('href')
                posts_user.append(post)

            data_return = {'posts_user': str(posts_user),
                           'name_user': str(name_user),
                           'num_followers': str(num_followers[0]),
                           'number_subscript': str(number_subscript),
                           'number_posts': str(number_posts),
                           'url_user': str(url_user)}
            return data_return
        except:
            return 404

    def get_followers_links(self):
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

    def get_subscript_links(self):
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

    @staticmethod
    def get_dict_profile(url_user):
        post_user = UserInfo()
        scroll = Scrolling()
        xpath_follower_window = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'
        xpath_subscript_window = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'
        try:

            profile_info = post_user.get_info_user(url_user)

            scroll.wait_scroll(settings.number_scroll_followers, xpath_follower_window)
            all_followers_user = post_user.get_followers_links()

            scroll.wait_scroll(settings.number_scroll_subscripts, xpath_subscript_window)
            all_subscripts_user = post_user.get_subscript_links()

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
        except AttributeError:
            return 404


class NewSubscript(ObjectMixin):
    """
    Класс подписки на пользователей из БД
    """
    def get_links_to_subscript(self):
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

                to_wait(data)
                print('120 сек. ожидание после подписки')

                tim = 0
                for i in range(0, 120):
                    time.sleep(1)
                    tim += 1
                    if tim % 10 == 0:
                        print('Прошло', tim, ' из 120')
            except:
                pass

    def __subscript_button(self):

        try:
            button_subscript = '//*[@id="react-root"]/section/main' \
                               '/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button'
            self.get_xpath_object(button_subscript).click()

        except ValueError:
            pass

    def delete_sub(self):
        response_db = get_to_unsubscribe()
        time.sleep(2)
        print('wait')
        for link in response_db:

            link = list(link)
            print(link)
            try:
                browser.get(link[1])
                time.sleep(2)
                browser.find_element(By.CLASS_NAME, '_5f5mN.-fzfL._6VtSN.yZn4P').click()

                time.sleep(1)
                browser.find_element(By.CLASS_NAME, 'aOOlW.-Cab_').click()
                time.sleep(2)
                delete_subscript(link[0])
                print('120 сек. ожидание после отписки')

                tim = 0
                for i in range(0,120):
                    time.sleep(1)
                    tim += 1
                    if tim % 10 == 0:
                        print('Прошло', tim, ' из 120')
                init.new_subs()
            except:
                print(link[0], 'не удалось')

class CheckUser(ObjectMixin):
    """
    Класс проверяет профили пользователей на ботов и магазины
    """

    @staticmethod
    def get_info_profile():
        data = 1
        return data


class InitProgram:
    list_check_profile = []
    list_links = get_column()

    def __init__(self):
        self.login = LoginUser()
        self.login.log_in()
        self.info = UserInfo()
        self.sub = NewSubscript()

    def check_profiles(self):
        for link in self.list_links:
            for profile in link[1]:
                try:
                    result = UserInfo.get_dict_profile(profile)
                except:
                    result = 404

                if result == 404:
                    pass
                else:
                    add_new_profile(result)
            self.list_check_profile.append(link[0])
            check_ok(link[0])

    def new_subs(self):
        self.sub.get_links_to_subscript()


init = InitProgram()
init.sub.delete_sub()
time.sleep(500)
