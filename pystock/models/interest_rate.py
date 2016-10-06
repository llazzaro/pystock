from collections import Counter

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    DECIMAL,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import object_session


from pystock import Base
from pystock.models import SecurityQuote


class InterestRateTag(Base):

    __tablename__ = 'interest_rate_tag'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class InterestRate(Base):

    __tablename__ = 'interest_rate'
    id = Column(Integer, primary_key=True)

    date = Column(DateTime)
    rate = Column(DECIMAL)
    country_iso = Column(String)
    tag = relationship('InterestRateTag', backref='tags')
    tag_id = Column(Integer, ForeignKey('interest_rate_tag.id'))
