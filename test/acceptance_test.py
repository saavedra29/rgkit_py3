import unittest
from os import path
# TODO: Make this hack better -_-.
try:
    import subprocess as runcommand
except:
    import subprocess as runcommand


class TestAttack(unittest.TestCase):
    def test_acceptance_cli(self):
        testdir = path.dirname(__file__)

        # test if -h runs
        cmd = testdir + "/../rgkit/run.py -h"
        exit_code, ignore = runcommand.getstatusoutput(cmd)
        self.assertEqual(exit_code, 0)

        robot_file = testdir + "/acceptance_robot.py"
        # test simple robot
        cmd = testdir + "/../rgkit/run.py -H {0} {0}".format(robot_file)

        exit_code, out = runcommand.getstatusoutput(cmd)
        self.assertEqual(exit_code, 0)
