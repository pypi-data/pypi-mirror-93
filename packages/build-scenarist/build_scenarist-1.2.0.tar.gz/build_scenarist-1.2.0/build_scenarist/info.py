# -*- coding: UTF-8 -*-
 
import os
import re
import platform
import build_scenarist.utility
from build_scenarist.config import defaultScenarioNameEnding

class Info:
    def osName(self):
        return platform.system().replace('"', '')
    
    def distName(self):
        distName = None
        if self.osName() == "Linux":
            osRelease = open('/etc/os-release').read()
            options = re.findall( r'.*=.*', osRelease)
            optionsMap = {}
            for option in options:
                nameValue  = option.split('=')
                optionsMap[nameValue[0]] = nameValue[1]

            if "NAME" in optionsMap:
                distName = optionsMap["NAME"].replace('"', '').replace(' ', '')
        elif self.osName() == "Windows":
            distName = platform.win32_ver()[0].replace('"', '')
        elif self.osName() == "Darwin":
            distName = "MacOS"

        return distName

    def distVersion(self):
        distVersion = None

        if self.osName() == "Linux":
            osRelease = open('/etc/os-release').read()
            options = re.findall( r'.*=.*', osRelease)
            optionsMap = {}
            for option in options:
                nameValue  = option.split('=')
                optionsMap[nameValue[0]] = nameValue[1]

            if "VERSION_ID" in optionsMap:
                distVersion = optionsMap["VERSION_ID"].replace('"', '').replace(' ', '')

        elif self.osName() == "Windows":
            distVersion = platform.win32_ver()[2].replace('"', '')
        elif self.osName() == "Darwin":
            distVersion = platform.mac_ver()[0]

        return distVersion

    def fullPlatformName(self):
        result = self.osName()

        if self.distName():
            result += '_' + self.distName()

        if self.distVersion():
            result += '_' + self.distVersion()

        return result


    def defaultScriptName(self):
        return self.fullPlatformName() + defaultScenarioNameEnding

    def scriptName(self, osName, distName, distVersion):
        return osName + '_' + distName + ' ' + distVersion + defaultScenarioNameEnding

    def about_platform(self):
        osNameString = "-"
        if self.osName():
            osNameString = self.osName()

        distNameString = "-"
        if self.distName():
            distNameString = self.distName()

        distVersionString = "-"
        if self.distVersion():
            distVersionString = self.distVersion()

        return """            OS name:    {0}
          Dist name:    {1}
          Dist version: {2}
Default script name:    {3}""".format(osNameString, distNameString, distVersionString, self.defaultScriptName())