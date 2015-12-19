from collections import Counter

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import object_session


from pystock import Base
from pystock.models import SecurityQuote


class Owner(Base):
    """
        Represent how is buying. usually this class is associated with another owner model in your app
    """
    __tablename__ = 'pystock_owner'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Broker(Base):
    """
        An agency broker is a broker that acts as a middle man to the stock exchange, and places trades on behalf of clients.
    """
    __tablename__ = 'pystock_broker'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    # usually phone and caegory are fks, we
    # save this for informational purposes
    # to aovid complex model on no so relevant info.
    # we only want to display this
    phone = Column(String)
    category = Column(String)
    web = Column(String)
    email = Column(String)
    identification_code = Column(String, unique=True)

    def __str__(self):
        return self.name or 'No Name'

    def commission(self, target):
        return 0


class Account(Base):
    """

    """
    __tablename__ = 'pystock_account'

    id = Column(Integer, primary_key=True)
    broker_id = Column(Integer, ForeignKey('pystock_broker.id'))
    broker = relationship('Broker', backref='accounts')
    owner = relationship('Owner', backref='accounts')
    owner_id = Column(Integer, ForeignKey('pystock_owner.id'))

    def __str__(self):
        return 'Account for {0} broker {1}'.format(self.owner.name, self.broker.name)

    @hybrid_property
    def cash(self):
        res = Counter()
        for money in self.money:
            res[money.currency] += money.amount

        return res

    @hybrid_property
    def holdings(self):
        res = Counter()
        for position in self.positions:
            if position.is_open:
                symbol = position.buy_order.security.symbol
                res[symbol] += position.share

        return res

    @hybrid_property
    def holdings_value(self):
        """
            all open positions with current market price
        """
        res = Counter()
        for position in self.positions:
            if position.is_open:
                latest_quote = object_session(position).query(SecurityQuote).order_by('date desc').limit(1).first()
                currency = position.buy_order.security.exchange.currency
                res[currency] += latest_quote.close_price * position.buy_order.share

        return res

    @hybrid_property
    def holdings_cost(self):
        """
            return how much money was used for current holdings
        """
        res = Counter()
        for position in self.positions:
            if position.is_open:
                symbol = position.buy_order.security.symbol
                res[symbol] += position.buy_order.price * position.buy_order.share

        return res

    def execute(self, order, tick):
        pass

    def deposit(self, money):
        money.account = self

    @hybrid_property
    def total(self):
        """
            total with holding current value
        """
        return self.cash + self.holdings_value
