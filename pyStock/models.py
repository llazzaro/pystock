import datetime

from pyStock import Base

from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    DECIMAL,
    Date
)


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


class Broker(Base):
    """
        An agency broker is a broker that acts as a middle man to the stock exchange, and places trades on behalf of clients.
    """
    __tablename__ = 'pystock_broker'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def commission(self, asset):
        pass


class Account(Base):
    """

    """
    __tablename__ = 'pystock_account'

    id = Column(Integer, primary_key=True)
    broker_id = Column(Integer, ForeignKey('pystock_broker.id'))
    broker = relationship("Broker", backref="accounts")


class Asset(Base):
    """
        An asset that derives value because of a contractual claim. Stocks, bonds, bank deposits, and the like are all examples of financial assets.
    """
    __tablename__ = 'pystock_asset'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False, unique=True)


#class StockAsset(Asset):
#    __tablename__ = 'pystock_stockasset'


class Tick(Base):
    """
        The minimum upward or downward movement in the price of a security. The term "tick" also refers to the change in the price of a security from trade to trade. Since 2001, with the advent of decimalization, the minimum tick size for stocks trading above $1 is 1 cent.
    """
    __tablename__ = 'pystock_tick'

    id = Column(Integer, primary_key=True)


class Quote(Base):
    __tablename__ = 'pystock_quote'
    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, onupdate=datetime.datetime.now)
    tick_date = Column(Date)
    px_open = Column(DECIMAL)
    px_close = Column(DECIMAL)
    px_high = Column(DECIMAL)
    px_low = Column(DECIMAL)
    volume = Column(Integer)
    asset_id = Column(Integer, ForeignKey('pystock_asset.id'))
    asset = relationship("Asset", backref="quotes")


class Action(object):
    SELL = 'sell'
    BUY = 'buy'
    SELL_SHORT = 'sell_short'
    BUY_TO_COVER = 'buy_to_cover'


class Type(object):
    pass


class Order(Base):
    """
        An investor's instructions to a broker or brokerage firm to purchase or sell a security.
        Orders are typically placed over the phone or online. Orders fall into different available
        types which allow investors to place restrictions on their orders affecting the price and
        time at which the order can be executed. These order instructions will affect the investor's
        profit or loss on the transaction and, in some cases, whether the order is executed at all.
    """
    OPEN = 'open'
    FILLED = 'filled'
    CANCELED = 'canceled'

    __tablename__ = 'pystock_order'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('pystock_account.id'))
    account = relationship("Account", backref="orders")
    asset_id = Column(Integer, ForeignKey('pystock_asset.id'))
    asset = relationship("Asset", backref="order")
    order_id = Column(String, unique=True)
    price = Column(DECIMAL)
    share = Column(Integer)
    executed_on = Column(DateTime, onupdate=datetime.datetime.now)
    filled_on = Column(DateTime, onupdate=datetime.datetime.now)
