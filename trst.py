#!/usr/bin/env python3

import re
import sys

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
    if len(args.expressions) < 2:
        if args.verbose:
            sys.stderr.write("fdsa\n")
        sys.exit(1)
    
    esc = args.esc
    # print(args.esc)
    replacement = args.expressions[-1]
    
    def maybe_escape(arg):
        print("esc: %s" % (esc,))
        if arg.startswith(esc):
            print("escaping")
            return re.escape(arg[1:])
        return arg
    
    exprs = ['(' + maybe_escape(expr) + ')' for expr in args.expressions[:-1]]
    print("exprs: %s" % (exprs,))
    jchar = ''
    if args.inject_spaces is True:
        jchar = ' '
    expr = jchar.join(exprs)
    print("expr: %s" % (expr,))
    regex = re.compile(expr)
    print("regex: %s" % (regex,))
        
    for idx, line in enumerate(sys.stdin):
        line = line.strip()
        out = re.sub(regex, replacement, line)
        print("%d: %s" % (idx, line))
        print("%d: %s" % (idx, out))
    
    pass

if __name__ == '__main__':
    sys.exit(main(sys.argv))

