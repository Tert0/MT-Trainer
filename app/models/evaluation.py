from app.database import db
from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship


class Evaluation(db.Base):
    __tablename__ = 'evaluations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', foreign_keys=[user_id])
    factor1 = Column(Integer)
    factor2 = Column(Integer)
    points = Column(Integer)
    count = Column(Integer)

    def __init__(self, user, factor1: int, factor2: int, points: int, count: int = 1):
        self.user = user
        self.factor1 = factor1
        self.factor2 = factor2
        self.result = factor1 * factor2
        self.points = points
        self.count = count
