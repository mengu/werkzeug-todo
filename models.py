# -*- coding: utf-8 -*-
from sqlalchemy import Table, Column, Integer, String, Text, DateTime, MetaData, ForeignKey, create_engine, BLOB, Unicode
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from markdown import markdown

Session = sessionmaker()
engine = create_engine("mysql://root:s@localhost/todo")
Session.configure(bind=engine)
session = Session()
Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(Unicode(150))
    password = Column(Unicode(32))

    todos = relation("ToDo", backref="user")

    def __init__(self, email, password):
        self.email = email
        self.password = password

class ToDo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    title = Column(Unicode(150))
    text = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    dateline = Column(DateTime)

    todofile = relation("File", backref="todo")

    def __init__(self, title, text, user):
        self.title = title
        self.text = text
        self.user_id = user
        self.dateline = datetime.now()

    @property
    def text_html(self):
        return markdown(self.text)

class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    todo_id = Column(Integer, ForeignKey('todo.id'))
    filename = Column(Unicode(100))
    filecontent = Column(BLOB)

    def __init__(self, todo, filename, filecontent):
        self.todo_id = todo
        self.filename = filename
        self.filecontent = filecontent

