# from flask import Flask




from flask import (
    Blueprint, render_template,request
)

bp = Blueprint('jumpserver_user_delete', __name__)






# @app.route('/delete_user/<name>', methods=['GET'])




def delete_user(deleteuser):
    import pymysql
    connection = pymysql.connect(host='10.2.1.125', port=3306, user='jumpserver', password='jumpserver',
                                 db='jumpserver', charset='utf8')

    print(deleteuser)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `juser_user` WHERE `username`=%s"
            cursor.execute(sql, (deleteuser,))
            result = cursor.fetchone()
            if result:
                result = list(result)
                print(result)

                forbidden_sql = "UPDATE `juser_user` SET  is_active=0  WHERE `username`=%s"
                print(forbidden_sql)
                cursor.execute(forbidden_sql, (deleteuser,))
                forbidden_result = cursor.fetchone()
                connection.commit()
                print(forbidden_result)
                return "200"

            else:
                print('无此用户！')
                return "300"
    finally:
        connection.close()


