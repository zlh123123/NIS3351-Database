import pymysql


# 创建python和MySQL连接
def create_connection():
    conn = pymysql.connect(
        host="localhost",  # 根据你的数据库主机设置
        user="root",  # MySQL用户名
        password="123456",  # MySQL密码
        database="findpartner",  # 数据库名称
    )
    return conn
