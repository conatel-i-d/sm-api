from sqlalchemy import Integer, Column, String
from app import db  # noqa


class Switch(db.Model):  # type: ignore
    """Switch Model"""

    __tablename__ = "switch"

    id = Column(Integer(), primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    model = Column(String(255))
    ip = Column(String(15))
    ansible_user = Column(String(255))
    ansible_ssh_pass = Column(String(255))
    ansible_ssh_port = Column(Integer)
    def update(self, changes):
        for key, val in changes.items():
            setattr(self, key, val)
        return self