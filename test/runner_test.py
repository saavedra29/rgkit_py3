
import unittest

import rgkit
from rgkit.run import Runner, Options
from rgkit.settings import settings as rgkit_settings
import rgkit.gamestate as gamestate


class TestRobot:
    def act(self, game):
        return ['guard']

called = False


class TestRunner(unittest.TestCase):
    def test_default_options(self):
        options = Options()
        assert options.map_filepath is not None
        assert isinstance(options.map_filepath, str)

        assert isinstance(options.print_info, bool)
        assert isinstance(options.n_of_games, int)
        assert isinstance(options.animate_render, bool)

    def test_default_settings(self):
        settings = Runner.default_settings()
        assert settings is not None
        assert settings == rgkit_settings

    def test_runner_from_robots(self):
        print((TestRobot().__class__))
        runner = Runner.from_robots([TestRobot(), TestRobot()])
        self.assertEqual(runner.options, Options())
        runner.settings.max_turns = 1
        runner.options.headless = True
        runner.options.quiet = 4
        runner.run()

    def test_runner_delta_callback(self):
        def callback(delta, game_state):
            global called
            called = True
            assert type(delta) is list
            assert type(delta[0]) is rgkit.settings.AttrDict
            assert type(game_state) is gamestate.GameState

        runner = Runner.from_robots([TestRobot(), TestRobot()],
                                    delta_callback=callback)
        runner.options.headless = True
        runner.options.quiet = 4
        runner.run()
        assert called

    def test_runner_from_robots_perf(self):

        runner = Runner.from_robots([TestRobot(), TestRobot()])
        runner.options.n_of_games = 100
        runner.settings.max_turns = 100
        # uncomment for profiling
        # import cProfile
        # cProfile.runctx("runner.runs()", globals(), locals())
