from sqlalchemy import Integer, Column, String, JSON
from app import db  # noqa


class Result(db.Model):  # type: ignore
    """Result Model"""

    __tablename__ = "result"

    id = Column(Integer(), primary_key=True)
    job_id = Column(Integer(), unique=True)
    type = Column(String(255))
    data = Column(JSON)

    def update(self, changes):
        for key, val in changes.items():
            setattr(self, key, val)
        return self