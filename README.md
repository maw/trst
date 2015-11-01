trst - kind of like sed

What is this?
=============

trst is a program to read input streams, replacing certain patterns with
certain other patterns.  It is modelled loosely on the classic sed program,
but it aims to be easier to use while remaining as powerful.

What does trst mean?
====================

tr for TRanslate, TRansfigure, TRansform.  st for STrings or STreams.

Also sed is Spanish for thirst and trst isn't too far from how a native
Spanish speaker might pronounce thirst.

Why should I use it?
====================

When using sed, have you ever got your regular expressions right very quickly,
only to spend far too much time getting escaping -- both for the shell and for
sed itself -- right? I have.

trst also includes a number of convenient extras:

The --spaces argument:

echo 'first second third' | ./trst.py --verbose -s all first second third '\3 \2 \1'



Why shouldn't I use it?
=======================

It's certainly buggy. Please don't use it on important files you don't have
backed up or which aren't in version control.

Why is it in Python?
====================

Easy prototyping.  Getting the command line parsing is tricky, not because
libraries to do it are deficient (quite the opposite in fact) but rather
because it isn't really clear at all what the command line arguments should
be. Doing it in Python means that I -- and hopefully you too -- can

Once I'm reasonably happy with how it works, rewriting it in a faster
language is something I'm open to.

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
