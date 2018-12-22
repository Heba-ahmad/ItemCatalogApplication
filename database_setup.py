#!/usr/bin/env python
# Module to set up database.
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# class to create the user table
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    provider = Column(String(25))


# Class to create the perfumes Category table
class Categories(Base):
    __tablename__ = 'perfumes'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    intro = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """ return Categories data in serializable format"""

        return {
            'name': self.name,
            'id': self.id,
            'intro': self.intro,
            'user_id': self.user_id
        }


# Class to create the item (favorite perfumes) table
class TopSelections(Base):
    __tablename__ = 'favorite'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    img_url = Column(String(550), nullable=True)
    description = Column(String(250), nullable=True)
    perfume_id = Column(Integer, ForeignKey('perfumes.id'))
    category = relationship(Categories, single_parent=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """ return TopSelections data in serializable format"""

        return {
            'name': self.name,
            'description': self.description,
            'img_url': self.img_url,
            'id': self.id,
            'user_id': self.user_id,
            'perfume_id': self.perfume_id
        }


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
