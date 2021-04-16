from app.database import db
from sqlalchemy import Integer, Column, Boolean, BigInteger, ForeignKey
from time import time as time_now
from sqlalchemy.orm import relationship


class LogEntry(db.Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', foreign_keys=[user_id])
    factor1 = Column(Integer)
    factor2 = Column(Integer)
    user_result = Column(Integer)
    correct = Column(Boolean)
    timestamp = Column(BigInteger)
    duration = Column(Integer)

    def __init__(self, user, factor1: int, factor2: int, user_result: int, correct: bool, duration: int):
        self.user = user
        self.factor1 = factor1
        self.factor2 = factor2
        self.user_result = user_result
        self.correct = correct
        self.timestamp = int(time_now())
        self.duration = duration
