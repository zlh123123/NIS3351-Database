from .connection import create_connection
from manufacture.class_database import Notice


# 创建需求，输入用户id 返回notice_id 未创建成功返回None
def create_notice(user_id: int):
    conn = create_connection()
    cur = conn.cursor()

    # 插入新需求
    sql = """
        INSERT INTO Notice (user_id, notice_image, notice_basic_type, notice_title, notice_owner_contact, notice_time, notice_tag, notice_description, notice_if_disabled)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    val = (
        user_id,
        "image",
        -1,
        "unknown_title",
        "unknown_owner_contact",
        "unknown_time",
        "unknown_tag",
        "unknown_description",
        0,
    )
    cur.execute(sql, val)
    conn.commit()

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    id = cur.lastrowid

    cur.close()
    conn.close()

    return id


# 查看需求基本信息 输入需求id 返回需求类 没有查询到则返回None
def check_notice_basic_database(id: int):
    conn = create_connection()
    cur = conn.cursor()

    # 查询需求基本信息
    sql = """
        SELECT *
        FROM Notice
        WHERE notice_id = (%s)
    """
    val = id
    cur.execute(sql, val)

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    res = cur.fetchone()
    notice = Notice(id, res[1], res[5], res[4], res[3])
    notice.image = res[2]
    notice.time = res[6]
    notice.tag = res[7].split("$")
    notice.description = res[8]
    notice.if_disabled = res[9]

    cur.close()
    conn.close()

    return notice


# 返回所有需求
def check_all_notice_database():
    notice_list = []
    conn = create_connection()
    cur = conn.cursor()

    # 查询所有未禁用的需求
    sql = """
        SELECT *
        FROM Notice
        WHERE notice_if_disabled = 0
    """
    cur.execute(sql)

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    for row in cur.fetchall():
        notice_list.append(row[0])

    cur.close()
    conn.close()
    return notice_list


# 全字段检索需求 输入搜索内容，在全字段检索 返回list(需求id列表) 未查询到返回None
def search_notice_content_database(notice_content):
    notice_list = []
    conn = create_connection()
    cur = conn.cursor()

    # 全字段检索需求
    sql = """
        SELECT notice_id
        FROM Notice
        WHERE CONCAT(notice_title, notice_time, notice_tag, notice_description) like (%s)
    """
    notice_content = "%" + notice_content + "%"
    val = notice_content
    cur.execute(sql, val)

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    for row in cur.fetchall():
        notice_list.append(row[0])

    cur.close()
    conn.close()

    return notice_list


# 按照大类检索需求 输入搜索内容(某个大类Basic_Type(自定义枚举类型)) 返回list(需求id列表) 未查询到返回None
def search_notice_type_database(notice_type: int):
    notice_list = []
    conn = create_connection()
    cur = conn.cursor()

    # 按照大类检索需求
    sql = """
        SELECT notice_id
        FROM Notice
        WHERE notice_basic_type = (%s)
    """
    val = notice_type
    cur.execute(sql, val)

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    for row in cur.fetchall():
        notice_list.append(row[0])

    cur.close()
    conn.close()

    return notice_list


# 按照大类和关键字检索 关键字在除大类以外的4个用户自定义字段(小类、时间、地点、活动描述)中检索 返回list(需求id列表) 未查询到返回None
def search_notice_all_database(notice_type: int, notice_content):
    notice_list = []
    conn = create_connection()
    cur = conn.cursor()

    notice_content = "%" + notice_content + "%"
    # 按照大类和关键字检索需求
    sql = """
        SELECT notice_id
        FROM Notice
        WHERE notice_basic_type = (%s) AND CONCAT(notice_title, notice_time, notice_tag, notice_description) like (%s)
    """
    val = (notice_type, notice_content)
    cur.execute(sql, val)

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    for row in cur.fetchall():
        notice_list.append(row[0])

    cur.close()
    conn.close()

    return notice_list


# 修改需求基本信息 基本同上
def change_notice_basic_database(notice_content: Notice):
    conn = create_connection()
    cur = conn.cursor()

    # 更新需求信息
    sql = """
        UPDATE Notice
        SET notice_image = (%s), notice_basic_type = (%s), notice_title = (%s), notice_owner_contact = (%s), notice_time = (%s), notice_tag = (%s), notice_description = (%s), notice_if_disabled = (%s) 
        WHERE notice_id = (%s);
    """
    tag_str = "$".join(notice_content.tag)
    val = (
        notice_content.image,
        notice_content.basic_type,
        notice_content.title,
        notice_content.owner_contact,
        notice_content.time,
        tag_str,
        notice_content.description,
        notice_content.if_disabled,
        notice_content.id,
    )
    cur.execute(sql, val)

    if_success = cur.rowcount > 0

    if if_success:
        conn.commit()

    cur.close()
    conn.close()

    return if_success
