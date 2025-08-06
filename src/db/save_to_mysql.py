# 把数据保存到MySQL
import pymysql
import json
import config

def get_txt_data():
    with open('test.txt', 'r', encoding='utf-8') as json_file:
        data_dict = json.load(json_file)

    result = data_dict['data']['output']
    return result

def save_to_mysql():
    connection = pymysql.connect(**config.DB_CONFIG)

    # 把数据格式化装入列表
    data_list = get_txt_data()
    inset_data = []
    for i in data_list:
        data = (
            i['category_id'],
            i['category_name'],
            i['price'],
            i['product_name'],
            i['publish_date'],
        )

        inset_data.append(data)

    try:
        # 构建插入SQL语句与提交
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO new_phones_test
            (category_id, category_name, price, product_name, publish_date)
            VALUES (%s, %s, %s, %s, %s)
            """

            # 批量数据插入
            cursor.executemany(sql,inset_data)

        # 提交事务
        connection.commit()
        print(f"数据库操作完成.")

    except pymysql.MySQLError as e:
        # 异常回滚
        connection.rollback()
        print(f"数据库操作异常：{e}")

    finally:
        # 资源释放
        connection.close()


if __name__ == '__main__':
    save_to_mysql()


