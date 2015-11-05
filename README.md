trst - kind of like sed

What is trst?
=============

trst is a program to read input streams, replacing certain patterns with
certain other patterns.  It is modelled loosely on the classic sed program,
but it aims to be easier to use while remaining as powerful in most use cases.

What does trst mean?
====================

tr is for TRanslate, TRansfigure, TRansform, TRansmute.  st is for STrings
or STreams.

"sed" is Spanish for thirst; "trst" isn't too far from how a native
Spanish speaker might pronounce thirst.

Why should I use it?
====================

When using sed, have you ever got your regular expressions right quickly,
only to spend far too much time getting escaping -- both for the shell and for
sed itself -- right? I have.

trst attempts to alleviate that pain through a variety of convenient features.

* Easy escaping and easy to read positional arguments

  By default when '%' starts an expression the expression is escaped. (You can choose a
  different character for this if you wish.)

  Try this:

  `echo '$dont[dothis] = 123;' | ./trst.py all '%$' '[a-zA-Z0-9]+' '%[' '[a-zA-Z][a-zA-Z0-9]*' '%]' "\1\2\3'\4'\5"`

  Now try to do it in sed. Modulo tyops, did it work right for you the first
  time with sed? It didn't for me, but with trst it did.


* The --spaces argument:

  Try this:

  `echo 'first second third' | ./trst.py --verbose --spaces all first second third '\3 \2 \1'`

  Or this:

  `echo 'first      second  third' | ./trst.py --verbose --spaces all first second third '\3 \2 \1'`

* The --debug argument:

  Of course, sometimes debugging your regular expressions really is the hard
  part. If so, try this:

  `echo 'hello world' | ./trst.py --debug all 'h[ea]llo' world  'wow dude'`

  Then try this:

  `echo 'world hello' | ./trst.py --debug all 'h[ea]llo' world  'wow dude'`


Why shouldn't I use it?
=======================

It's certainly buggy. Please don't use it on important files you don't have
backed up or which aren't in version control.

Also, trst's command line arguments and flags are experimental and subject to
change. If you use it in a script your script could break later.

Why is it in Python?
====================

Easy prototyping.  Getting the command line parsing right is tricky, not
because libraries to do it are deficient (quite the opposite in fact) but
rather because it isn't really clear at all what the command line
arguments should be. Doing it in Python means that I -- and hopefully
you too -- can experiment easily.

Once I'm reasonably happy with how it works, rewriting it in a faster
language is something I'm open to.

What remains to be done?
========================

* Create a test suite
* Fix bugs
* Come up with a ridiculous logo.

Random notes
============

Usage ideas:


trst [general args] [search args] [args]


Questions:

* What sorts of subcommands make sense?

  Possibilities: replace-all, replace-any. If none, assume replace-all?

* What sorts of general args make sense?
  
  Apply more than once in a given line -- cf sed's /g -- by default?

* How to avoid or mitigate shell quoting annoyances?

* What symbols -- ie, more or less anything you get by hitting shift + number
