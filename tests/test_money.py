from pyStock.models import (
    get_or_create,
)
from pyStock.models.money import (
    Currency,
    Money,
)

from . import DatabaseTest


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
