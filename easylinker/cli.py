#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import sys
if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

from . import config
from . import parsers

def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        filename = parsers.to_unicode(filename)
        parsers.run(filename)
    else:
        msg = 'Usage: {} <metadata>'.format(sys.argv[0])
        print(msg)
        print('\nPredefined Variables')
        for k, v in config.PREDEFINED_VARIABLE_TABLE.items():
            print('{}\t: {}'.format(k, v))

if __name__ == '__main__':
    main()
