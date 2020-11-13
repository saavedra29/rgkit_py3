rgkit -- Testing kit for Robot game
===============================================================
This is the code from https://github.com/RobotGame/rgkit with minor changes to work in Python 3.

Installing as a package
--------------------------------

**pip**

The easiest way to install the kit is with
`pip <http://www.pip-installer.org/en/latest/>`__. From the terminal,
run:

::

    pip install rgkit_py3

Or if you want the development version:

::

    pip install git+https://github.com/saavedra29/rgkit.git

**Note:** *This will install rgkit system-wide. It is recommended to use*
`virtualenv <http://www.virtualenv.org/en/latest/>`__
*to manage development environments.*

**virtualenv**

Installing with ``virtualenv`` requires the following steps:

::

    mkdir my_robot
    cd my_robot
    virtualenv env
    source env/bin/activate
    pip install rgkit

**setup.py**

You can also manually install directly from the source folder. Make a
local copy of the git repository or download the source files. Then,
using the terminal, run the following from the root directory of the
source code:

::

    python setup.py install

**Note:** *This will install rgkit system-wide. It is recommended to use*
`virtualenv <http://www.virtualenv.org/en/latest/>`__
*to manage development environments.*

**Running the game**

After installing the package, the script is executable from the command
line (if you're using virtualenv, remember to activate the environment).
There are two entry points provided: ``rgrun`` and ``rgmap``. The
general usage of run is:

::

    usage: rgrun [-h] [-m MAP] [-c COUNT] [-A] [-q] [-H | -T | -C]
                 [--game-seed GAME_SEED]
                 [--match-seeds [MATCH_SEEDS [MATCH_SEEDS ...]]] [-r]
                 player1 player2

    Robot game execution script.

    positional arguments:
      player1               File containing first robot class definition.
      player2               File containing second robot class definition.

    optional arguments:
      -h, --help            show this help message and exit
      -m MAP, --map MAP     User-specified map file.
      -c COUNT, --count COUNT
                            Game count, default: 1, multithreading if >1
      -A, --animate         Enable animations in rendering.
      -q, --quiet           Quiet execution.
                            -q : suppresses bot stdout
                            -qq: suppresses bot stdout and stderr
                            -qqq: supresses all rgkit and bot output
      -H, --headless        Disable rendering game output.
      -T, --play-in-thread  Separate GUI thread from robot move calculations.
      -C, --curses          Display game in command line using curses.
      --game-seed GAME_SEED
                            Appended with game countfor per-match seeds.
      --match-seeds [MATCH_SEEDS [MATCH_SEEDS ...]]
                            Used for random seed of the first matches in order.
      -r, --random          Bots spawn randomly instead of symmetrically.

So, from a directory containing your\_robot.py, you can run a game
against the default robot and suppress GUI output with the following
command:

::

    rgrun -H your_robot.py defaultrobots.py

Developing with source
-----------------------------------

``rgkit`` is packaged as a module, but you *can* just checkout the
repository and import/run the source scripts.

::

    ./rgkit
    |--- rgkit
    |    |--- __init__.py
    |    |--- game.py
    |    |--- run.py
    |    |--- ...
    |    |--- your_robot.py
    |--- setup.py
    ...
    /path/your_other_robot.py

**Running the game**

To run the game with the source configured this way, use the terminal
and execute the following from the inner ``rgkit`` folder (i.e., in the
same directory as ``run.py``):

::

    python run.py your_robot.py /path/your_other_robot.py

Coding your own robots
------------------------------

Once installed, you should only need the ``rg`` module to develop your
own robots. The package can be imported like any other module:

::

    import rg

    class Robot:
        def act(self):
            return ['guard']

Other Tools
--------------------

Here are some excellent tools made by fellow players!

- `Open Source Bots <https://github.com/mpeterv/robotgame-bots>`__
- `Simulate Situations <https://github.com/mpeterv/rgsimulator>`__
- `Compare Bots <https://github.com/mueslo/rgcompare>`__

