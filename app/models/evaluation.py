from app.database import db
from sqlalchemy import Integer, Column, Boolean, BigInteger
from time import time as time_now


class Evaluation(db.Base):
    __tablename__ = 'evaluations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    factor1 = Column(Integer)
    factor2 = Column(Integer)
    points = Column(Integer)
    count = Column(Integer)

    def __init__(self, user_id: int, factor1: int, factor2: int, points: int, count: int = 1):
        self.user_id = user_id
        self.factor1 = factor1
        self.factor2 = factor2
        self.result = factor1 * factor2
        self.points = points
        self.count = count
