import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable = False)


class Songs(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    name = name = Column(String(250), nullable = False)
    description = Column(String())
    url = Column(String(250),nullable = False)
    g_id = Column(Integer, ForeignKey('genre.id'))


engine = create_engine('sqlite:///MusicDatabase.db')
Base.metadata.create_all(engine)