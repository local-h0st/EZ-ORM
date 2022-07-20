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
    def __init__(self, msg):
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
        self.columns = []  # 不包含id
        self.primary_key = 0
        self.database.cursor.execute('create table ' + self.name + ' (id int primary key not null)')
        print('[Info] table \'' + table_name + '\' created.')

    def addColumns(self, column_list):
        pass

    def addColumn(self, column_name, column_type, not_null=False):
        sql = 'alter table ' + self.name + ' add column ' + column_name + ' '
        # column_type仅支持int str(size)， int对应int，str对应varchar
        if column_type == 'int':
            sql += 'int'
            self.columns.append(dict(column_name=column_name, column_type="int"))
        elif column_type[:3] == 'str':
            sql += 'varchar' + column_type[3:]
            self.columns.append(dict(column_name=column_name, column_type="str"))
        else:
            raise Error("Unsupported type '" + column_type + "'")
        if not_null:
            sql += ' not null'
        self.database.cursor.execute(sql)
        print('[Info] column \'' + column_name + '\' in table \'' + self.name + '\' created.')

    def insertRecord(self, **kwargs):
        # TODO 检查数据类型是否对应
        value_list = []
        for i in range(len(self.columns)):
            found = False
            for k, v in kwargs.items():
                if k == self.columns[i]['column_name']:
                    value_list.append(v)
                    found = True
                    break
            if not found:
                raise Error("column '" + self.columns[i] + "' not found in your args")
            # 这种检测当给定的多于需要的列的数据时，多余的那部分数据不会进入数据库，也不会报错
        # 下一步拼接sql字符串
        sql = "insert into " + self.name + " "
        # 生成(column,column,...,column)
        column_str = "(id,"
        for column in self.columns:
            column_str += column['column_name'] + ","
        column_str = column_str[:-1] + ")"
        sql += column_str + " values "
        # TODO 生成(value,value,...,value)
        value_str = "(" + str(self.primary_key) + ","
        self.primary_key += 1
        # for value in value_list:
        #     # TODO value类型需要判断
        #     value_str += value + ","
        # value_str = value_str[:-1] + ")"
        sql += value_str
        print(sql)  # TODO 还没有execute

# column_list =
#     [
#         {
#             'name':'column1',
#             'type':'int'
#         },
#         {
#             'name': 'column2',
#             'type': 'str'
#         },
#         {
#             'name': 'column3',
#             'type': 'int'
#         }
#     ]
