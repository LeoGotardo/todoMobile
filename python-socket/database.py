import sys, uuid, requests, os, datetime, inspect, time

from sqlalchemy import Column, Integer, String, DateTime, event, ForeignKey, create_engine
from sqlalchemy.orm import joinedload
from cryptograph import Cryptograph
from dotenv import load_dotenv
from functools import wraps
from typing import Literal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ownerId = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    done = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now())

    def __repr__(self):
        return f"<Todo(id={self.id}, title={self.title}, description={self.description}, due_date={self.due_date}, done={self.done}, created_at={self.created_at}, updated_at={self.updated_at})>"

    def to_dict(self):
        return {
            "id": self.id,
            "owener": self.session.query(User).filter(User.id == self.ownerId).first().to_dict(),
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "done": self.done,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        
    def safe_dict(self):
        return {
            "id": self.id,
            "owenerId": self.ownerId,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "done": self.done,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now())
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now())
    
    todos = relationship("Todo", back_populates="ownerId")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "todos": [todo.to_dict() for todo in self.todos]
        }
        
    def safe_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, password={self.password}, created_at={self.created_at}, updated_at={self.updated_at})>"
    
    
class Database:
    def __init__(self):
        self.engine = None
        self.session = None
        self.cryptograph = Cryptograph()

        self.setupDB()
        
    
    def setupDB(self):
        self.engine = create_engine('sqlite:///todo.db', echo=True)
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        
        
    def canHandle(f):
        @wraps(f)
        def wrapper(self, userId: str, itemType: str, method: str, item: Todo | User = None, *args, **kwargs):
            match method:
                case 'post':
                    if type(item) == User and item.id == userId:
                        return f(self, item, *args, **kwargs)
                    else:
                        return False, f'You are not authorized to {method} this item'
                case 'get':
                        success, items = f(self, item, *args, **kwargs)
                        if success:
                            l1 = len(items)
                            items = [item.to_dict() for item in items if item.ownerId == userId]
                            l2 = len(items)
                            if l1 != l2:
                                return False, f'You are not authorized to {method} this item'
                            else:
                                return True, items
                        else:
                            return False, items
                case _:
                    return False, f'Invalid method {method}'
        return wrapper
    

#Todo Methods
    def addTodo(self, title: str, description: str, due_date: datetime, ownerId: str):
        try:
            user = Todo(title=title, description=description, due_date=due_date, ownerId=ownerId, created_at=datetime.now(), updated_at=datetime.now())
            self.session.add(user)
            self.session.commit()
            return True, user
        except Exception as e:
            self.session.rollback()
            error = f'{type(e).__name__}: {e} in line {sys.exc_info()[-1].tb_lineno} in file {sys.exc_info()[-1].tb_frame.f_code.co_filename}'
            return False, error
        
    
    def getTodo(self, todoiId: str):
        try:
            todo = self.session.query(Todo).filter(Todo.id == todoiId).first()
            return True, todo
        except Exception as e:
            error = f'{type(e).__name__}: {e} in line {sys.exc_info()[-1].tb_lineno} in file {sys.exc_info()[-1].tb_frame.f_code.co_filename}'
            return False, error
        
    
    def editTodo(self, todoiId: str, title: str = None, description: str = None, due_date: datetime = None, ownerId: str = None):
        try:
            todo = self.session.query(Todo).filter(Todo.id == todoiId).first()
            if title:
                todo.title = title
            if description:
                todo.description = description
            if due_date:
                todo.due_date = due_date
            if ownerId:
                todo.ownerId = ownerId
            todo.updated_at = datetime.now()
            self.session.commit()
            return True, todo
        except Exception as e:
            self.session.rollback()
            error = f'{type(e).__name__}: {e} in line {sys.exc_info()[-1].tb_lineno} in file {sys.exc_info()[-1].tb_frame.f_code.co_filename}'
            return False, error
        
    
    def deleteTodo(self, todoiId: str):
        try:
            todo = self.session.query(Todo).filter(Todo.id == todoiId).first()
            self.session.delete(todo)
            self.session.commit()
            return True, todo
        except Exception as e:
            self.session.rollback()
            error = f'{type(e).__name__}: {e} in line {sys.exc_info()[-1].tb_lineno} in file {sys.exc_info()[-1].tb_frame.f_code.co_filename}'
            return False, error
        
        
    def getUserTodos(self, ownerId: str):
        try:
            todos = self.session.query(Todo).filter(Todo.ownerId == ownerId).all()
            return True, todos
        except Exception as e:
            error = f'{type(e).__name__}: {e} in line {sys.exc_info()[-1].tb_lineno} in file {sys.exc_info()[-1].tb_frame.f_code.co_filename}'
            return False, error
        
    
    
#User Methods
    def addUser(self, username: str, password: str):
        try:
            user = User(username=username, password=self.cryptograph.encrypt(password))
            self.session.add(user)
            self.session.commit()
            return True, user
        except Exception as e:
            self.session.rollback()
            error = f'{type(e).__name__}: {e} in line {sys.exc_info()[-1].tb_lineno} in file {sys.exc_info()[-1].tb_frame.f_code.co_filename}'
            return False, error
        
    
    def getUser(self, userId: str):
        try:
            user = self.session.query(User).filter(User.id == userId).first()
            return True, user
        except Exception as e:
            error = f'{type(e).__name__}: {e} in line {sys.exc_info()[-1].tb_lineno} in file {sys.exc_info()[-1].tb_frame.f_code.co_filename}'
            return False, error
        
    
    def editUser(self, userId: str, username: str = None, password: str = None):
        try:
            user = self.session.query(User).filter(User.id == userId).first()
            if username:
                user.username = username
            if password:
                user.password = self.cryptograph.encrypt(password)
            self.session.commit()
            return True, user
        except Exception as e:
            self.session.rollback()
            error = f'{type(e).__name__}: {e} in line {sys.exc_info()[-1].tb_lineno} in file {sys.exc_info()[-1].tb_frame.f_code.co_filename}'
            return False, error
        
    
    def deleteUser(self, userId: str):
        try:
            user = self.session.query(User).filter(User.id == userId).first()
            self.session.delete(user)
            self.session.commit()
            return True, user
        except Exception as e:
            self.session.rollback()
            error = f'{type(e).__name__}: {e} in line {sys.exc_info()[-1].tb_lineno} in file {sys.exc_info()[-1].tb_frame.f_code.co_filename}'
            return False, error
        
    
    def loginUser(self, username: str, password: str):
        try:
            user = self.session.query(User).filter(User.username == username).first()
            if user and self.cryptograph.decrypt(user.password, password):
                return True, user
            else:
                return False, 'Invalid username or password'
        except Exception as e:
            error = f'{type(e).__name__}: {e} in line {sys.exc_info()[-1].tb_lineno} in file {sys.exc_info()[-1].tb_frame.f_code.co_filename}'
            return False, error