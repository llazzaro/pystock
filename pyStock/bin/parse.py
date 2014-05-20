#!/usr/bin/env python
import optparse

if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage)
    parser.add_option("-s", "--format", dest="format",
                    action="store",
                    default='metastock',
                    help="Filetype format, use metastock for example")
    options, args = parser.parse_args()

    if options.format == 'metastock':
        print 'meta'
