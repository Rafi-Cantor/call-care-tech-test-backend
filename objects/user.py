from utils.database import get_session, transaction_scope
from app.models import models


class UserAlreadyExistsError(Exception):
    pass


class UserDoesntExistError(Exception):
    pass


class User:
    def __init__(self, user_id: int, user_name: str, is_admin: bool, xp: int = None, current_level_id: int = None):
        self.user_id = user_id
        self.user_name = user_name
        self.is_admin = is_admin
        self.xp = xp
        self.current_level_id = current_level_id

    @classmethod
    def create(cls, user_name, is_admin, password, xp: int = None, current_level_id: int = None):
        session = get_session()
        with transaction_scope(session=session) as s:
            existing_user = s.query(models.UserModel).filter_by(user_name=user_name).first()
            if existing_user:
                raise UserAlreadyExistsError(f"User with username '{user_name}' already exists.")
            user = models.UserModel(
                user_name=user_name,
                password=password,
                is_admin=is_admin,
                xp=xp,
                current_level_id=current_level_id
            )
            s.add(user)

        return cls.from_user_name(user.user_name)

    @classmethod
    def from_user_name(cls, user_name):
        session = get_session()
        with transaction_scope(session=session) as s:
            user = s.query(models.UserModel).filter_by(user_name=user_name).first()
        if not user:
            return None
        return cls(
            user_id=user.user_id,
            user_name=user.user_name,
            is_admin=user.is_admin,
            xp=user.xp,
            current_level_id=user.current_level_id
        )

    @classmethod
    def from_user_id(cls, user_id):
        session = get_session()
        with transaction_scope(session=session) as s:
            user = s.query(models.UserModel).filter_by(user_id=user_id).first()
        if not user:
            return None
        return cls(
            user_id=user.user_id,
            user_name=user.user_name,
            is_admin=user.is_admin,
            xp=user.xp,
            current_level_id=user.current_level_id
        )

    @staticmethod
    def all_employees():
        session = get_session()
        with transaction_scope(session=session) as s:
            employees = s.query(models.UserModel).filter_by(is_admin=False).all()
        return [User(user_id=u.user_id,
                     user_name=u.user_name,
                     is_admin=u.is_admin,
                     xp=u.xp,
                     current_level_id=u.current_level_id
                     ) for u in employees]

    @staticmethod
    def all_admins():
        session = get_session()
        with transaction_scope(session=session) as s:
            admins = s.query(models.UserModel).filter_by(is_admin=True).all()
        return [User(user_id=u.user_id,
                     user_name=u.user_name,
                     is_admin=u.is_admin,
                     xp=u.xp,
                     current_level_id=u.current_level_id
                     ) for u in admins]

    def update_xp(self, xp: int):
        session = get_session()
        with transaction_scope(session=session) as s:
            user = s.query(models.UserModel).filter_by(user_id=self.user_id).first()
            if not user:
                raise UserDoesntExistError(f"User with user id '{self.user_id}' doesnt exist.")
            user.xp = xp

    def update_level(self, current_level_id: int):
        session = get_session()
        with transaction_scope(session=session) as s:
            user = s.query(models.UserModel).filter_by(user_id=self.user_id).first()
            if not user:
                raise UserDoesntExistError(f"User with user id '{self.user_id}' doesnt exist.")
            user.current_level_id = current_level_id

    def update_level_and_xp(self, xp: int, current_level_id: int):
        session = get_session()
        with transaction_scope(session=session) as s:
            user = s.query(models.UserModel).filter_by(user_id=self.user_id).first()
            if not user:
                raise UserAlreadyExistsError(f"User with user id '{self.user_id}' doesnt exist.")
            user.xp = xp
            user.current_level_id = current_level_id

    def check_password(self, password: str) -> bool:
        session = get_session()
        with transaction_scope(session=session) as s:
            user = s.query(models.UserModel).filter_by(user_id=self.user_id).first()
            if not user:
                raise UserDoesntExistError(f"User with user id '{self.user_id}' doesn't exist.")
        return user.check_password(password)




