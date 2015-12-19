# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import event
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm import object_session

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    DECIMAL,
    Boolean,
)

from pystock import Base
from pystock.models.events import (
    validate_buy_order,
    validate_sell_order,
    order_with_open_stage,
)


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in list(kwargs.items()) if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


class Asset(Base):
    """
        An asset is an economic resource.
        Anything tangible or intangible that can be owned or controlled
        to produce value and that is held to have positive economic value is considered an asset.

    """
    __tablename__ = 'pystock_asset'

    id = Column(Integer, primary_key=True)
    exchange = relationship('Exchange', backref='securities')
    exchange_id = Column(Integer, ForeignKey('pystock_exchange.id'))
    issuer_name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    asset_type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_asset',
        'polymorphic_on': asset_type
    }


class Security(Asset):
    """
        A security is a financial instrument that represents an
        ownership position in a publicly-traded corporation (stock),
        a creditor relationship with governmental body or a
        corporation (bond), or rights to ownership as represented by an option.

        ISIN:  International Securities Identification Number (ISIN)
        uniquely identifies a security. Its structure is defined in ISO 6166.
    """
    __tablename__ = 'pystock_security'

    id = Column(Integer, ForeignKey('pystock_asset.id'), primary_key=True)
    symbol = Column(String, nullable=False, unique=True)
    ISIN = Column(String(12), nullable=False, unique=True)
    CFI = Column(String(6), nullable=True, unique=True)

    def __str__(self):
        return self.symbol

    @hybrid_property
    def currency(self):
        return self.exchange.currency


