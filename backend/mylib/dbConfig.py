import pymysql

"""数据源配置信息"""
localSourceConfig = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': 'Ab123456',
    'db': 'sports_facility_management',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor
}



