import pymysql
from pymysql.cursors import DictCursor
import config

def check_mysql_data():
    connection = pymysql.connect(**config.DB_CONFIG)

    with connection.cursor(DictCursor) as cursor:
        sql = "select * from new_phones_test limit 100"
        cursor.execute(sql)
        # 获取所有结果
        return cursor.fetchall()

if __name__ == '__main__':
    data = check_mysql_data()
    for i in data:
        print(i)