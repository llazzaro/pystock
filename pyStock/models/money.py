# -*- coding: utf-8 -*-
from __future__ import division
import sys
from decimal import Decimal, ROUND_DOWN


PYTHON2 = sys.version_info[0] == 2


from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    ForeignKey,
)


from pyStock import (
    Base,
)


class Currency(Base):
    """
        A generally accepted form of money, including coins and paper notes,
        which is issued by a government and circulated within an economy.
        Used as a medium of exchange for goods and services, currency is the basis for trade.

        code uses ISO 4217 Currency Code
    """
    __tablename__ = 'pystock_currency'
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)

    def __eq__(self, other):
        return type(self) is type(other) and self.code == other.code

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.code


class Money(Base):

    __tablename__ = 'pystock_money'
    id = Column(Integer, primary_key=True)
    amount = Column(Numeric)
    account_id = Column(Integer, ForeignKey('pystock_account.id'))
    account = relationship("Account", backref="money")
    currency_id = Column(Integer, ForeignKey('pystock_currency.id'))
    currency = relationship("Currency", backref="money")

    def __repr__(self):
        return "{0} {1}".format(self.amount.to_integral_value(ROUND_DOWN),
                          self.currency)

    def __unicode__(self):
        from moneyed.localization import format_money
        return format_money(self)

    def __str__(self):
        from moneyed.localization import format_money
        return format_money(self)

    def __pos__(self):
        return self.__class__(
            amount=self.amount,
            currency=self.currency)

    def __neg__(self):
        return self.__class__(
            amount=-self.amount,
            currency=self.currency)

    def __add__(self, other):
        if other == 0:
            # This allows things like 'sum' to work on list of Money instances,
            # just like list of Decimal.
            return self
        if not isinstance(other, Money):
            raise TypeError('Cannot add or subtract a ' +
                            'Money and non-Money instance.')
        if self.currency == other.currency:
            return self.__class__(
                amount=self.amount + other.amount,
                currency=self.currency)

        raise TypeError('Cannot add or subtract two Money ' +
                        'instances with different currencies.')

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        if isinstance(other, Money):
            raise TypeError('Cannot multiply two Money instances.')
        else:
            return self.__class__(
                amount=(self.amount * Decimal(str(other))),
                currency=self.currency)

    def __truediv__(self, other):
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise TypeError('Cannot divide two different currencies.')
            return self.amount / other.amount
        else:
            return self.__class__(
                amount=self.amount / Decimal(str(other)),
                currency=self.currency)

    def __abs__(self):
        return self.__class__(
            amount=abs(self.amount),
            currency=self.currency)

    def __bool__(self):
        return bool(self.amount)

    if PYTHON2:
        __nonzero__ = __bool__

    def __rmod__(self, other):
        """
        Calculate percentage of an amount.  The left-hand side of the
        operator must be a numeric value.
        Example:
        >>> money = Money(200, 'USD')
        >>> 5 % money
        USD 10.00
        """
        if isinstance(other, Money):
            raise TypeError('Invalid __rmod__ operation')
        else:
            return self.__class__(
                amount=(Decimal(str(other)) * self.amount / 100),
                currency=self.currency)

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__

    # _______________________________________
    # Override comparison operators
    def __eq__(self, other):
        return (isinstance(other, Money)
                and (self.amount == other.amount)
                and (self.currency == other.currency))

    def __ne__(self, other):
        result = self.__eq__(other)
        return not result

    def __lt__(self, other):
        if not isinstance(other, Money):
            raise TypeError('Cannot compare Monet with other thing that is not Money.')
        if (self.currency == other.currency):
            return (self.amount < other.amount)
        else:
            raise TypeError('Cannot compare Money with different currencies.')

    def __gt__(self, other):
        if not isinstance(other, Money):
            raise TypeError('Cannot compare Monet with other thing that is not Money.')
        if (self.currency == other.currency):
            return (self.amount > other.amount)
        else:
            raise TypeError('Cannot compare Money with different currencies.')

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other
