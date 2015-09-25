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
    Security,
    Tick,
    Company,
    OpenOrderStage,
    OpenPositionStage,
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


class TestOrder(DatabaseTest):

    def test_is_order_met(self):
        now = datetime.datetime.now()
        broker = Broker(name='Broker1')
        account = Account(broker=broker)

        pesos = Currency(name='Pesos', code='ARG')
        account.deposit(Money(amount=10000, currency=pesos))
        exchange = Exchange(name='Merval', code='MERV', currency=pesos)
        stock=Stock(symbol='symbol', description='a stock', ISIN='US123456789', exchange=exchange)
        tick1=Tick(trade_date=now, price=13.20, amount=1000, volume=1000, security=stock)
        order1=BuyOrder(account=account, security=stock, price=13.25, share=10, is_market=True)
        order2=BuyOrder(account=account, security=stock, price=13.15, share=10)
        order3=SellOrder(account=account, security=stock, price=13.25, share=10)
        order4=SellOrder(account=account, security=stock, price=13.15, share=10, is_market=True)
        self.session.add(order1)
        self.session.add(order2)
        self.session.add(order3)
        self.session.add(order4)
        self.session.commit()

        self.assertTrue(order1.is_order_met(tick1))
        self.assertFalse(order2.is_order_met(tick1))
        self.assertFalse(order3.is_order_met(tick1))
        self.assertTrue(order4.is_order_met(tick1))


class TestStringOutputs(DatabaseTest):

    def test_account_ste(self):
        owner = Owner(name='Owner name')
        broker = Broker(name='Broker1')
        account = Account(owner=owner, broker=broker)

        self.assertEquals('Account for Owner name broker Broker1', str(account))

    def test_order_stage_str(self):
        order_stage = OpenOrderStage()

        self.session.add(order_stage)
        self.session.commit()

        self.assertEquals('pystock_stage_open_order {0}'.format(order_stage.executed_on), str(order_stage))

    def test_security_quote(self):
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        exchange = Exchange(name='Merval', code='MERV')
        security = Stock(symbol='PBR', description='Petrobras BR', ISIN='US71654V4086', exchange=exchange)
        quote = SecurityQuote(date=tomorrow, close_price=Decimal(100), open_price=10.1, high_price=14, low_price=10.1, volume=10000, security=security)
        self.session.add(quote)
        self.session.commit()

        self.assertEquals("<Quote('PBR', '{0}','10.1000000000', '14.0000000000', '10.1000000000', '100.0000000000', '10000.0000000000', 'None')>".format(quote.date), str(quote))

    def test_position_stage_str(self):
        order_stage = OpenPositionStage()

        self.session.add(order_stage)
        self.session.commit()

        self.assertEquals('pystock_open_position_stage {0}'.format(order_stage.executed_on), str(order_stage))

    def test_broker_str(self):
        broker = Broker(name='test')

        self.assertEquals('test', str(broker))

    def test_security_str(self):
        security = Security(symbol='YPF')

        self.assertEquals('YPF', str(security))

    def test_company_str(self):
        company = Company(name='Lalal S.A.')

        self.assertEquals('Company Lalal S.A.', str(company))

    def test_tick_str(self):
        import datetime
        now = datetime.datetime.now()
        security = Security(symbol='YPF')
        tick = Tick(security=security, trade_date=now, price=Decimal(10), volume=100)

        self.assertEquals("<Tick('YPF', '{0}', '10', '100')>".format(now), str(tick))

    def test_order_str(self):
        security = Security(symbol='YPF')
        order = BuyOrder(security=security, share=10, price=Decimal(10))

        self.assertEquals('pystock_buy_order Total 100', str(order))

    def test_exchange_str(self):
        exchange = Exchange(name='Merval', code='MERV')

        self.assertEquals('Exchange MERV Merval', str(exchange))


class TestPosition(DatabaseTest):

    def _buy_stock(self):
        pesos = Currency(name='Pesos', code='ARG')
        broker = Broker(name='Cheap')
        self.account = Account(broker=broker)
        self.account.deposit(Money(amount=Decimal(10000), currency=pesos))
        exchange = Exchange(name='Merval', currency=pesos)
        self.security = Stock(symbol='PBR', description='Petrobras BR', ISIN='US71654V4086', exchange=exchange)
        filled_stage = FillOrderStage(executed_on=datetime.datetime.now())
        price = Decimal(10)
        share = 10
        order = BuyOrder(account=self.account, security=self.security, stage=filled_stage, price=price, share=share)

        self.session.add(order)
        self.session.commit()
        return self.account

    def test_current_position_stage_is_open(self):
        account = self._buy_stock()
        position = account.positions[0]
        self.assertTrue(position.current_stage.is_open())

    def test_close_position_ok_path(self):
        self._buy_stock()

        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        quote = SecurityQuote(date=tomorrow, close_price=Decimal(100), open_price=10.1, high_price=14, low_price=10.1, volume=10000, security=self.security)
        self.session.add(quote)
        self.session.commit()

        filled_stage = FillOrderStage(executed_on=datetime.datetime.now())
        sell_order = SellOrder(account=self.account, security=self.security, stage=filled_stage, price=Decimal(100), share=10)

        self.session.add(sell_order)
        self.session.commit()

        self.account.positions[0].close(sell_order)

        self.assertFalse(self.account.positions[0].is_open())

    def test_close_position_less_than_bought_opens_a_new_position(self):
        self._buy_stock()

        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        quote = SecurityQuote(date=tomorrow, close_price=Decimal(100), open_price=10.1, high_price=14, low_price=10.1, volume=10000, security=self.security)
        self.session.add(quote)
        self.session.commit()

        filled_stage = FillOrderStage(executed_on=datetime.datetime.now())
        sell_order = SellOrder(account=self.account, security=self.security, stage=filled_stage, price=Decimal(100), share=5)

        self.session.add(sell_order)
        self.session.commit()

        self.account.positions[0].close(sell_order)

        self.assertEquals(len(self.account.positions), 2)
        self.assertFalse(self.account.positions[0].is_open())
        self.assertTrue(self.account.positions[1].is_open())

    def test_close_position_with_more_share_raises_execption(self):
        self._buy_stock()
        # buy more to allow to sell 15
        filled_stage = FillOrderStage(executed_on=datetime.datetime.now())
        buy_order = BuyOrder(account=self.account, security=self.security, stage=filled_stage, price=Decimal(20), share=10)
        self.session.add(buy_order)
        self.session.commit()

        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        quote = SecurityQuote(date=tomorrow, close_price=Decimal(100), open_price=10.1, high_price=14, low_price=10.1, volume=10000, security=self.security)
        self.session.add(quote)
        self.session.commit()

        filled_stage = FillOrderStage(executed_on=datetime.datetime.now())
        sell_order = SellOrder(account=self.account, security=self.security, stage=filled_stage, price=Decimal(100), share=15)

        self.session.add(sell_order)
        self.session.commit()

        with self.assertRaises(Exception):
            self.account.positions[0].close(sell_order)
