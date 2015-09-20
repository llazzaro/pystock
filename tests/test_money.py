from __future__ import division
from decimal import Decimal

from pyStock.models import (
    get_or_create,
)
from pyStock.models.money import (
    Currency,
    Money,
)

from . import DatabaseTest


class TestCurrency(DatabaseTest):

    def test_repr(self):
        currency_arg, created = get_or_create(self.session, Currency, name='Peso', code='ARG')

        self.assertEquals(currency_arg.__repr__(), currency_arg.code)

    def test_not_equals(self):
        currency_arg, created = get_or_create(self.session, Currency, name='Peso', code='ARG')
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')

        self.assertTrue(currency_arg != currency_usd)


class TestMoney(DatabaseTest):

    def test_money_compare_currencies(self):
        currency_arg, created = get_or_create(self.session, Currency, name='Peso', code='ARG')
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')

        ar_10, created = get_or_create(self.session, Money, amount=10, currency=currency_arg)
        usd_10, created = get_or_create(self.session, Money, amount=10, currency=currency_usd)

    def test_money_gt(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')
        usd_10, created = get_or_create(self.session, Money, amount=10, currency=currency_usd)
        usd_11, created = get_or_create(self.session, Money, amount=11, currency=currency_usd)

        self.assertTrue(usd_11 > usd_10)

    def test_money_lt(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')

        usd_10, created = get_or_create(self.session, Money, amount=10, currency=currency_usd)
        usd_11, created = get_or_create(self.session, Money, amount=11, currency=currency_usd)

        self.assertFalse(usd_11 < usd_10)

    def test_money_equals(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')

        usd_10, created = get_or_create(self.session, Money, amount=10, currency=currency_usd)
        other_usd_10, created = get_or_create(self.session, Money, amount=10, currency=currency_usd)
        self.assertTrue(other_usd_10 == usd_10)

    def test_repr(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')

        usd_10, created = get_or_create(self.session, Money, amount=Decimal(10), currency=currency_usd)
        self.assertEquals(usd_10.__repr__(), '10 USD')

    def test_str(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')

        usd_10, created = get_or_create(self.session, Money, amount=Decimal(10), currency=currency_usd)

        self.assertEquals("US$10.00", str(usd_10))

    def test_unicode(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')

        usd_10, created = get_or_create(self.session, Money, amount=Decimal(10), currency=currency_usd)

        self.assertEquals(u'US$10.00', unicode(usd_10))

    def test_add_money(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')

        usd_10, created = get_or_create(self.session, Money, amount=Decimal(10), currency=currency_usd)
        usd_20, created = get_or_create(self.session, Money, amount=Decimal(20), currency=currency_usd)

        usd_30 = usd_10 + usd_20

        self.assertEquals(usd_30.amount, 30)
        self.assertEquals(usd_30.currency.code, 'USD')

    def test_sub(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')

        usd_10, created = get_or_create(self.session, Money, amount=Decimal(10), currency=currency_usd)
        usd_20, created = get_or_create(self.session, Money, amount=Decimal(20), currency=currency_usd)

        usd_sub = usd_20 - usd_10

        self.assertEquals(usd_sub.amount, 10)
        self.assertEquals(usd_sub.currency.code, 'USD')

    def test_less_or_equal(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')

        usd_10, created = get_or_create(self.session, Money, amount=Decimal(10), currency=currency_usd)
        other_usd_10, created = get_or_create(self.session, Money, amount=Decimal(10), currency=currency_usd)
        usd_20, created = get_or_create(self.session, Money, amount=Decimal(20), currency=currency_usd)

        self.assertTrue(usd_10 <= usd_20)
        self.assertTrue(usd_10 <= other_usd_10)

    def test_great_or_equal(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')

        usd_10, created = get_or_create(self.session, Money, amount=Decimal(10), currency=currency_usd)
        other_usd_10, created = get_or_create(self.session, Money, amount=Decimal(10), currency=currency_usd)
        usd_20, created = get_or_create(self.session, Money, amount=Decimal(20), currency=currency_usd)

        self.assertTrue(usd_20 >= usd_10)
        self.assertTrue(usd_20 >= other_usd_10)

    def test_not_equal_by_amount(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')

        usd_10, created = get_or_create(self.session, Money, amount=Decimal(10), currency=currency_usd)
        usd_20, created = get_or_create(self.session, Money, amount=Decimal(20), currency=currency_usd)

        self.assertTrue(usd_10 != usd_20)

    def test_not_equal_by_currency(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')
        currency_ar, created = get_or_create(self.session, Currency, name='Peso', code='ARG')

        usd_10, created = get_or_create(self.session, Money, amount=Decimal(10), currency=currency_usd)
        ar_10, created = get_or_create(self.session, Money, amount=Decimal(10), currency=currency_ar)

        self.assertTrue(usd_10 != ar_10)

    def test_rmod(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')
        usd_200, created = get_or_create(self.session, Money, amount=Decimal(200), currency=currency_usd)

        self.assertEquals(5 % usd_200, Money(amount=Decimal(10), currency=currency_usd))

    def test_abs(self):

        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')
        usd_minus_200, created = get_or_create(self.session, Money, amount=Decimal(-200), currency=currency_usd)

        self.assertEquals(Money(amount=Decimal(200), currency=currency_usd), abs(usd_minus_200))

    def test_mul(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')
        usd_10, created = get_or_create(self.session, Money, amount=Decimal(10), currency=currency_usd)

        self.assertEquals(usd_10 * 20, Money(amount=Decimal(10 * 20), currency=currency_usd))

    def test_mul_bad(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')
        usd_10, created = get_or_create(self.session, Money, amount=Decimal(10), currency=currency_usd)

        with self.assertRaises(Exception):
            usd_10 * usd_10

    def test_sum(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')
        money = sum([Money(amount=1, currency=currency_usd), Money(amount=2, currency=currency_usd)])
        self.assertEquals(money, Money(amount=3, currency=currency_usd))

    def test_add_non_money(self):
        with self.assertRaises(Exception):
            Money(1000) + 123

    def test_div(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')
        x = Money(amount=50, currency=currency_usd)
        y = Money(amount=2, currency=currency_usd)
        self.assertEquals(x / y, Decimal(25))

    def test_div_by_non_Money(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')
        x = Money(amount=50, currency=currency_usd)
        y = 2
        self.assertEquals(x / y, Money(amount=25, currency=currency_usd))

    def test_rmod_bad(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')
        x = Money(amount=2, currency=currency_usd)
        with self.assertRaises(Exception):
            self.assertEquals(x, 1)

    def test_lt(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')
        x = Money(amount=1, currency=currency_usd)
        y = Money(amount=2, currency=currency_usd)
        self.assertTrue(x < y)

    def test_lgt(self):
        currency_usd, created = get_or_create(self.session, Currency, name='Dollar', code='USD')
        x = Money(amount=2, currency=currency_usd)
        y = Money(amount=1, currency=currency_usd)
        self.assertTrue(x > y)
