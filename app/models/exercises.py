from app.database import db
from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship


class Exercises(db.Base):
    __tablename__ = 'exercises'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', foreign_keys=[user_id])
    factor1 = Column(Integer)
    factor2 = Column(Integer)
    result = Column(Integer)

    def __init__(self, user, factor1: int, factor2: int):
        self.user = user
        self.factor1 = factor1
        self.factor2 = factor2
        self.result = factor1 * factor2
