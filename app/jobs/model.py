from sqlalchemy import Integer, Column, String, JSON
from app import db  # noqa


class Job(db.Model):  # type: ignore
    """Job Model"""

    __tablename__ = "jobs"

    id = Column(Integer(), primary_key=True)
    job_id = Column(Integer(), unique=True)
    type = Column(String(255))
    result = Column(JSON)

    def update(self, changes):
        for key, val in changes.items():
            setattr(self, key, val)
        return self