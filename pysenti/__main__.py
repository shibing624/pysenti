"""pysenti command line interface."""

import sys
from argparse import ArgumentParser

from pysenti import RuleClassifier, __version__
from pysenti.compat import PY2, default_encoding


def main(args):
    rule_classifier = RuleClassifier()
    fp = open(args.filename, 'r') if args.filename else sys.stdin

    if args.dict:
        rule_classifier.init(sentiment_dict_path=args.dict)
    else:
        rule_classifier.init()
    if args.user_dict:
        rule_classifier.load_user_sentiment_dict(args.user_dict)

    ln = fp.readline()
    while ln:
        r = rule_classifier.classify(ln.rstrip())
        if args.output_all:
            result = str(r)
        else:
            result = str(r['score'])
        if PY2:
            result = result.encode(default_encoding)
        print(result)
        ln = fp.readline()

    fp.close()


if __name__ == '__main__':
    parser = ArgumentParser(usage="%s -m pysenti [options] filename" % sys.executable,
                            description="pysenti command line interface.",
                            epilog="If no filename specified, use STDIN instead.")
    parser.add_argument("-d", "--dict", help="use DICT as dictionary")
    parser.add_argument("-u", "--user-dict",
                        help="use USER_DICT together with the default dictionary or DICT (if specified)")
    parser.add_argument("-a", "--output-all",
                        action="store_true", default=False,
                        help="output text sentiment score and word sentiment info")
    parser.add_argument("-V", '--version', action='version',
                        version="pysenti " + __version__)
    parser.add_argument("filename", nargs='?', help="input file")
    args = parser.parse_args()

    main(args)
