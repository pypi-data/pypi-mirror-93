# -*- coding: UTF-8 -*-
 
import sys
import os
import subprocess
import shlex

from subprocess import call

from . utility import splitTargetCallToNameAndParams
from . config import bcolors, global_vars, defaultScenarioNameEnding, defaultScenarioDir
from . runner import runTargets

def runTarget(targetCall, scenarios = "*", scenarioDir=defaultScenarioDir):
    if scenarios != "*":
        scenariosFullPathes = []
        for scenarioName in scenarios:
            path = os.path.join(scenarioDir, scenarioName)
            if os.path.isfile(path):
                scenariosFullPathes.append(path)
        scenarios = scenariosFullPathes

    runTargets([targetCall], scenarios)

def runShell(cmd, fallAtFail=True):
    sys.stdout.write("\n" + bcolors.HEADER + "shell: " + bcolors.ENDC + "\n")
    sys.stdout.write(bcolors.BOLD + cmd + bcolors.ENDC + "\n")
    sys.stdout.flush()
    retCode = subprocess.call(shlex.split(cmd))
    if retCode != 0 and fallAtFail:
        sys.stdout.write("\nShell code failed with code: " + str(retCode) + "\n")
        sys.stdout.flush()
        sys.exit(retCode)
    sys.stdout.write("\n")
    sys.stdout.flush()
    return retCode

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        try:
            os.chdir(self.newPath)
        except OSError:
            raise Exception(bcolors.FAIL + "Path: {0}. No such file or directory!".format(self.newPath) + bcolors.ENDC)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
