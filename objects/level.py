from utils.database import get_session, transaction_scope
from app.models import models


class Level:
    def __init__(self, level_id: int, name: str, description: str, code: str):
        self.level_id = level_id
        self.name = name
        self.description = description
        self.code = code

    @classmethod
    def create(cls, name: str, description: str, code: str):
        session = get_session()
        with transaction_scope(session=session) as s:
            level = models.LevelModel(name=name, description=description, code=code)
            s.add(level)
        return cls.from_level_id(level.level_id)

    @classmethod
    def from_level_id(cls, level_id):
        session = get_session()
        with transaction_scope(session=session) as s:
            level = s.query(models.LevelModel).filter_by(level_id=level_id).first()
        if not level:
            return None
        return cls(
            level_id=level.level_id,
            name=level.name,
            description=level.description,
            code=level.code
        )


class Levels:
    @staticmethod
    def get_all_levels():
        session = get_session()
        with transaction_scope(session=session) as s:
            levels = s.query(models.LevelModel).all()
        return [Level(level_id=l.level_id, name=l.name, description=l.description, code=l.code) for l in levels]
