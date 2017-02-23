import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Job(Base):
    __tablename__ = 'job'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    remote_id = Column(String(1000))
    snapshoted_at =  Column(String(1000))

    title = Column(String(1000))
    description = Column(Text())
    raw_text = Column(Text())

    location =  Column(String(1000))
    type = Column(String(250))
    post_url = Column(String(2000), nullable=False)
    company_id = Column(String(250))
    company_name = Column(String(1000))
    company_url = Column(String(1000))

    source_id = Column(String(500))

class DataSource(Base):
    __tablename__ = 'data_source'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(1000))
    source_url = Column(String(30000))
    location =  Column(String(1000))
    description = Column(String(30000))


class Company(Base):
    __tablename__ = 'company'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    remote_id = Column(String(1000))
    snapshoted_at =  Column(String(1000))
    name = Column(String(1000))
    short_description = Column(Text())
    long_description = Column(Text())
    company_url = Column(String(30000))
    location =  Column(String(1000))


class CompanySite(Base):
    __tablename__ = 'company_site'

    id = Column(Integer, primary_key=True)
    snapshoted_at = Column(String(1000))
    url = Column(String(10000))
    domain =  Column(String(200))
    raw_html = Column(Text())
    justext_content = Column(Text())
    justext_json = Column(Text())
    justext_parsed = Column(Text())





# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('mysql+mysqldb://townie:hugedata@192.168.1.2/jobs?charset=utf8')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
