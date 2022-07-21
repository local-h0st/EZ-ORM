# Python实现一个ORM，对常用sql语句进行支持，以sqlite作为基本数据库
# sqlite基于文件，比较小型
# conn = sqlite3.connect(':memory:')    # 会在内存中创建数据库

import EZORM

EZORM.update_config(DEBUG=True)

db = EZORM.Database('data.db', using_memory=True)

table_user = EZORM.Table(database=db, table_name='user')
table_user.addColumn(column_name='username', column_type='str(10)')

table_comment = EZORM.Table(database=db, table_name='comments')
table_comment.addColumn(column_name='user_comments', column_type='str(10)')
table_comment.addColumn(column_name='belongs_to_whom', column_type='str(100)')

print("############# insert ############")
table_user.print_info()
table_user.insertRecord(username='localh0st')
table_user.insertRecord(username='purelov3')
table_comment.print_info()
table_comment.insertRecord(user_comments='l1', belongs_to_whom='localh0st')
table_comment.insertRecord(user_comments='l2', belongs_to_whom='localh0st')
table_comment.insertRecord(user_comments='p1', belongs_to_whom='purelov3')

print("############ select ##############")
print(table_comment.selectRecord('user_comments', 'belongs_to_whom', belongs_to_whom='localh0st'))

# result = db.exec_sql("select * from user")
# print(result)
# result = db.exec_sql("select * from comments")
# print(result)


# print(type(result[0][0]))     # [(0, 'localh0st')]    <class 'int'>
# db.exec_sql("insert into user (id, username) values (1, 'localh0st')")
# db.exec_sql("insert into user (id, username) values (3, 'lt')")
# db.exec_sql("select * from user")
db.commitChange()
