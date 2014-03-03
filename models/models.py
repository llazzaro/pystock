from pystock.models import Base
from sqlalchemy import Column, Integer, String


class Account(Base):
    pass


class Asset(Base):
    """
        An asset that derives value because of a contractual claim. Stocks, bonds, bank deposits, and the like are all examples of financial assets.
    """
    pass


class Tick(Base):
    """
        The minimum upward or downward movement in the price of a security. The term "tick" also refers to the change in the price of a security from trade to trade. Since 2001, with the advent of decimalization, the minimum tick size for stocks trading above $1 is 1 cent.
    """
    pass


class Quote(Base):
    pass


class Action(object):
    pass

class Type(object):
    pass


class Order(Base):
    pass


