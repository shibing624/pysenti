"""pysenti command line interface."""
import sys
from argparse import ArgumentParser

import pysenti
from pysenti.compat import PY2, default_encoding

parser = ArgumentParser(usage="%s -m pysenti [options] filename" % sys.executable,
                        description="pysenti command line interface.",
                        epilog="If no filename specified, use STDIN instead.")
parser.add_argument("-d", "--dict", help="use DICT as dictionary")
parser.add_argument("-u", "--user-dict",
                    help="use USER_DICT together with the default dictionary or DICT (if specified)")
parser.add_argument("-a", "--output-all",
                    action="store_true", dest="oupput all info", default=False,
                    help="output text sentiment score and word sentiment info")
parser.add_argument("-V", '--version', action='version',
                    version="pysenti " + pysenti.__version__)
parser.add_argument("filename", nargs='?', help="input file")

args = parser.parse_args()

fp = open(args.filename, 'r') if args.filename else sys.stdin

if args.dict:
    pysenti.rule_classifier.init(sentiment_dict_path=args.dict)
else:
    pysenti.rule_classifier.init()
if args.user_dict:
    pysenti.rule_classifier.load_user_sentiment_dict(args.user_dict)

ln = fp.readline()
while ln:
    l = ln.rstrip('\r\n')
    result = '\t'.join(pysenti.classify(ln.rstrip('\r\n')))
    if PY2:
        result = result.encode(default_encoding)
    print(result)
    ln = fp.readline()

fp.close()
