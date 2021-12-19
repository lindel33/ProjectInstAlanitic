from pprint import pprint

import MySQLdb
from serializers.serializer_db import serializer_data

conn = MySQLdb.connect('localhost', 'root', 'I1QEvAR503', 'inst')
cursor = conn.cursor()


def add_new_profile():
    # data = serializer_data()

    # my = ["dsadas", 'adsads', 'dsadas', 'sadsaddasdas', 'dsadasdas', 2222, 22, 22]
    my = {'user_name': "aaaaaa",
          'user_link': 'aaaaaa',
         'user_sub': 'aaaa',
         'user_followers': 'sadsaddasdas',
         'user_posts': 'dsadasdas',
         'number_sub': 54444,
         'number_followers': 333,
         'number_posts': 132213}
    sql = ("INSERT INTO user_prsssofiles (user_name,"
           " user_link, user_sub, user_followers,"
           " user_posts, number_sub, number_followers, number_posts)"
           " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(sql, my)
    conn.commit()
# add_new_profile()


def create_table_profile():
    try:
        sql = ('CREATE TABLE user_profiles('
               'id int NOT NULL AUTO_INCREMENT,'
               'user_name varchar(255),'
               'user_link varchar(255),'
               'user_sub LONGTEXT,'
               'user_followers LONGTEXT,'
               'user_posts LONGTEXT,'
               'number_sub int,'
               'number_followers int,'
               'number_posts int,'
               'PRIMARY KEY (ID) );')
        cursor.execute(sql)
        conn.commit()

    except:
        pass
# dsasdadsdasdssaddsdadsddasd
add_new_profile()


