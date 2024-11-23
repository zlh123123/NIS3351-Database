from .connection import create_connection
from manufacture.class_database import User

# 创建用户 输入用户名 返回user_id 用户名已存在返回None
def create_user(name):
    conn = create_connection()
    cur = conn.cursor()

    # 检查用户名是否已存在
    sql_1 = """
        SELECT user_name
        FROM Users
        WHERE user_name = (%s)
    """
    val_1 = name
    cur.execute(sql_1, val_1)
    if cur.rowcount:
        cur.close()
        conn.close()
        return None

    # 插入新用户
    sql_2 = """
        INSERT INTO Users (user_name, user_nickname, user_psword, user_sex, user_hobby, user_image, user_introduction)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    val_2 = (
        name,
        name,
        "psword",
        "unknown",
        "hobby",
        "https://gss0.bdstatic.com/6LZ1dD3d1sgCo2Kml5_Y_D3/sys/portraith/item/tb.1.bead35fc.MtiwdXhDXbnsPJ6EQHv6kg",
        "introduction",
    )
    cur.execute(sql_2, val_2)
    conn.commit()
    id = cur.lastrowid

    cur.close()
    conn.close()

    return id


# 查看用户基本信息 输入用户id 返回用户类 没有查询到则返回None
def check_user_basic_database(id: int):
    conn = create_connection()
    cur = conn.cursor()

    # 查询用户基本信息
    sql = """
        SELECT *
        FROM Users
        WHERE user_id = (%s)
    """
    val = id
    cur.execute(sql, val)

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    res = cur.fetchone()
    user = User(id, res[1], res[3])
    user.nickname = res[2]
    user.sex = res[4]
    user.hobby = res[5]
    user.image = res[6]
    user.introduction = res[7]

    cur.close()
    conn.close()

    return user


# 修改用户基本信息 输入用户修改后的内容 把该id下的非空内容全部用user_content的内容替换 返回是否修改成功
def change_user_basic_database(user_content: User):
    conn = create_connection()
    cur = conn.cursor()

    # 更新用户信息
    sql = """
        UPDATE Users
        SET user_name = (%s), user_nickname = (%s), user_psword = (%s), user_sex = (%s), user_hobby = (%s), user_image = (%s), user_introduction = (%s)
        WHERE user_id = (%s);
    """
    val = (
        user_content.user_name,
        user_content.nickname,
        user_content.passwords,
        user_content.sex,
        user_content.hobby,
        user_content.image,
        user_content.introduction,
        user_content.id,
    )
    cur.execute(sql, val)
    conn.commit()

    if_success = cur.rowcount > 0

    cur.close()
    conn.close()

    return if_success


# 根据用户id查找用户名 找不到返回 None
def user_id_to_name(id: int):
    conn = create_connection()
    cur = conn.cursor()

    # 根据用户ID查询用户名
    sql = """
        SELECT user_name
        FROM Users
        WHERE user_id = (%s)
    """
    val = id
    cur.execute(sql, val)

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    res = cur.fetchone()
    name = res[0]

    cur.close()
    conn.close()

    return name


# 根据用户名查找用户id 找不到返回 None
def user_name_to_id(name):
    conn = create_connection()
    cur = conn.cursor()

    # 根据用户名查询用户ID
    sql = """
        SELECT user_id
        FROM Users
        WHERE user_name = (%s)
    """
    val = name
    cur.execute(sql, val)

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    res = cur.fetchone()
    id = res[0]

    cur.close()
    conn.close()

    return id
