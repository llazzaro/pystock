from decimal import Decimal
from sqlalchemy.orm import object_session


def validate_buy_order(mapper, connection, target):
    from pyStock.models.money import Money
    from pyStock.models import Position, OpenPositionStage
    cost = target.share * target.price + target.account.broker.commission(target)
    if cost > target.account.cash[target.security.currency]:
        raise Exception('Transition fails validation: cash {0} is smaller than cost {1}'.format(target.account.cash[target.security.currency], cost))
    # TODO create the withdraw from account
    target.account.withdraw(Money(amount=target.share * Decimal(target.price), currency=target.security.exchange.currency))
    session = object_session(target)
    position = Position(buy_order=target, stage=OpenPositionStage(), share=target.share, account=target.account)
    session.add(position)


def validate_sell_order(mapper, connection, target):
    from pyStock.models import SecurityQuote, Action
    currency = target.security.exchange.currency
    if target.security.symbol not in target.account.holdings.keys():
        raise Exception('Transition fails validation: symbol {0} not in holdings'.format(target.security.symbol))
    elif target.share > target.account.holdings[target.security.symbol]:
        raise Exception('Transition fails validation: share {0} is not enough as {1}'.format(target.share, target.account.holdings[target.security.symbol]))
    elif target.account.broker.commission(target) > target.account.cash[currency]:
        raise Exception('Transition fails validation: cash {0} is not enough for commission {1}'.format(target.account.cash, target.account.broker.commision(target)))

    latest_quote = object_session(target).query(SecurityQuote).order_by('date desc').limit(1).first()
    close_price = latest_quote.close_price
    if target.action == Action.STOP and target.price > close_price:
        raise Exception("Sell stop order price %s shouldn't be higher than market price %s" % (target.price, close_price))


def validate_buy_to_cover(mapper, connection, target):
    from pyStock.models import SecurityQuote, Action
    latest_quote = object_session(target).query(SecurityQuote).order_by('date desc').limit(1).first()
    close_price = latest_quote.close_price
    if Action.STOP == target.type and target.price < close_price:
        raise Exception("Buy to cover stop target price %s shouldn't be higher than market price %s" % (target.price, close_price))


