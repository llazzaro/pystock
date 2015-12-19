from decimal import Decimal
from sqlalchemy.orm import object_session


def order_with_open_stage(mapper, connection, target):
    from pystock.models import OpenOrderStage
    target.update_stage(OpenOrderStage())


def validate_buy_order(mapper, connection, target):
    from pystock.models.money import Money
    from pystock.models import Position, OpenPositionStage
    cost = target.share * target.price + target.account.broker.commission(target)
    if cost > target.account.cash[target.security.currency]:
        raise Exception('Transition fails validation: cash {0} is smaller than cost {1}'.format(target.account.cash[target.security.currency], cost))

    target.account.deposit(Money(amount=target.share * -1 * Decimal(target.price), currency=target.security.exchange.currency))
    session = object_session(target)
    position = Position(buy_order=target, stage=OpenPositionStage(), share=target.share, account=target.account)
    session.add(position)


def validate_sell_order(mapper, connection, target):
    from pystock.models import SecurityQuote, Tick
    currency = target.security.exchange.currency
    if target.security.symbol not in target.account.holdings.keys():
        raise Exception('Transition fails validation: symbol {0} not in holdings'.format(target.security.symbol))
    elif target.share > target.account.holdings[target.security.symbol]:
        raise Exception('Transition fails validation: share {0} is not enough as {1}'.format(target.share, target.account.holdings[target.security.symbol]))
    elif target.account.broker.commission(target) > target.account.cash[currency]:
        raise Exception('Transition fails validation: cash {0} is not enough for commission {1}'.format(target.account.cash, target.account.broker.commision(target)))

    latest_quote = object_session(target).query(SecurityQuote).order_by('date desc').limit(1).first()
    latest_tick = object_session(target).query(Tick).order_by('trade_date desc').limit(1).first()

    close_price = (latest_quote and latest_quote.close_price) or (latest_tick and latest_tick.price)
    if target.is_stop and target.price > close_price:
        raise Exception("Sell stop order price %s shouldn't be higher than market price %s" % (target.price, close_price))


def validate_buy_to_cover(mapper, connection, target):
    from pystock.models import SecurityQuote
    latest_quote = object_session(target).query(SecurityQuote).order_by('date desc').limit(1).first()
    close_price = latest_quote.close_price
    if target.is_stop and target.price < close_price:
        raise Exception("Buy to cover stop target price %s shouldn't be higher than market price %s" % (target.price, close_price))
