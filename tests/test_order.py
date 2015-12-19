import datetime
from pystock.models import (
    Stock,
    SecurityQuote,
    BuyOrder,
    SellOrder,
    Exchange,
    FillOrderStage,
    CancelOrderStage,
)
from pystock.models.account import (
    Owner,
    Account,
    Broker,
)
from pystock.models.money import (
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

    def _buy_stock(self, stock):
        self.account.deposit(self.money)
        # buy it
        order = BuyOrder(account=self.account, security=stock, price=100, share=9)
        self.session.add(order)
        self.session.commit()
        return order

    def test_open_order_stage_is_open(self):
        order = self._buy_stock(self.stock_one)
        self.assertTrue(order.current_stage.is_open)

    def test_update_order_stage_to_filled(self):
        order = self._buy_stock(self.stock_one)
        order.update_stage(FillOrderStage())

        self.assertTrue(order.current_stage.is_filled)

    def test_update_order_stage_to_cancel(self):
        order = self._buy_stock(self.stock_one)
        order.cancel()

        self.assertTrue(order.current_stage.is_cancel)

    def test_sell_validate_selling_something_not_owned(self):
        # can't sell because don't have the stock
        with self.assertRaises(Exception):
            order = SellOrder(account=self.account, security=self.stock_two, price=100, share=9)
            self.session.add(order)
            self.session.commit()

    def test_sell_validate_selling_something_owned_but_quantity_invalid(self):
        self._buy_stock(self.stock_one)
        # can't sell because don't have the enough share
        with self.assertRaises(Exception):
            order = SellOrder(account=self.account, security=self.stock_one, price=100, share=9000)
            self.session.add(order)
            self.session.commit()

    def test_sell_validate_selling_more_than_owned(self):
        self._buy_stock(self.stock_one)
        # can't sell because don't have the stock
        with self.assertRaises(Exception):
            order = SellOrder(account=self.account, security=self.stock_two, price=200, share=9)
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
