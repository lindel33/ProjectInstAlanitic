import datetime
from ast import literal_eval
import MySQLdb
from global_set.settings import login_db, pass_db

connect = MySQLdb.connect('localhost', login_db, pass_db, 'inst')
cursor = connect.cursor()


def add_new_profile(data):
    print('data')
    sql = ("INSERT INTO user_profiles (user_name,"
           " user_link, user_sub, user_followers,"
           " user_posts, number_sub, number_followers, number_posts, profile_check, subscribe_ok)"
           " VALUES (%(user_name)s, %(user_link)s, %(user_sub)s, %(user_followers)s, %(user_posts)s,"
           " %(number_sub)s, %(number_followers)s, %(number_posts)s, 1, 1)")
    cursor.execute(sql, data)
    connect.commit()
    print('save')


def get_all_info():
    """
    Вернет все данные из таблицы user_profiles
    :return:
    """
    cursor.execute(f"SELECT *"
                   "FROM user_profiles "

                   )
    my_result = cursor.fetchall()

    return my_result


def get_profile_value(value_1, value_2):
    """
    Принимает value_1 - максимальное кол-во подписчиков
    Принимает value_2 - максимальное кол-во подписок
    :param value_1:
    :param value_2:
    :return: result - tuple профиль из БД
    """

    cursor.execute(f"SELECT *"
                   "FROM user_profiles "
                   f"WHERE number_followers < {value_1} "
                   f"and number_sub < {value_2}"
                   )
    result = cursor.fetchall()

    return result


def get_column(name_column='user_followers',
               sub_min=0, sub_max=10_000,
               follower_min=0, follower_max=10_000,
               subscript_ok=1, profile_check=1):

    """
    sub_min=7500, sub_max=7590,
               follower_min=4360, follower_max=4375):
    Фильтрация таблицы user_profile
    :param profile_check: 1
    :param subscript_ok: 1
    :param name_column: user_followers
    :param sub_min: 0
    :param sub_max: 10_000
    :param follower_min: 0
    :param follower_max: 10_000
    :return: Столбец таблицы выбранный по условиям
    """

    cursor.execute(f"SELECT id,{name_column} "
                   f"FROM user_profiles "
                   f"WHERE number_sub > {sub_min} "
                   f"and number_sub < {sub_max} "
                   f"and number_followers > {follower_min} "
                   f"and number_followers < {follower_max} "
                   f"and profile_check = {profile_check} "
                   f"and subscribe_ok={subscript_ok}"

                   )
    response_db = cursor.fetchall()
    result = []

    if name_column == 'user_followers':
        # Создаем список [id пользователя,[Ссылки таблицы]]
        for tuple_link in response_db:
            id_user = tuple_link[0]
            list_link = literal_eval(tuple_link[1])
            result.append([id_user, list_link])
        return result
    elif name_column == 'user_link':
        for link in response_db:
            result.append(list(link))
        return result
    else:
        return response_db


def check_ok(id_user):
    """
    Функция меняет значение profile_check на 0, то есть что профиль обработан
    :param id_user:
    :return:
    """
    sql = f"UPDATE user_profiles SET profile_check = 0 WHERE id = {id_user};"
    cursor.execute(sql)
    connect.commit()


def subscribe_ok(id_user):
    sql = f"UPDATE user_profiles SET subscribe_ok = 0 WHERE id = {id_user};"
    cursor.execute(sql)
    connect.commit()


def to_wait(data):
    """
    Запись в таблицу ожидания к отписке
    :return:
    """
    sql = ("INSERT INTO wait_to_unsubscribe (name_user, date_sub, date_unsub)"
           " VALUES (%(name_user)s, %(date_sub)s, %(date_unsub)s)")
    cursor.execute(sql, data)
    connect.commit()


def get_to_unsubscribe():
    today = str(datetime.date.today())
    print(today)
    sql = f"select id, name_user from wait_to_unsubscribe where date_unsub < '{today}'"
    cursor.execute(sql)
    response_db = cursor.fetchall()
    return response_db


def delete_subscript(id_user):
    sql = f"DELETE FROM wait_to_unsubscribe WHERE id = {id_user}"
    cursor.execute(sql)
    connect.commit()



