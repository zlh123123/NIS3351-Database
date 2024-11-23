from .connection import create_connection
from manufacture.class_database import Request

# 增加request 输入被申请的notice_id和申请类(包括申请人user_id 申请人联系方式和应答状态) 返回是否成功 若该申请人已经申请过返回False
def add_request(notice_id: int, request_to_add: Request):
    conn = create_connection()
    cur = conn.cursor()

    # 检查是否已经申请过
    sql_1 = """
        SELECT *
        FROM Requests
        WHERE user_id = (%s) AND notice_id = (%s)
    """
    val_1 = (request_to_add.id, notice_id)
    cur.execute(sql_1, val_1)
    if cur.rowcount:
        cur.close()
        conn.close()
        return False

    # 插入新申请
    sql_2 = """
        INSERT INTO Requests (user_id, notice_id, request_contact, answer_state)
        VALUES (%s, %s, %s, %s)
    """
    val_2 = (
        request_to_add.id,
        notice_id,
        request_to_add.contact,
        request_to_add.answer_state,
    )
    cur.execute(sql_2, val_2)

    if_success = cur.rowcount > 0

    if if_success:
        conn.commit()

    cur.close()
    conn.close()
    return if_success


# 删除request 输入被申请的notice_id和 申请人user_id 返回是否成功 若该申请不存在返回False
def delete_request(notice_id: int, user_id: int):
    conn = create_connection()
    cur = conn.cursor()

    # 检查申请是否存在
    sql_1 = """
        SELECT *
        FROM Requests
        WHERE user_id = (%s) AND notice_id = (%s)
    """
    val_1 = (user_id, notice_id)
    cur.execute(sql_1, val_1)
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return False

    # 删除申请
    sql_2 = """
        DELETE
        FROM Requests
        WHERE user_id = (%s) AND notice_id = (%s)
    """
    val_2 = (user_id, notice_id)
    cur.execute(sql_2, val_2)

    if_success = cur.rowcount > 0

    if if_success:
        conn.commit()

    cur.close()
    conn.close()
    return if_success


# 更改reqeust状态 输入被申请的notice_id和申请类(包括申请人user_id 申请人联系方式和应答状态) 返回是否成功
def change_request_state(notice_id: int, request_to_change: Request):
    conn = create_connection()
    cur = conn.cursor()

    # 更新申请状态
    sql = """
        UPDATE Requests
        SET request_contact = (%s), answer_state = (%s)
        WHERE user_id = (%s) AND notice_id = (%s);
    """
    val = (
        request_to_change.contact,
        request_to_change.answer_state,
        request_to_change.id,
        notice_id,
    )
    cur.execute(sql, val)

    if_success = cur.rowcount > 0

    if if_success:
        conn.commit()

    cur.close()
    conn.close()

    return if_success


# 查看某个request的应答状态 返回应答状态 未查询到返回None
def check_request(user_id: int, notice_id: int):
    conn = create_connection()
    cur = conn.cursor()

    # 查询申请状态
    sql = """
        SELECT answer_state
        FROM Requests
        WHERE user_id = (%s) AND notice_id = (%s)
    """
    val = (user_id, notice_id)
    cur.execute(sql, val)

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    ans = cur.fetchone()
    cur.close()
    conn.close()

    return ans


# 查看用户申请的需求 返回一个list 未查询到返回None
def check_user_request_list(id: int):
    request_list = []
    conn = create_connection()
    cur = conn.cursor()

    # 查询用户申请的需求
    sql = """
        SELECT notice_id
        FROM Requests
        WHERE user_id = (%s)
    """
    val = id
    cur.execute(sql, val)

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    for line in cur.fetchall():
        request_list.append(line[0])

    cur.close()
    conn.close()

    return request_list


# 查看用户拥有的需求 返回一个list 未查询到返回None
def check_user_own_list(id: int):
    notice_list = []
    conn = create_connection()
    cur = conn.cursor()

    # 查询用户拥有的需求
    sql = """
        SELECT notice_id
        FROM Notice
        WHERE user_id = (%s)
    """
    val = id
    cur.execute(sql, val)

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    for line in cur.fetchall():
        notice_list.append(line[0])

    cur.close()
    conn.close()

    return notice_list


# 查看某个需求的申请列表 返回一个list 未查询到返回None
def check_notice_request_list(id: int):
    request_list = []
    conn = create_connection()
    cur = conn.cursor()

    # 查询某个需求的申请列表
    sql = """
        SELECT user_id
        FROM Requests
        WHERE notice_id = (%s)
    """
    val = id
    cur.execute(sql, val)

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    for line in cur.fetchall():
        request_list.append(line[0])

    cur.close()
    conn.close()

    return request_list
