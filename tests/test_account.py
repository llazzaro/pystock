import datetime
from decimal import Decimal
from pyStock.models import (
    Stock,
    Account,
    SecurityQuote,
    FillOrderStage,
    BuyOrder,
    SellOrder,
    Owner,
    Broker,
    Exchange,
)
from pyStock.models.money import (
    Money,
    Currency
)

from . import DatabaseTest


class TestAccount(DatabaseTest):

    def setUp(self):
        super(TestAccount, self).setUp()
        self.owner = Owner(name='lucky')
        self.pesos = Currency(name='Pesos', code='ARG')
        self.exchange = Exchange(name='Merval', currency=self.pesos)
        self.free_broker = Broker(name='Free Broker')
        self.stock_one = Stock(symbol='PBR', description='Petrobras BR', ISIN='US71654V4086', exchange=self.exchange)
        self.stock_two = Stock(symbol='YPF', description='YPF S.A', ISIN='US9842451000', exchange=self.exchange)
        self.account=Account(owner=self.owner, broker=self.free_broker)
        self.money = Money(amount=1000, currency=self.pesos)

    def test_cash_deposit(self):
        account=Account()
        one_thousands_pesos = Money(amount=1000, currency=self.pesos)
        account.deposit(one_thousands_pesos)
        self.assertEquals(1000, account.cash[self.pesos])

    def test_holdings_cost(self):
        share=10
        price=9.1

        self.account.deposit(self.money)
        filled_stage = FillOrderStage(executed_on=datetime.datetime.now())

        order = BuyOrder(account=self.account, security=self.stock_one, stage=filled_stage, price=price, share=share)
        self.session.add(order)
        self.session.commit()

        holding_cost=self.account.holdings_cost
        symbol = self.stock_one.symbol
        self.assertAlmostEquals(Decimal(share * price), holding_cost[symbol])

    def test_holding_value(self):
        share=10
        price=9.1
        cur_price=10.1
        self.account.deposit(self.money)
        filled_stage = FillOrderStage(executed_on=datetime.datetime.now())

        order = BuyOrder(account=self.account, security=self.stock_one, stage=filled_stage, price=price, share=share)
        self.session.add(order)
        self.session.commit()

        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        quote = SecurityQuote(date=tomorrow, close_price=cur_price, open_price=10.1, high_price=14, low_price=10.1, volume=10000, security=self.stock_one)
        self.session.add(quote)
        self.session.commit()
        # account.setLastTickDict({'stock1': Quote(0, 0, 0, 0, curPrice, 0, 0)})

        holding_value=self.account.holdings_value
        currency = self.stock_one.exchange.currency
        self.assertAlmostEqual(Decimal(share * cur_price), holding_value[currency])

    def test_total_value(self):
        account=Account(owner=self.owner, broker=self.free_broker)
        money = Money(amount=1000, currency=self.pesos)
        account.deposit(money)

        share=10
        price = 9.1
        filled_stage = FillOrderStage(executed_on=datetime.datetime.now())
        order = BuyOrder(account=account, security=self.stock_one, stage=filled_stage, price=price, share=share)
        self.session.add(order)
        self.session.commit()
        # lets check that it was withdraw form the account
        # no fee is charged with the free broker
        self.assertEquals(account.cash[self.pesos], 1000 - 9.1 * share)

        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        quote = SecurityQuote(date=tomorrow, close_price=12, open_price=10.1, high_price=14, low_price=10.1, volume=10000, security=self.stock_one)
        self.session.add(quote)
        self.session.commit()

        total = account.total
        self.assertAlmostEquals(909 + 10 * 12, total[self.pesos])

    def test_buy_validate_price_too_high(self):
        self.account.deposit(self.money)

        # can't buy because price too high
        with self.assertRaises(Exception):
            order = BuyOrder(account=self.account, security=self.stock_one, price=10000, share=100000)
            self.session.add(order)
            self.session.commit()

    def test_buy_validate_comission_fee_plus_cost_not_enough_money(self):
        self.account.deposit(self.money)
        self.free_broker.commission = lambda target: 10000
        # can't buy because of commission fee
        with self.assertRaises(Exception):
            order = BuyOrder(account=self.account, security=self.stock_one, price=100, share=10)
            self.session.add(order)
            self.session.commit()

    def test_buy_validate_enough_money_ok_path(self):
        self.account.deposit(self.money)
        # buy it
        order = BuyOrder(account=self.account, security=self.stock_one, price=100, share=9)
        self.session.add(order)
        self.session.commit()

    def _buy_stock(self, stock):
        self.account.deposit(self.money)
        # buy it
        order = BuyOrder(account=self.account, security=stock, price=100, share=9)
        self.session.add(order)
        self.session.commit()

    def test_sell_validate_selling_something_not_owned(self):
        # can't sell because don't have the stock
        with self.assertRaises(Exception):
            order = SellOrder(account=self.account, security=self.stock_two, price=100, share=9)
            self.session.add(order)
            self.session.commit()

    def test_sell_validate_selling_something_owned_but_quantity_invalid(self):
        # can't sell because don't have the enough share
        with self.assertRaises(Exception):
            order = SellOrder(account=self.account, security=self.stock_one, price=100, share=9000)
            self.session.add(order)
            self.session.commit()

    def test_sell_something_owned_ok_path(self):
        self._buy_stock(self.stock_one)

        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        quote = SecurityQuote(date=tomorrow, close_price=12, open_price=10.1, high_price=14, low_price=10.1, volume=10000)
        self.session.add(quote)
        self.session.commit()
        # sell it
        order = SellOrder(account=self.account, security=self.stock_one, price=100, share=9)

        self.session.add(order)
        self.session.commit()
