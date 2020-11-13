Getting Started
===============

1. Creating a robot
-------------------

This is the basic structure of every robot file:

.. code:: python

    class Robot:
        def act(self, game):
            return [<some action>, <params>]

At the beginning of the game, the system creates one instance of your
Robot class. This means that class variables and your module's global
variables are shared between calls. Every turn the system calls that
single instance's act method once for each of your robots to determine
its next action. (Again, please read the rules first.) The method should
return one of:

.. code:: python

    ['move', (x, y)]
    ['attack', (x, y)]
    ['guard']
    ['suicide']

If act throws an exception or returns an invalid command, the robot will
simply guard, but if it times out too many times then it will be forced
to surrender the match. Please see Security for those details.

2. Accessing the robot's info
-----------------------------

Every robot, including self, has the following properties exposed:

-  ``location`` — the robot's location as a tuple (x, y)
-  ``hp`` — the robot's health as an int
-  ``player_id`` — the robot's player\_id (what "team" it belongs to)
-  ``robot_id`` — a unique number identifying each robot (only available
   for robots on your team)

For example, to access the current robot's HP, you would write self.hp.

Every turn, the system calls your act method, passing it a game
parameter set to the following structure:

.. code:: python

    {
        # a dictionary of all robots on the field mapped
        # by {location: robot}
        'robots': {
            (x1, y1): {
                'location': (x1, y1),
                'hp': hp,
                'player_id': player_id,

                # only if the robot is on your team
                'robot_id': robot_id
            },

            # ...and the rest of the robots
        },

        # number of turns passed (starts at 0)
        'turn': turn
    }

``game`` and every robot in ``game['robots']`` are instances of a
special type of dict where you can access values using attributes. This
is to make writing code faster. So, the following are equivalent:

.. code:: python

    game['robots'][location]['hp']
    game['robots'][location].hp
    game.robots[location].hp

Here's a quick example to print out the location of any robots that are
on your team:

.. code:: python

    class Robot:
        def act(self, game):
            for loc, robot in game.robots.items():
                if robot.player_id == self.player_id:
                    print loc

3. Example starting robot
-------------------------

Here's a simple robot to use as a starting point. It looks for any
enemies around and attacks them. Otherwise, it tries to move to the
center.

.. code:: python

    import rg

    class Robot:
        def act(self, game):
            # if we're in the center, stay put
            if self.location == rg.CENTER_POINT:
                return ['guard']

            # if there are enemies around, attack them
            for loc, bot in game.robots.iteritems():
                if bot.player_id != self.player_id:
                    if rg.dist(loc, self.location) <= 1:
                        return ['attack', loc]

            # move toward the center
            return ['move', rg.toward(self.location, rg.CENTER_POINT)]

As you can see, there is a module called rg being used. We'll look at
this next.

Implementation detail: only one instance of your robot is created each
game, so you can store persistent data in your instance variables.
