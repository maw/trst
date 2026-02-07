#!/usr/bin/env python3

import argparse
import re
import sys

VERBOSE = False


def log_debug(msg):
    if VERBOSE:
        sys.stderr.write(f"{msg}\n")
        sys.stderr.flush()


def build_parser():
    parser = argparse.ArgumentParser(
        prog="trst",
        description="Replace patterns in text streams — a friendlier sed alternative",
    )
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true")
    parser.add_argument(
        "-Q",
        "--literal",
        dest="literal",
        action="store_true",
        help="Force all arguments to be escaped; note that"
        " leading escape characters will not be removed",
    )
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        help="Operate in special debugging mode",
    )
    parser.add_argument(
        "-e",
        "--escape",
        dest="esc",
        help="Prefix to force escaping immediately subsequent metacharacters; defaults to %%",
        default="%",
    )
    parser.add_argument(
        "-i",
        "--ignore-case",
        dest="case_insensitive",
        action="store_true",
        help="Match case insensitively",
    )
    parser.add_argument(
        "-s",
        "--spaces",
        dest="inject_spaces",
        help="Allow flexible whitespace between expressions",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "expressions",
        metavar="EXPR",
        type=str,
        nargs="+",
        help="Search expressions followed by a replacement string",
    )
    return parser


def main(argv=None):
    global VERBOSE

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.verbose:
        VERBOSE = True

    if len(args.expressions) < 2:
        parser.error("need at least one search expression and a replacement")

    esc = args.esc
    replacement = args.expressions[-1]

    def maybe_escape(arg):
        log_debug(f"esc: {esc}")
        if arg.startswith(esc):
            log_debug("escaping")
            return re.escape(arg[len(esc) :])
        return arg

    if args.literal:
        exprs = ["(" + re.escape(expr) + ")" for expr in args.expressions[:-1]]
    else:
        exprs = ["(" + maybe_escape(expr) + ")" for expr in args.expressions[:-1]]
    log_debug(f"exprs: {exprs}")

    jchar = r"\s*" if args.inject_spaces else ""

    expr = jchar.join(exprs)
    log_debug(f"expr: {expr}")

    flags = re.IGNORECASE if args.case_insensitive else 0
    regex = re.compile(expr, flags)
    log_debug(f"regex: {regex}")

    for idx, line in enumerate(sys.stdin):
        line = line.rstrip("\n")
        if args.debug:
            matches = []
            for eidx, single_expr in enumerate(exprs):
                mo = re.search(re.compile(single_expr, flags), line)
                if mo is not None:
                    last_match = None
                    if len(matches) > 0:
                        last_match = matches[-1]
                    print(f"expression #{eidx + 1} {single_expr} matches")
                    if last_match is not None and mo.span()[0] <= last_match.span()[1]:
                        print("but it came before the previous match!")
                    print(f"> {line}")
                    spaces = " " * mo.span()[0]
                    carets = "^" * (mo.span()[1] - mo.span()[0])
                    print(f"  {spaces}{carets}")
                    matches.append(mo)
                else:
                    print(f"expression {single_expr} does not match")
        else:
            out = re.sub(regex, replacement, line)
            log_debug(f"{idx}: {line}")
            log_debug(f"{idx}: {out}")
            print(out)

    return 0


if __name__ == "__main__":
    sys.exit(main())
