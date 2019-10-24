from sqlalchemy import Integer, Column, String
from app import db  # noqa


class Switch(db.Model):  # type: ignore
    """Switch Model"""

    __tablename__ = "switch"

    id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    model = Column(String(255))

    def update(self, changes):
        for key, val in changes.items():
            setattr(self, key, val)
        return self