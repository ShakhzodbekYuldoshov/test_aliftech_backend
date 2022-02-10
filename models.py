'''
Database models 
'''

from sqlalchemy import Integer, Float, String, Column
from database  import Base


class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    body_fat_percent = Column(Float)
    diastolic = Column(Float)
    systolic = Column(Float)
    grip_force = Column(Float)
    sit_and_bend_forward_cm = Column(Float)
    sit_ups_count = Column(Float)
    broad_jump_cm = Column(Float)
    gender=Column(String)
    classification_probability=Column(Float)
