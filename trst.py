#!/usr/bin/env python3

import re
import sys

VERBOSE = False

def spam(str):
    if VERBOSE is True:
        sys.stderr.write("fdsa\n")
        sys.stderr.flush()

def build_parser():
    import argparse
    
    parser = argparse.ArgumentParser(description='replace things')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-e', '--escape-char', dest='esc', help="help!",
                        default='%')
    parser.add_argument('-s', '--spaces', dest='inject_spaces', help="inject spaces",
                        action='store_true', default=False)
    
    subparsers = parser.add_subparsers()
    all = subparsers.add_parser('all', help='they are all concatenated')
    all.add_argument('expressions', metavar='EXPR', type=str, nargs='+',
                     help='some expressions, at least two and maybe more')
    
    any = subparsers.add_parser('any', help='we check each in turn')
    any.add_argument('expressions', metavar='EXPR', type=str, nargs='+',
                     help="some expressions, at least two and maybe more")
    
    return parser


def main(args):
    parser = build_parser()
    
    args = parser.parse_args()
    # print(args.expressions)
    # print(type(args.expressions))
    # print(len(args.expressions))
    if args.verbose is True:
        VERBOSE = True
    if len(args.expressions) < 2:
        spam("too few arguments")
        sys.exit(1)
    
    esc = args.esc
    # print(args.esc)
    replacement = args.expressions[-1]
    
    def maybe_escape(arg):
        spam("esc: %s" % (esc,))
        if arg.startswith(esc):
            spam("escaping")
            return re.escape(arg[1:])
        return arg
    
    exprs = ['(' + maybe_escape(expr) + ')' for expr in args.expressions[:-1]]
    spam("exprs: %s" % (exprs,))
    jchar = ''
    if args.inject_spaces is True:
        jchar = ' '
    expr = jchar.join(exprs)
    spam("expr: %s" % (expr,))
    regex = re.compile(expr)
    spam("regex: %s" % (regex,))
        
    for idx, line in enumerate(sys.stdin):
        line = line.strip()
        out = re.sub(regex, replacement, line)
        spam("%d: %s" % (idx, line))
        spam("%d: %s" % (idx, out))
        print("%s" % (out,))
    
    pass

if __name__ == '__main__':
    sys.exit(main(sys.argv))

