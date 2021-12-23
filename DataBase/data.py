import MySQLdb
from global_set.settings import login_db, pass_db

connect = MySQLdb.connect('localhost', login_db, pass_db, 'inst')
cursor = connect.cursor()


def add_new_profile(data):
    print(data)
    sql = ("INSERT INTO user_profiles (user_name,"
           " user_link, user_sub, user_followers,"
           " user_posts, number_sub, number_followers, number_posts)"
           " VALUES (%(user_name)s, %(user_link)s, %(user_sub)s, %(user_followers)s, %(user_posts)s,"
           " %(number_sub)s, %(number_followers)s, %(number_posts)s)")
    cursor.execute(sql, data)
    connect.commit()


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
        connect.commit()

    except:
        pass
create_table_profile()