Library documentation
=====================

Robot Game comes with a library to make your life easier. It's packaged
inside the rg module which you can import like any other, by writing
import rg at the top of your file. Things to note:

Locations are represented by tuples of the form (x, y).

method ``rg.dist(loc1, loc2)``
------------------------------

Returns the mathematical distance between two locations.

method ``rg.wdist(loc1, loc2)``
-------------------------------

Returns the walking difference between two locations. Since robots can't
move diagonally, this is ``dx + dy``.

method ``rg.loc_types(loc)``
----------------------------

Returns a list of the types of locations that loc is. Possible values
are:

::

    `invalid` — out of bounds (e.g. (-1, -5) or (23, 66))
    `normal` — on the grid
    `spawn` — spawn point
    `obstacle` — somewhere you can't walk (all the gray squares)

This method has no contextual information about the game—\ ``obstacle``,
for example, doesn't know if there's an enemy robot standing on a
square, for example. All it knows is whether a square is a map obstacle.

The returned list may contain a combination of these, like

.. code:: python

    ['normal', 'obstacle']

method ``rg.locs_around(loc[, filter_out=None)``
------------------------------------------------

Returns a list of adjacent locations to loc. You can supply a list of
location types to filter out as ``filter_out``. For example,

.. code:: python

    rg.locs_around(self.location, filter_out=('invalid', 'obstacle'))

would give you a list of all locations you can move into.

method ``rg.toward(current_loc, dest_loc)``
-------------------------------------------

Returns the next point on the way from current\_loc to dest\_loc. For
example, the following code

.. code:: python

    import rg

    class Robot:
        def act(self, game):
            if self.location == rg.CENTER_POINT:
                return ['suicide']
            return ['move', rg.toward(self.location, rg.CENTER_POINT)]

would make your robot move to the center, then commit suicide.

constant rg.CENTER\_POINT
-------------------------

The location of the center of the board.

AttrDict rg.settings
--------------------

A special type of dict that can be accessed via attributes that holds
game settings.

``rg.settings.spawn_every`` how many turns pass between robots being
spawned

``rg.settings.spawn_per_player`` how many robots are spawned per player

``rg.settings.robot_hp`` default robot HP

``rg.settings.attack_range`` a tuple (minimum, maximum) holding range of
damage dealt by attacks

``rg.settings.collision_damage`` damage dealt by collisions

``rg.settings.suicide_damage`` damage dealt by suicides

``rg.settings.max_turns`` number of turns per game
