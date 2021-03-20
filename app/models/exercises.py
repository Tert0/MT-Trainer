from app.database import db
from sqlalchemy import Integer, Column, Boolean, BigInteger
from time import time as time_now


class Exercises(db.Base):
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    factor1 = Column(Integer)
    factor2 = Column(Integer)
    result = Column(Integer)

    def __init__(self, user_id: int, factor1: int, factor2: int):
        self.user_id = user_id
        self.factor1 = factor1
        self.factor2 = factor2
        self.result = factor1 * factor2
