from sqlalchemy import Column, Integer,String,BigInteger,DateTime,ForeignKey,Numeric,create_engine,Boolean
from sqlalchemy.orm import declarative_base,relationship
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
link=os.getenv('link')
Base=declarative_base()
db_url=link

engine=create_engine(db_url)

class Users(Base):
    __tablename__='users'
    id=Column(Integer, primary_key=True)
    tg_id=Column(BigInteger, unique=True)
    language=Column(String(150))
    name=Column(String(150))

class Quizzes(Base):
    __tablename__='quizzes'
    id=Column(Integer, primary_key=True)
    creator_id=Column(Integer,ForeignKey('users.id', ondelete='CASCADE'),index=True)
    title=Column(String(250))
    description=Column(String(250))
    is_public=Column(Boolean,default=True)
    created_ay=Column(DateTime,default=datetime.now())

class Questions(Base):
    __tablename__='questions'
    id=Column(Integer, primary_key=True)
    quiz_id=Column(Integer,ForeignKey('quizzes.id', ondelete='CASCADE'), index=True)
    question_text=Column(String(250),nullable=False)
    question_type=Column (String(20),default='single')
    time_limit=Column(Integer)
    created_ay=Column(DateTime,default=datetime.now())

class Options(Base):
    __tablename__='options'
    id=Column(Integer, primary_key=True)  
    question_id=Column(Integer, ForeignKey(Questions.id, ondelete='CASCADE'), index=True)  
    option_text=Column(String(250),nullable=False)
    is_correct=Column(Boolean,default=False)

class QuizSession(Base):
    __tablename__='quiz_sessions'
    id=Column(Integer, primary_key=True) 
    quiz_id=Column(Integer,ForeignKey('quizzes.id', ondelete='CASCADE'),index=True)
    chat_id=Column(BigInteger,nullable=False)
    started_at=Column(DateTime,default=datetime.now())
    ended_at=Column(DateTime)

class UserAnswer(Base):
    __tablename__='user_answers'
    id=Column(Integer, primary_key=True)
    session_id=Column(Integer,ForeignKey('quiz_sessions.id'),index=True)
    user_id=Column(Integer,ForeignKey('users.id'),index=True)
    question_id=Column(Integer,ForeignKey('questions.id'),index=True)
    option_id=Column(Integer,ForeignKey('options.id'),index=True)
    answered_at=Column(DateTime,default=datetime.now())

class Results(Base):
    __tablename__='user_answers'
    id=Column(Integer, primary_key=True)
    session_id=Column(Integer,ForeignKey('quiz_sessions.id'),index=True)
    user_id=Column(Integer,ForeignKey('users.id'),index=True)
    score=Column(Integer,default=0)
    total_question=Column(Integer)
    finished_at=Column(DateTime,default=datetime.now())

Base.metadata.create_all(engine)





    