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
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    parser.add_argument('-Q', '--literal', dest='literal', action='store_true',
                        help="Force all arguments to be escaped; note that " + \
                        " leading escape characters will not be removed")
    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                        help="Operate in special debugging mode")
    parser.add_argument('-e', '--escape', dest='esc',
                        help="Prefix to force escaping immediately subsequent " +
                        "metacharacters; defaults to %%",
                        default='%')
    parser.add_argument('-i', '--ignore-case', dest='case_insensitive',
                        action='store_true', help="Match case insensitively (not yet implemented)")
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
    if args.verbose is True:
        VERBOSE = True
    if len(args.expressions) < 2:
        spam("too few arguments")
        sys.exit(1)
    
    esc = args.esc
    replacement = args.expressions[-1]
    
    def maybe_escape(arg):
        spam("esc: %s" % (esc,))
        if arg.startswith(esc):
            spam("escaping")
            return re.escape(arg[1:])
        return arg
    
    if args.literal is True:
        exprs = ['(' + re.escape(expr) + ')' for expr in args.expressions[:-1]]
    else:
        exprs = ['(' + maybe_escape(expr) + ')' for expr in args.expressions[:-1]]
    spam("exprs: %s" % (exprs,))
    jchar = ''
    if args.inject_spaces is True:
        jchar = '\s*'
    
    expr = jchar.join(exprs)
    spam("expr: %s" % (expr,))
    regex = re.compile(expr)
    spam("regex: %s" % (regex,))
        
    for idx, line in enumerate(sys.stdin):
        line = line.strip()
        if args.debug is True:
            for eidx, expr in enumerate(exprs):
                # does it match?
                # if it does, print line
                # and print a line below with carets
                # chop up line, try to match using the next expr
                # if it does not show the arg that doesn't and then give up for this line
                mo = re.search(re.compile(expr), line)
                if mo is not None:
                    print("expression #%d %s matches" % (eidx + 1, expr))
                    print("> %s" % (line,))
                    spaces = ''.join([' ' for _ in range(0, mo.span()[0])])
                    carets = ''.join(['^' for _ in range(0, mo.span()[1] - mo.span()[0])])
                    print("  %s%s" % (spaces, carets))
                else:
                    print("expression %s does not match" % (expr,))
        else:
            out = re.sub(regex, replacement, line)
            spam("%d: %s" % (idx, line))
            spam("%d: %s" % (idx, out))
            print("%s" % (out,))
    
    pass

if __name__ == '__main__':
    sys.exit(main(sys.argv))

