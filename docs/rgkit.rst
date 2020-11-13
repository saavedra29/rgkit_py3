rgkit - Command Line Interface
==============================

To test your robots beforehand, please download the latest rgkit from
pip, or use the link on the Stats page (which is also the version of
rgkit that the server uses). The ``rg`` module is part of that kit.

You can use ``pip install -U rgkit`` and run:
``bash $ rgrun yourcode.py yourothercode.py``

Or you can gunzip and untar it wherever you want and run:
``bash $ python rgkit/rgkit/run.py yourcode.py yourothercode.py`` and it
will launch a game between ``yourcode.py`` and ``yourothercode.py``. If
you've only written one AI, you can just run it against itself.

``run.py`` also takes optional parameters. Two common ones are:

::

        -m, --map <map>: specifies a map file
        -H, --headless: runs without the UI (e.g. for A/B testing, etc.)
        -c, --count <number>: specifies a number of games to run concurrently.

More information (and the development version) can be found on GitHub.
