# Python实现一个ORM，对常用sql语句进行支持，以sqlite作为基本数据库
# sqlite基于文件，比较小型
# conn = sqlite3.connect(':memory:')    # 会在内存中创建数据库

import EZORM

db = EZORM.Database('data.db', using_memory=True)

table_user = EZORM.Table(database=db, table_name='user')
table_user.addColumn(column_name='username', column_type='varchar(10)')

table_comment = EZORM.Table(database=db, table_name='comment')
table_comment.addColumn(column_name='user_comments', column_type='varchar(10)')
table_comment.addColumn(column_name='belongs_to_whom', column_type='varchar(100)')

db.commitChange()

db.exec_sql("select * from user")
# db.exec_sql("insert into user (id, username) values (1, 'localh0st')")
# db.exec_sql("insert into user (id, username) values (3, 'lt')")
# db.exec_sql("select * from user")
