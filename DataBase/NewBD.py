import MySQLdb
from global_set.settings import login_db, pass_db

connect = MySQLdb.connect('localhost', login_db, pass_db, 'inst')
cursor = connect.cursor()


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
               'profile_check int,'
               'subscribe_ok int,'
               'PRIMARY KEY (ID) );')
        cursor.execute(sql)
        connect.commit()

    except:
        pass


def create_table_wait_unsubscribe():
    sql = ("create table wait_to_unsubscribe("
           "id int auto_increment,"
           "name_user varchar(255),"
           "date_sub date,"
           "date_unsub date,"
           "primary key(id))")
    cursor.execute(sql)
    connect.commit()



