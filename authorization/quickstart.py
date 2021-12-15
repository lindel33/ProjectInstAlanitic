from global_set import settings
from selenium.webdriver.common.by import By
from global_set.global_set import get_browser
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
            self.set_up('//*[@id="loginForm"]/div/div[3]').click()
            return 0
        except None:
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
        self.set_up('//*[@id="react-root"]/div/div/section/main/div/header/section/ul/li[2]/a').click()
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
    @staticmethod
    def get_posts_user(url_user):
        """
        Функция возвращает список ссылок на посты пользователя
        :param url_user:
        """
        time.sleep(3)
        browser.get(url_user)
        time.sleep(4)

        # links имя div в котором хранятся посты
        links = browser.find_elements(By.CLASS_NAME, 'v1Nh3.kIKUG._bz0w')
        all_posts_user = []
        for el in links:
            post = el.find_element(By.TAG_NAME, 'a').get_attribute('href')
            all_posts_user.append(post)

        return all_posts_user

    @staticmethod
    def get_subscript_links():
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


login = LoginUser()
login.log_in()
post_user = UserInfo()
z = post_user.get_posts_user('https://www.instagram.com/astrogks/')
print(z)
scroll = Scrolling()
scroll.wait_scroll(settings.number_scroll_subscripts)
x = post_user.get_subscript_links()
print(x)

time.sleep(500)
