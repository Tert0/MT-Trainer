from app.database import db
from sqlalchemy import Integer, Column, Boolean, String


class User(db.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(255))
    admin = Column(Boolean)

    def __init__(self, username: str, password: str, admin: bool = False):
        self.username = username
        self.password = password
        self.admin = admin