class Stock(Security):
    """
        A stock or any other security representing an ownership interest.
        An equity investment generally refers to the buying and holding of
        shares of stock on a stock market by individuals and firms in
        anticipation of income from dividends and capital gains, as the value of the stock rises.

    """
    __tablename__ = 'pystock_stock'

    id = Column(Integer, ForeignKey('pystock_security.id'), primary_key=True)
    company = relationship('Company', backref='stock')
    company_id = Column(Integer, ForeignKey('pystock_company.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_stock',
    }


class Bond(Security):
    __tablename__ = 'pystock_bond'

    id = Column(Integer, ForeignKey('pystock_security.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_bond',
    }


class Tick(Base):
    """
        The minimum upward or downward movement in the price of a security.
        The term "tick" also refers to the change in the price of a security from trade to trade.
        Since 2001, with the advent of decimalization, the minimum tick size for stocks trading above $1 is 1 cent.
    """

    __tablename__ = 'pystock_tick'

    id = Column(Integer, primary_key=True)

    created_on = Column(DateTime, onupdate=datetime.datetime.now)
    broker_buyer_id = Column(Integer, ForeignKey('pystock_broker.id'))
    broker_buyer = relationship('Broker', backref='buyer_trades', foreign_keys=[broker_buyer_id])
    broker_seller_id = Column(Integer, ForeignKey('pystock_broker.id'))
    broker_seller = relationship('Broker', backref='seller_trades', foreign_keys=[broker_seller_id])
    price = Column(DECIMAL)
    amount = Column(DECIMAL)
    volume = Column(Integer)
    nominal_amount = Column(Integer)
    trade_date = Column(DateTime)
    security_id = Column(Integer, ForeignKey('pystock_security.id'))
    security = relationship('Security', backref='trades')
    fraction = Column(Boolean)
    expiration = Column(String)
    register_number = Column(String, unique=True)

    def __repr__(self):
        return "<Tick('{0}', '{1}', '{2}', '{3}')>".format(self.security.symbol, self.trade_date, self.price, self.volume)


class Action(object):
    SELL = 'sell'
    BUY = 'buy'
    SELL_SHORT = 'sell_short'
    BUY_TO_COVER = 'buy_to_cover'
    STOP = 'stop'


class Order(Base):
    """
        An investor's instructions to a broker or brokerage firm to purchase or sell a security.
        Orders are typically placed over the phone or online. Orders fall into different available
        types which allow investors to place restrictions on their orders affecting the price and
        time at which the order can be executed. These order instructions will affect the investor's
        profit or loss on the transaction and, in some cases, whether the order is executed at all.
    """

    __tablename__ = 'pystock_order'
    id = Column(Integer, primary_key=True)

    # order type is used by sqlalchemy to track class inheritance
    order_type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_order',
        'polymorphic_on': order_type
    }

    account_id = Column(Integer, ForeignKey('pystock_account.id'))
    account = relationship('Account', backref='orders')
    security_id = Column(Integer, ForeignKey('pystock_security.id'))
    security = relationship('Security', backref='order')
    order_id = Column(String, unique=True)
    price = Column(DECIMAL)
    share = Column(Integer)
    stage = relationship('OrderStage', backref='orders')
    stage_id = Column(Integer, ForeignKey('pystock_stage_order.id'))
    action = Column(String, unique=True)
    is_market = Column(Boolean)
    is_limit = Column(Boolean)
    is_stop = Column(Boolean)

    def __str__(self):
        return '{0} Total {1}'.format(self.order_type, self.share * self.price)

    @property
    def effective_date(self):
        return self.stage.executed_on

    def calculate_split(self, res, func):
        splits = filter(lambda split: split.split_date >= self.stage.executed_on, self.security.splits)
        for split in splits:
            if self.stage.executed_on >= split.split_date:
                continue
            res = func(res, split.ratio)
        return res

    def is_order_met(self, tick):
        raise NotImplementedError('Abstrat method called')

    @hybrid_property
    def current_stage(self):
        current_stage = self.stage
        while self.stage and current_stage.next_stage is not None:
            current_stage = current_stage.next_stage

        return current_stage

    def update_stage(self, stage):
        session = object_session(self)
        if self.current_stage is not None:
            self.current_stage.next_stage = stage
        else:
            self.stage = stage
        session.add(stage)

    def cancel(self):
        if self.current_stage.is_open:
            session = object_session(self)
            cancel_stage = CancelOrderStage()
            self.update_stage(cancel_stage)
            session.add(cancel_stage)


class SellOrder(Order):
    __tablename__ = 'pystock_sell_order'
    id = Column(Integer, ForeignKey('pystock_order.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_sell_order',
    }

    @hybrid_property
    def current_price(self):
        func = lambda price, ratio: price / ratio
        return self.calculate_split(self._price, func)

    @hybrid_property
    def current_shares(self):
        func = lambda price, ratio: price * ratio
        return self.calculate_split(self._shares, func)

    def is_order_met(self, tick):
        if self.is_market:
            return True
        elif Action.STOP == self.action and float(tick.low_price) <= float(self.price):
            return True
        return False


class BuyOrder(Order):
    __tablename__ = 'pystock_buy_order'
    id = Column(Integer, ForeignKey('pystock_order.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_buy_order',
    }

    @hybrid_property
    def current_price(self):
        func = lambda price, ratio: price / ratio
        return self.calculate_split(self._price, func)

    @hybrid_property
    def current_shares(self):
        func = lambda price, ratio: price * ratio
        return self.calculate_split(self._shares, func)

    def is_order_met(self, tick):
        if self.is_market:
            return True
        elif self.is_limit and float(tick.low) <= float(self.price):
            return True
        return False


class SellShortOrder(Order):

    __tablename__ = 'pystock_sell_short_order'
    id = Column(Integer, ForeignKey('pystock_order.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_sell_short_order',
    }

    def is_order_met(self, tick):
        if self.is_market:
            return True
        elif self.is_limit and float(tick.high) >= float(self.price):
            return True
        return False


class BuyToCoverOrder(Order):

    __tablename__ = 'pystock_buy_to_cover_order'
    id = Column(Integer, ForeignKey('pystock_order.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_buy_to_cover_order',
    }

    def is_order_met(self, tick):
        if self.is_market:
            return True
        elif Action.STOP == self.action and float(tick.high) >= float(self.price):
            return True
        return False


class OrderStage(Base):
    __tablename__ = 'pystock_stage_order'
    id = Column(Integer, primary_key=True)

    stage_type = Column(String(50))
    executed_on = Column(DateTime, onupdate=datetime.datetime.now)
    next_stage = relationship('OrderStage', remote_side=[id])
    next_stage_id = Column(Integer, ForeignKey('pystock_stage_order.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_order_stage',
        'polymorphic_on': stage_type
    }

    def __str__(self):
        return '{0} {1}'.format(self.stage_type, self.executed_on)

    @hybrid_property
    def is_open(self):
        return False

    @hybrid_property
    def is_cancel(self):
        return False

    @hybrid_property
    def is_filled(self):
        return False


class OpenOrderStage(OrderStage):
    """
        An order to buy or sell a security that remains in effect until
        it is either canceled by the customer, until it is executed or until it expires.
    """
    __tablename__ = 'pystock_open_stage_order'
    id = Column(Integer, ForeignKey('pystock_stage_order.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_stage_open_order',
    }

    @hybrid_property
    def is_open(self):
        return True


class CancelOrderStage(OrderStage):
    """

    """
    __tablename__ = 'pystock_cancel_stage_order'
    id = Column(Integer, ForeignKey('pystock_stage_order.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_stage_cancel_order',
    }

    @hybrid_property
    def is_cancel(self):
        return True


class FillOrderStage(OrderStage):
    __tablename__ = 'pystock_fill_stage_order'
    id = Column(Integer, ForeignKey('pystock_stage_order.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_stage_fill_order',
    }

    @hybrid_property
    def is_filled(self):
        return True


class Split(Base):
    """
        A corporate action in which a company divides its existing shares into multiple shares.
        Although the number of shares outstanding increases by a specific multiple, the total
        dollar value of the shares remains the same compared to pre-split amounts, because the
        split did not add any real value.
    """
    __tablename__ = 'pystock_split'
    id = Column(Integer, primary_key=True)
    announce_date = Column(DateTime)
    split_date = Column(DateTime)
    ratio = Column(Integer)
    security_id = Column(Integer, ForeignKey('pystock_security.id'))
    security = relationship('Security', backref='splits')


class Dividend(Base):
    """
        A distribution of a portion of a company's earnings, decided by the board of directors,
        to a class of its shareholders. The dividend is most often quoted in terms of the dollar
        amount each share receives (dividends per share). It can also be quoted in terms of a
        percent of the current market price, referred to as dividend yield.
    """

    __tablename__ = 'pystock_dividend'
    id = Column(Integer, primary_key=True)
    announce_date = Column(DateTime)
    exdividend_date = Column(DateTime)
    record_date = Column(DateTime)
    payment_date = Column(DateTime)
    amount = Column(DECIMAL)
    security_id = Column(Integer, ForeignKey('pystock_security.id'))
    security = relationship('Security', backref='dividends')


class ADR(Base):
    """
    """
    __tablename__ = 'pystock_adr'
    id = Column(Integer, primary_key=True)
    ratio = Column(Integer)
    adr_security_id = Column(Integer, ForeignKey('pystock_security.id'))
    adr_security = relationship('Stock', backref='ADROrigin', foreign_keys='ADR.adr_security_id')
    security_id = Column(Integer, ForeignKey('pystock_security.id'))
    security = relationship('Stock', backref='ADRDestination', foreign_keys='ADR.security_id')
    exchange_id = Column(Integer, ForeignKey('pystock_exchange.id'))
    exchange = relationship('Exchange', backref='ADR')


class MonetarySource(Base):
    __tablename__ = 'pystock_monetary_source'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class FXRates(Base):
    """
        The price of a nation's currency in terms of another currency.
        An exchange rate thus has two components, the domestic currency
        and a foreign currency, and can be quoted either directly or
        indirectly. In a direct quotation, the price of a unit of foreign
        currency is expressed in terms of the domestic currency.
        In an indirect quotation, the price of a unit of domestic currency
        is expressed in terms of the foreign currency. An exchange rate
        that does not have the domestic currency as one of the two
        currency components is known as a cross currency, or cross rate.
    """
    __tablename__ = 'pystock_fxrates'
    __table_args__ = (
            UniqueConstraint('date', 'monetary_source_id', name='unique_monetary_date'),
    )

    id = Column(Integer, primary_key=True)
    monetary_source = relationship('MonetarySource', backref='fxrates')
    monetary_source_id = Column(Integer, ForeignKey('pystock_monetary_source.id'))
    from_currency_id = Column(Integer, ForeignKey('pystock_currency.id'))
    from_currency = relationship('Currency', backref='from_fxrates', foreign_keys=[from_currency_id])
    to_curreny_id = Column(Integer, ForeignKey('pystock_currency.id'))
    to_currency = relationship('Currency', backref='to_fxrates', foreign_keys=[to_curreny_id])
    buy_rate = Column(DECIMAL)
    sell_rate = Column(DECIMAL)
    created_on = Column(DateTime, onupdate=datetime.datetime.now)
    date = Column(DateTime)


class Company(Base):
    __tablename__ = 'pystock_company'
    id = Column(Integer, primary_key=True)

    name = Column(String)

    def __str__(self):
        return 'Company {0}'.format(self.name)


class Book(Base):
    """
         record of all the positions that a trader is holding.
         This record shows the total amount of long and short position
         that the trader has undertaken.
    """
    __tablename__ = 'pystock_book'
    id = Column(Integer, primary_key=True)

    name = Column(String)
    owner = relationship('Owner', backref='trades')
    owner_id = Column(Integer, ForeignKey('pystock_owner.id'))


class Exchange(Base):
    """
        A marketplace in which securities, commodities, derivatives and other financial instruments are traded.
        The core function of an exchange - such as a stock exchange - is to ensure fair and orderly trading,
        as well as efficient dissemination of price information for any securities trading on that exchange.
        Exchanges give companies, governments and other groups a platform to sell securities to the investing public.
    """
    __tablename__ = 'pystock_exchange'
    id = Column(Integer, primary_key=True)

    code = Column(String)
    name = Column(String)
    currency = relationship('Currency', backref='exchanges')
    currency_id = Column(Integer, ForeignKey('pystock_currency.id'))

    def __str__(self):
        return 'Exchange {0} {1}'.format(self.code, self.name)


class Liability(Base):
    """
        Recorded on the balance sheet (right side), liabilities include loans,
        accounts payable, mortgages, deferred revenues and accrued expenses.
    """
    __tablename__ = 'pystock_liability'
    id = Column(Integer, primary_key=True)


class Quote(Base):
    """
        This denotes the prevailing buy and sell prices for a particular financial instrument.
        Quotes are displayed as: sell price -- buy price.
        For example, if 125.7 -- 125.9 is the quote: 125.7 is the sell price and 125.9 is the buy price.
    """

    __tablename__ = 'pystock_quote'
    id = Column(Integer, primary_key=True)

    date = Column(DateTime)
    close_price = Column(DECIMAL)
    high_price = Column(DECIMAL)
    low_price = Column(DECIMAL)
    open_price = Column(DECIMAL)
    unadj = Column(DECIMAL)
    volume = Column(DECIMAL)

    def __repr__(self):
        raise NotImplementedError


class ExchangeQuote(Quote):
    """
    """
    __tablename__ = 'pystock_exchange_quote'
    id = Column(Integer, ForeignKey('pystock_quote.id'), primary_key=True)
    exchange_id = Column(Integer, ForeignKey('pystock_exchange.id'))
    exchange = relationship('Exchange', backref='quotes')

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_exchange_quote',
    }


class SecurityQuote(Quote):
    """
    """
    __tablename__ = 'pystock_security_quote'

    id = Column(Integer, ForeignKey('pystock_quote.id'), primary_key=True)
    security_id = Column(Integer, ForeignKey('pystock_security.id'))
    security = relationship('Security', backref='quotes', order_by='SecurityQuote.date')

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_security_quote',
    }

    def __repr__(self):
        return "<Quote('{0}', '{1}','{2}', '{3}', '{4}', '{5}', '{6}', '{7}')>" .format(self.security.symbol, self.date, self.open_price, self.high_price, self.low_price, self.close_price, self.volume, self.unadj)


class PositionStage(Base):
    """
    """
    __tablename__ = 'pystock_position_stage'

    id = Column(Integer, primary_key=True)

    stage_type = Column(String(50))
    executed_on = Column(DateTime, onupdate=datetime.datetime.now)
    next_stage = relationship('PositionStage', remote_side=[id])
    next_stage_id = Column(Integer, ForeignKey('pystock_position_stage.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_position_stage',
        'polymorphic_on': stage_type
    }

    def __str__(self):
        return '{0} {1}'.format(self.stage_type, self.executed_on)


class OpenPositionStage(PositionStage):
    """
    """
    __tablename__ = 'pystock_open_position_stage'
    id = Column(Integer, ForeignKey('pystock_position_stage.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_open_position_stage',
    }

    def is_open(self):
        return True


class ClosePositionStage(PositionStage):
    """
    """
    __tablename__ = 'pystock_close_position_stage'
    id = Column(Integer, ForeignKey('pystock_position_stage.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'pystock_close_position_stage',
    }

    def is_open(self):
        return False


class Position(Base):
    """
        Close Position: Executing a security transaction that is the exact opposite of an open position,
        thereby nullifying it and eliminating the initial exposure.
        Closing a long position in a security would entail selling it,
        while closing a short position in a security would involve buying it back.
    """
    __tablename__ = 'pystock_position'

    id = Column(Integer, primary_key=True)
    share = Column(Integer, nullable=False)
    buy_order = relationship('BuyOrder', backref='tracking')
    buy_order_id = Column(Integer, ForeignKey('pystock_buy_order.id'))
    sell_order = relationship('SellOrder', backref='tracking')
    sell_order_id = Column(Integer, ForeignKey('pystock_sell_order.id'))
    stage = relationship('PositionStage', backref='positions')
    first_id = Column(Integer, ForeignKey('pystock_position_stage.id'))
    account_id = Column(Integer, ForeignKey('pystock_account.id'))
    account = relationship('Account', backref='positions')

    @hybrid_property
    def is_open(self):
        return self.current_stage.is_open

    @hybrid_property
    def current_stage(self):
        current_stage = self.stage
        while current_stage.next_stage is not None:
            current_stage = current_stage.next_stage

        return current_stage

    def close(self, sell_order, commit=True):
        session = object_session(sell_order)
        self.sell_order = sell_order
        if sell_order.share > self.share:
            raise Exception('Cant close with more share')
        close_stage = ClosePositionStage()
        self.current_stage.next_stage = close_stage
        session.add(close_stage)
        if sell_order.share != self.share:
            # we open a new position with the remaining
            # the old one is closed with the sell_order share
            position = self.__class__(stage=OpenPositionStage(), share=self.share - sell_order.share, buy_order=self.buy_order, account=self.account)
            session.add(position)
        if commit:
            session.commit()

event.listen(BuyOrder, 'before_insert', validate_buy_order)
event.listen(SellOrder, 'before_insert', validate_sell_order)
event.listen(BuyOrder, 'after_insert', order_with_open_stage)
event.listen(SellOrder, 'after_insert', order_with_open_stage)

from pystock.models.account import Account
