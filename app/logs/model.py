import datetime

from sqlalchemy import Integer, Column, String, JSON, DateTime
from app import db  # noqa


class Log(db.Model):  # type: ignore
    """Log Model"""

    __tablename__ = "logs"

    id = Column(Integer(), primary_key=True)
    event_type = Column(String(30))
    event_result = Column(String(30))
    entity = Column(String(30))
    payload = Column(String(500))
    user_id = Column(String(255), unique=True)
    date = Column(DateTime(), default=datetime.datetime.utcnow)

    def update(self, changes):
        for key, val in changes.items():
            setattr(self, key, val)
        return self