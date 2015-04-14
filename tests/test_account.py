'''
Created on Jan 08, 2012

@author: ppa
'''
import unittest
import datetime
from pyStock.models import (
    Account,
    Quote,
    FillOrderStage,
    BuyOrder,
    SellOrder
)


class testAccount(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetCash(self):
        account=Account()
        account.deposit(1000)
        self.assertEquals(1000, account.cash)

    def testGetHoldingCost(self):
        share=10
        price=9.1
        account=Account(1000, 1)
        account._Account__holdings={'stock1': (share, price)}
        print(account.holdings)

        holdingCost=account.getHoldingCost()
        print(holdingCost)

        self.assertAlmostEquals(share * price, holdingCost)

    def testGetHoldingValue(self):
        share=10
        price=9.1
        curPrice=10.1
        account=Account(1000, 1)
        account._Account__holdings={'stock1': (share, price)}
        account.setLastTickDict({'stock1': Quote(0, 0, 0, 0, curPrice, 0, 0)})

        holdingValue=account.getHoldingValue()
        print(holdingValue)
        self.assertAlmostEqual(share * curPrice, holdingValue)

    def testTotalValue(self):
        share=10
        price=9.1
        account=Account(owner=self.owner)
        account.deposit(1000)
        filled_stage = FillOrderStage(executed_on=datetime.now())
        BuyOrder(account=account, security=self.stock_one, stage=filled_stage, price=price, shares=share)

        tomorrow = datetime.now() + datetime.timedelta(days=1)
        Quote(date=tomorrow, close_price=12, open_price=10.1, high_price=14, low_price=10.1, volume=10000)

        total = account.total
        self.assertAlmostEquals(909 + 10 * 12, total)

    def testValidate(self):
        account=Account()
        account.deposit(1000)

        # can't buy because price too high
        order1=BuyOrder(accountId=account, security=self.security, price=10000, share=100000)
        self.assertEquals(False, account.validate(order1))

        # can't buy because of commission fee
        order1=BuyOrder(accountId=account, security=self.security, price=100, share=10)
        self.assertEquals(False, account.validate(order1))

        # buy it
        order1=BuyOrder(account=account, security=self.security, price=100, share=9)
        self.assertEquals(True, account.validate(order1))

        # can't sell because don't have the stock
        order1=SellOrder(account=account, security=self.security_two, price=100, share=9)
        self.assertEquals(False, account.validate(order1))

        # can't sell because don't have the enough share
        order1=SellOrder(account=account, security=self.security, price=100, share=9000)
        self.assertEquals(False, account.validate(order1))

        # sell it
        order1=SellOrder(account=account, security=self.security, price=100, share=9)
        self.assertEquals(True, account.validate(order1))
