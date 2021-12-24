from ast import literal_eval
from pprint import pprint
import MySQLdb
from global_set.settings import login_db, pass_db

connect = MySQLdb.connect('localhost', login_db, pass_db, 'inst')
cursor = connect.cursor()


def add_new_profile(data):
    try:
        sql = ("INSERT INTO user_profiles (user_name,"
               " user_link, user_sub, user_followers,"
               " user_posts, number_sub, number_followers, number_posts, profile_check)"
               " VALUES (%(user_name)s, %(user_link)s, %(user_sub)s, %(user_followers)s, %(user_posts)s,"
               " %(number_sub)s, %(number_followers)s, %(number_posts)s), %(chek_profile)s")
        cursor.execute(sql, data)
        connect.commit()
    except:
        pass

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
               follower_min=0, follower_max=10_000):

    """
    sub_min=7500, sub_max=7590,
               follower_min=4360, follower_max=4375):
    Фильтрация таблицы user_profile
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
                   f"and profile_check = 1"

                   )
    response_db = cursor.fetchall()
    result = []

    # Создаем список [id пользователя,[Ссылки таблицы]]
    for tuple_link in response_db:
        id_user = tuple_link[0]
        list_link = literal_eval(tuple_link[1])
        result.append([id_user, list_link])

    return result


def check_ok(id_user):
    """
    Функция меняет значение profile_check на 0, то есть что профиль обработан
    :param id_users:
    :return:
    """
    sql = (f"UPDATE user_profiles SET profile_check = 0 WHERE id = {id_user};")
    cursor.execute(sql)
    connect.commit()
    print('+++++++++++++++++++')
    print('commit')
    print('+++++++++++++++++++')