import MySQLdb
from serializers.serializer_db import serializer_data
conn = MySQLdb.connect('localhost', 'root', 'I1QEvAR503', 'inst')
cursor = conn.cursor()

cursor.execute("SELECT * FROM userprofile")

# Получаем данные.
row = cursor.fetchone()
print(row)


datas=  {"id": "1", "user_name": "astrogks", "user_link": "https://www.instagram.com/astrogks/",
        "user_sub": ["https://www.instagram.com/lenkafomina486/", "https://www.instagram.com/sashaaleksandrova723/", "https://www.instagram.com/evgeniiatitova872/", "https://www.instagram.com/haqnazarovsiyovush/", "https://www.instagram.com/elenabogdanova5301/", "https://www.instagram.com/katiakomarova684/", "https://www.instagram.com/svetagolubeva4046/", "https://www.instagram.com/iuliakrylova759/", "https://www.instagram.com/vdskin193/", "https://www.instagram.com/spasov_evgenii/", "https://www.instagram.com/iuliagerasimova105/", "https://www.instagram.com/elenatimofeeva2836/", "https://www.instagram.com/valeriiastepanova7924/", "https://www.instagram.com/sashasmirnova831/", "https://www.instagram.com/evgeniiaalekseeva2140/", "https://www.instagram.com/keit6711/", "https://www.instagram.com/svetastepanova121/", "https://www.instagram.com/arkam6724/", "https://www.instagram.com/aniastepanova6444/", "https://www.instagram.com/belozertsevartur/", "https://www.instagram.com/nikityk_y/", "https://www.instagram.com/cuba_ruk/", "https://www.instagram.com/natashasaveleva1024/", "https://www.instagram.com/evgeniiaivanova7154/", "https://www.instagram.com/deborahlewiswtagfxndka/", "https://www.instagram.com/lesiamikhailova120/", "https://www.instagram.com/viskas.vis/", "https://www.instagram.com/lesiamartynova72/", "https://www.instagram.com/plotnikova_mariia/", "https://www.instagram.com/zheniaegorova4185/", "https://www.instagram.com/valentinagrigoreva4290/", "https://www.instagram.com/lesiaborisova493/", "https://www.instagram.com/ekaterinadanilova4021/", "https://www.instagram.com/9352_nika/", "https://www.instagram.com/sashamelnikova659/", "https://www.instagram.com/galiarodionova479/", "https://www.instagram.com/lenkatitova69/", "https://www.instagram.com/vh728999/", "https://www.instagram.com/tomynuk_yqavecuvy_547/", "https://www.instagram.com/svetazhukova5857/", "https://www.instagram.com/ftddwmqrzgdoafmoba/", "https://www.instagram.com/lobanovadaria663/", "https://www.instagram.com/solovevaanastasiia752/", "https://www.instagram.com/liudmilakulikova3669/", "https://www.instagram.com/kirabaranova3569/", "https://www.instagram.com/qdoigzrvhfexxuwkac/", "https://www.instagram.com/innamorozova7952/", "https://www.instagram.com/valiakovaleva6636/"], "user_followers": "0", "user_posts": ["https://www.instagram.com/p/CXlp0CisAA1/", "https://www.instagram.com/p/CXk4DZUMdBp/", "https://www.instagram.com/p/CXkryafshSx/", "https://www.instagram.com/p/CXjWh7YMFPf/", "https://www.instagram.com/p/CXiZ7xLs8cT/", "https://www.instagram.com/p/CXgvqxnsDcb/", "https://www.instagram.com/p/CXfwgZ-M_3p/", "https://www.instagram.com/p/CXePzABqN13/", "https://www.instagram.com/p/CXdKwvjsIFb/", "https://www.instagram.com/p/CXbkEhispuc/", "https://www.instagram.com/p/CXaoFdGsZQg/", "https://www.instagram.com/p/CXZF-BEMR1A/"], "number_sub": "\u041f\u043e\u0434\u043f\u0438\u0441\u043a\u0438", "number_followers": "941000", "number_posts": "1 227", "date_save": "2021-12-17"}


def add_new_profile():
    data = serializer_data(datas)
    print('FuCndassaddasasd')

    sql = ("INSERT INTO userprofile(id, user_name, user_link, user_sub, user_followers,"
                         " user_posts, number_sub, number_followers, number_posts, date_save)"
                         " VALUES ( %(id)s, %(user_name)s, %(user_link)s, %(user_sub)s, %(user_followers)s,"
                         " %(user_posts)s, %(number_sub)s, %(number_followers)s, %(number_posts)s, %(date_save)s)")
    cursor.execute(sql, data)
    cursor.commit()

add_new_profile()
# Разрываем подключение.
conn.close()
