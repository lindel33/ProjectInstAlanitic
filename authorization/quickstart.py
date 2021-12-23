import datetime
from DataBase.data import add_new_profile
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
        try:
            post_user = UserInfo()
            profile_info = post_user.get_info_user(url_user)

            scroll = Scrolling()
            scroll.wait_scroll(settings.number_scroll_subscripts, '//*[@id="react-root"]'
                                                                  '/section/main/div/header/section/ul/li[2]/a')
            all_followers_user = post_user.get_followers_links()

            scroll.wait_scroll(settings.number_scroll_subscripts, '//*[@id="react-root"]'
                                                                  '/section/main/div/header/section/ul/li[3]/a')
            all_subscripts_user = post_user.get_subscript_links()

            # Чистка 1 000 от пробела (подписчики)
            clear_number = profile_info['number_posts']
            if ' ' in clear_number:
                clear_number = profile_info['number_posts'].split()
                clear_number = int(clear_number[0] + clear_number[1])
            date = str(datetime.date.today())

            data = {'user_name': profile_info['name_user'],
                    'user_link': profile_info['url_user'],
                    'user_sub': all_subscripts_user,
                    'user_followers': all_followers_user,
                    'user_posts': profile_info['posts_user'],
                    'number_sub': profile_info['number_subscript'],
                    'number_followers': profile_info['num_followers'],
                    'number_posts': clear_number,
                    'date_save': date,
                    'chek_profile': 1,
                    }

            return data
        except:
            return 404


x = [
     'https://www.instagram.com/musliman_05_05/',
     'https://www.instagram.com/simonashopska/',
     'https://www.instagram.com/kx_boburbek/',
     'https://www.instagram.com/javoxir_9070/',
     'https://www.instagram.com/moaeyed.mohammed/',
     'https://www.instagram.com/asilkingo7/',
     'https://www.instagram.com/_vlad_nedviga_/']

login = LoginUser()
login.log_in()

info = UserInfo()
for i in x:
    result = UserInfo.get_dict_profile(i)
    if result == 404:
        pass
    else:
        add_new_profile(result)
# sub = NewSubscribe()
# sub.new_subscribe(x)
time.sleep(500)


class CheckUser(ObjectMixin):
    """
    Класс проверяет профили пользователей на ботов и магазины
    """

    @staticmethod
    def get_info_profile():
        data = 1
        return data
