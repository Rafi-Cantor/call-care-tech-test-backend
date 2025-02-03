from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import validates, relationship
import bcrypt
from app import db


class UserModel(db.Model):
    __tablename__ = "users"

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    xp = Column(Integer, default=0, nullable=False)
    current_level_id = Column(Integer, ForeignKey("levels.level_id", ondelete="SET NULL"), nullable=True, default=0)

    current_level = relationship("LevelModel", back_populates="users")

    @validates("password")
    def hash_password(self, key, password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @validates('xp')
    def validate_xp(self, key, value):
        if value:
            if value < 0 or value > 100:
                raise ValueError('xp must be between 0 and 100.')
        return value

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))


class LevelModel(db.Model):
    __tablename__ = "levels"

    level_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    code = Column(String, unique=True, nullable=False)

    users = relationship("UserModel", back_populates="current_level")
