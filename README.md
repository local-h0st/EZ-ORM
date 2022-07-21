# EZ ORM - A Python-Sqlite ORM Framework
## test database structure in main.py :
```commandline
database:<in memory>
    |---- table:user
    |           |---- colunm:id<primary key>
    |           |---- column:username
    |---- table:comment
                |---- column:id<primary key>
                |---- column:user_comments
                |---- column:belongs_to_whom
```

## Quick start:
两个文件`EZORM.py`和`EZORM_assistance.py`需要一起放在项目目录下
```commandline
import EZORM

db = EZORM.Database('data.db', using_memory=True)
new_table = EZORM.Table(database=db, table_name='user')
new_table.addColumn(column_name='username', column_type='str(10)')

new_table.insertRecord(username='localh0st')

db.commitChange()

result = new_table.selectRecord('*', username='localh0st')
print(result)
```


## TODO
* select建议返回结果的时候也返回self.columns
* delete没写完，update没写
* 联合查询union没写