Security
========

When your app is remote code execution, you have to be a bit paranoid.
To be upfront, here are the measures taken on the server.

-  all robot code is run in a chroot jail
-  all robot code is run as the user nobody
-  all robot code is run with umask set to 0
-  each Robot must take less than 2000ms to compile and initialize
-  the first act call of each turn is limited to 1500ms
-  each subsequent act call is limited to 300ms
-  the match will be forfeited if 3 or more errors (including timeouts)
   occur
-  the following modules are explicitly disabled:

   -  ``ctype``
   -  ``imp``
   -  ``inspect``
   -  ``multiprocessing``
   -  ``os``
   -  ``pdb``
   -  ``posix``
   -  ``sys``
   -  additional modules that depend on these also cannot be imported
      (e.g. code, logging, etc)

Please consider these things when you're coding your robots.
