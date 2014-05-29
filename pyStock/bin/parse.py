#!/usr/bin/env python
import csv
import optparse
import datetime
from functools import reduce
from operator import add
from itertools import izip
from sqlalchemy.orm import sessionmaker

from pyStock.models import Asset, Quote, get_or_create
from pyStock import engine


def import_metastock(session, filename):
    with open(filename, 'rb') as csvfile:
        incsv = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(incsv)  # skip header
        for row in incsv:
            print 'row', row
            x = iter(str(row[1]))
            splitted_date = [reduce(add, tup) for tup in izip(x, x)]
            day = int(splitted_date[2])
            month = int(splitted_date[1])
            year = 2000 + int(splitted_date[0])
            tick_date = datetime.datetime(year, month, day)
            symbol = row[0]
            open_value = row[2]
            high = row[3]
            low = row[4]
            close = row[5]
            asset, created = get_or_create(session, Asset, symbol=symbol, ISIN=symbol)
            Quote(tick_date=tick_date, asset=asset, px_open=open_value, px_high=high, px_low=low, px_close=close)
            session.commit()


if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage)
    parser.add_option(
        "-s", "--format", dest="format",
        action="store",
        default='metastock',
        help="Filetype format, use metastock for example")

    parser.add_option(
        "-f", "--filename", dest="filename",
        action="store",
        default=None,
        help="Filename for the file to import")

    options, args = parser.parse_args()

    if options.filename is None:
        raise Exception()

    # create a configured "Session" class
    Session = sessionmaker(bind=engine)

    # create a Session
    session = Session()

    if options.format == 'metastock':
        import_metastock(session, options.filename)
