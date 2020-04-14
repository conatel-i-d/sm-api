import datetime

from sqlalchemy import Integer, Column, String, JSON, DateTime
from app import db  # noqa


class Log(db.Model):  # type: ignore
    """Log Model"""

    __tablename__ = "logs"

    id = Column(Integer(), primary_key=True)
    http_method = Column(String(30))
    http_url = Column(String(30))
    payload = Column(String(1000))
    user_name = Column(String(255))
    user_email = Column(String(255))
    response_status_code = Column(Integer)
    message = Column(String(255))
    date_start = Column(DateTime(), default=datetime.datetime.utcnow)
    date_end = Column(DateTime(), default=datetime.datetime.utcnow)
    def update(self, changes):
        for key, val in changes.items():
            setattr(self, key, val)
        return self