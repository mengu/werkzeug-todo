from sqlalchemy import Table, Column, Integer, String, Text, DateTime, MetaData, ForeignKey, create_engine
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relation, backref
from datetime import datetime
from markdown import markdown

metadata = MetaData()
Session = sessionmaker()
engine = create_engine("mysql://root:s@localhost/todo")
Session.configure(bind=engine)
session = Session()

user_table = Table('user', metadata,
    Column('userid', Integer, primary_key=True),
    Column('email', String(100)),
    Column('password', String(32))
)

todo_table = Table('todo', metadata,
    Column('todoid', Integer, primary_key=True),
    Column('title', String(100)),
    Column('text', Text),
    Column('user_id', Integer, ForeignKey('user.userid')),
    Column('dateline', DateTime)
)

class ToDo(object):
    def __init__(self, title, text, user):
        self.title = title
        self.text = text
        self.user_id = user
        self.dateline = datetime.now()

    @property
    def text_html(self):
        return markdown(self.text)

class User(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User %s>" % self.email

mapper(User, user_table, properties={'todos': relation(ToDo, backref='user')})
mapper(ToDo, todo_table)

