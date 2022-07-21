from EZORM_assistance import debug_info, Error, update_config
import sqlite3

class Database(object):
    def __init__(self, database_name='Default database', using_memory=False):
        if using_memory:
            database_name = ':memory:'
        self.connect = sqlite3.connect(database_name)
        self.cursor = self.connect.cursor()
        debug_info('database connected.')

    def __del__(self):
        self.cursor.close()
        self.connect.close()
        debug_info('database closed.')

    def commitChange(self):
        self.connect.commit()

    def exec_sql(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()


class Table(object):
    # 初始化一张表的时候自带主键column:id并且自增
    def __init__(self, database, table_name):
        self.database = database
        self.name = table_name
        self.columns = []  # 不包含id
        self.primary_key = 0
        self.database.cursor.execute('create table ' + self.name + ' (id int primary key not null)')
        debug_info('table \'' + table_name + '\' created.')

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
        debug_info('column \'' + column_name + '\' in table \'' + self.name + '\' created.')

    def print_info(self):
        info = "[Total columns: "
        info += str(len(self.columns)) + "] "
        # 不含主键id列
        for column in self.columns:
            info += column['column_name'] + "(" + column['column_type'] + ")  "
        print("-------- table info --------")
        print('[Table name]', self.name)
        print(info)
        print("----------------------------")

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
        # 生成“(column,column,...,column)”
        column_str = "(id,"
        for column in self.columns:
            column_str += column['column_name'] + ","
        column_str = column_str[:-1] + ")"
        sql += column_str + " values "
        # 生成“(value,value,...,value)”
        value_str = "(" + str(self.primary_key) + ","
        self.primary_key += 1
        for i in range(len(self.columns)):
            if self.columns[i]['column_type'] == 'int':
                value_str += value_list[i] + ","
            elif self.columns[i]['column_type'] == 'str':
                value_str += "'" + value_list[i] + "'" + ","
        value_str = value_str[:-1] + ")"
        sql += value_str
        # execute
        self.database.cursor.execute(sql)
        debug_info("record inserted, sql : " + sql)

    def deleteRecord(self, arg, by_id=False):
        # 如果by_id为True，则arg传入id值(int类型)，如果不传入by_id默认为False，则arg传入selectRecord的结果
        if by_id:
            self.database.cursor.execute("delete from " + self.name + " where id = " + str(arg))
            print("[Info] record deleted, id =", arg)
        else:
            # TODO arg传入selectRecord的结果
            pass

    def selectRecord(self, *columns, **filter):
        # TODO 没有实现orderby，没有实现or条件
        sql = "select "
        for column in columns:
            sql += column + ","
        sql = sql[:-1] + " from " + self.name
        if filter:
            sql += " where "
            for k, v in filter.items():
                that_column = {}
                for column in self.columns:
                    if column['column_name'] == k:
                        that_column = column
                if k == 'id':
                    that_column = {'column_name': 'belongs_to_whom', 'column_type': 'int'}
                if not that_column:
                    raise Error("filter not found : " + k)
                if that_column['column_type'] == 'int':
                    sql += k + "=" + str(v) + " and "
                elif that_column['column_type'] == 'str':
                    sql += k + "='" + str(v) + "' and "
            sql = sql[:-5]  # 砍掉末尾多的 and
        self.database.cursor.execute(sql)
        return self.database.cursor.fetchall()
