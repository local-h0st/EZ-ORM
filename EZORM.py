import sqlite3
from functools import wraps


# decorator
def log(msg):
    def rtmWrappedFunc(f):
        @wraps(f)
        def wrappedFunc(*args, **kwargs):
            print('[log info]', msg)
            return f(*args, **kwargs)

        return wrappedFunc

    return rtmWrappedFunc



# def commitChange(database):
#     def rtmWrappedFunc(f):
#         @wraps(f)
#         def wrappedFunc(*args, **kwargs):
#             rst = f(*args, **kwargs)
#             database.connect.commit()
#             return rst
#         return wrappedFunc
#     return rtmWrappedFunc



# end decorator


# error class
class Error(Exception):
    def __init__(self,msg):
        self.message = msg

    def message(self):
        return self.message

# error class

class Database(object):
    def __init__(self, database_name='Default database', using_memory=False):
        if using_memory:
            database_name = ':memory:'
        self.connect = sqlite3.connect(database_name)
        self.cursor = self.connect.cursor()
        print('[Info] database connected.')

    def __del__(self):
        self.cursor.close()
        self.connect.close()
        print('[Info] database closed.')

    def commitChange(self):
        self.connect.commit()

    def exec_sql(self, sql):
        self.cursor.execute(sql)
        print(self.cursor.fetchall())


class Table(object):
    # 初始化一张表的时候自带主键column:id并且自增
    def __init__(self, database, table_name):
        self.database = database
        self.name = table_name
        self.columns = []   # 不包含id
        self.primary_key = 0
        self.database.cursor.execute('create table ' + self.name + ' (id int primary key not null)')
        print('[Info] table \'' + table_name + '\' created.')

    def addColumns(self, column_list):
        pass

    def addColumn(self, column_name, column_type, not_null=False):
        sql = 'alter table ' + self.name + ' add column ' + column_name + ' ' + column_type
        if not_null:
            sql += ' not null'
        self.database.cursor.execute(sql)
        self.columns.append(column_name)
        print('[Info] column \'' + column_name + '\' in table \'' + self.name + '\' created.')

    def insertRecord(self, **kwargs):
        # TODO check
        value_list = []
        for i in range(len(self.columns)):
            found = False
            for k, v in kwargs.items():
                if k == self.columns[i]:
                    value_list.append(v)
                    found = True
                    break
            if not found:
                raise Error("column '" + self.columns[i] + "' not found in your args")
            # 这种检测当给定的多于需要的列的数据时，多余的那部分数据不会进入数据库，也不会报错
        # 下一步拼接sql字符串
        sql = "insert"








# column_list =
#     [
#         {
#             'name':'column1',
#             'type':'int'
#         },
#         {
#             'name': 'column2',
#             'type': 'int'
#         },
#         {
#             'name': 'column3',
#             'type': 'int'
#         }
#     ]
