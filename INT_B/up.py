import pymysql

    # 数据库配置信息
config = {
'user': 'root',
'password': '',
'host': 'localhost',
'database': 'INT_data'
}
# 连接到数据库
connection = pymysql.connect(user=config['user'],
                                password=config['password'],
                                host=config['host'],
                                database=config['database'],
                                port=3306,
                                cursorclass=pymysql.cursors.DictCursor)


def read_file(file_path):
    """读取文件并返回每一行的字典"""
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            # 分割行，提取列名和值
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                data[key] = value
    return data


def insert_data_to_mysql(data):
    """将数据插入到 MySQL 数据库中"""
    try:
        with connection.cursor() as cursor:
            # 创建 SQL 插入语句
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            sql = f"""
            INSERT INTO server_data ({columns}) 
            VALUES ({placeholders}) 
            ON DUPLICATE KEY UPDATE 
            {", ".join([f"{col}=VALUES({col})" for col in columns.split(", ")])}
            """

            # 执行插入操作
            cursor.execute(sql, list(data.values()))
            connection.commit()
    finally:
        connection.close()

def main():
    file_path = 'node-info.txt'
    data = read_file(file_path)
    insert_data_to_mysql(data)

if __name__ == '__main__':
    main()
