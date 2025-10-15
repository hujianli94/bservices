# coding: utf-8
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from oslo_db.sqlalchemy import models

BASE = declarative_base()


class TestData(Base, models.ModelBase):
    """测试数据模型"""
    __tablename__ = 'test_data'

    id = Column(Integer, primary_key=True)
    data = Column(String(255), nullable=False)
    create_time = Column(DateTime, default=datetime.datetime.utcnow)
    update_time = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def save(self, session):
        session.add(self)
        session.flush()
        return self

    def delete(self, session):
        session.delete(self)
        session.flush()
        return True

    def __repr__(self):
        return f"<TestData(id={self.id}, data={self.data})>"

    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            "create_time": self.create_time.isoformat(),
            "update_time": self.update_time.isoformat()
        }
