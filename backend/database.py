from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func


# SQLALCHEMY_DATABASE_URL = 'sqlite:///./coronavirus.sqlite3'
# SQLALCHEMY_DATABASE_URL = "postgresql://username:password@host:port/database_name"
# MySQL或PostgreSQL的连接方法如下
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:711004szheli@127.0.0.1:3306/easyparkingsystem"

engine = create_engine(
    # echo=True表示引擎将用repr()函数记录所有语句及其参数列表到日志
    # 由于SQLAlchemy是多线程，指定check_same_thread=False来让建立的对象任意线程都可使用。这个参数只在用SQLite数据库时设置
    # SQLALCHEMY_DATABASE_URL, encoding='utf-8', echo=True, connect_args={'check_same_thread': False}
    SQLALCHEMY_DATABASE_URL, echo=True
)

metadata = MetaData()

# 创建所有表
metadata.create_all(engine)

# 在SQLAlchemy中，CRUD都是通过会话(session)进行的，所以我们必须要先创建会话，每一个SessionLocal实例就是一个数据库session
# flush()是指发送数据库语句到数据库，但数据库不一定执行写入磁盘；commit()是指提交事务，将变更保存到数据库文件
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)

# 创建基本映射类
Base = declarative_base(name='Base')