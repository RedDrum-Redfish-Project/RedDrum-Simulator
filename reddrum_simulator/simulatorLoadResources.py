
# Copyright Notice:
#    Copyright 2018 Dell, Inc. All rights reserved.
#    License: BSD License.  For full license text see link: https://github.com/RedDrum-Redfish-Project/RedDrum-Simulator/LICENSE.txt

import sys
import os
import json

class RdLoadSimulatorStaticResources():
    def __init__(self, rdr):
        version=0.9
        self.rdr=rdr



    def loadStaticResourceDatabases(self,rdr):
        self.rdr.logMsg("INFO","........ verifying path to profile data")
        # verify path to the profile directory
        # verify that this profile dir exists
        profileDirPath=os.path.join(self.rdr.staticConfigDataPath, self.rdr.rdProfile )
        if not os.path.isdir(profileDirPath):
            errMsg="*****ERROR: Profile {} Resource Db directory does not exist. Exiting. (path: {})"
            self.rdr.logMsg("CRITICAL",errMsg.format(self.rdr.rdProfile, profileDirPath ))
            sys.exit(10)

        # managers
        #   if managersDb is not already loaded from cache, get it from static files, and update the cache
        if self.rdr.root.managers.managersDbDiscovered is False:
            self.rdr.logMsg("INFO","........ loading Managers resource data from profile default files for: {}".format(rdr.rdProfile))
            # managersDb
            self.rdr.root.managers.managersDb = self.loadStaticResourceDbFile( profileDirPath, "managersDb", "ManagersDb.json")
            self.rdr.root.managers.updateStaticManagersDbFile()
            self.rdr.root.managers.managersDbDiscovered=True
        else:
            self.rdr.logMsg("WARNING","..... loaded  Managers Resource data from previous resource cache")

        # chassis
        #   if chassisDb is not already loaded from cache, get it from static files
        if self.rdr.root.chassis.chassisDbDiscovered is False:
            self.rdr.logMsg("INFO","........ loading Chassis resource data from profile default files for: {}".format(rdr.rdProfile))

            # chassisDb
            self.rdr.root.chassis.chassisDb = self.loadStaticResourceDbFile( profileDirPath, "chassisDb", "ChassisDb.json")
            self.rdr.root.chassis.updateStaticChassisDbFile()

            # fansDb
            self.rdr.root.chassis.fansDb = self.loadStaticResourceDbFile( profileDirPath, "chassisDb", "FansDb.json")
            self.rdr.root.chassis.updateStaticFansDbFile()

            # tempSensorsDb
            self.rdr.root.chassis.tempSensorsDb = self.loadStaticResourceDbFile( profileDirPath, "chassisDb", "TempSensorsDb.json")
            self.rdr.root.chassis.updateStaticTempSensorDbFile()

            # powerSuppliesDb
            self.rdr.root.chassis.powerSuppliesDb = self.loadStaticResourceDbFile( profileDirPath, "chassisDb", "PowerSuppliesDb.json")
            self.rdr.root.chassis.updateStaticPowerSuppliesDbFile()

            # voltageSensorsDb
            self.rdr.root.chassis.voltageSensorsDb = self.loadStaticResourceDbFile( profileDirPath, "chassisDb", "VoltageSensorsDb.json")
            self.rdr.root.chassis.updateStaticVoltageSensorsDbFile()

            # powerControlDb
            self.rdr.root.chassis.powerControlDb = self.loadStaticResourceDbFile( profileDirPath, "chassisDb", "PowerControlDb.json")
            self.rdr.root.chassis.updateStaticPowerControlDbFile()

            # set discovered flag true
            self.rdr.root.chassis.chassisDbDiscovered=True

        else:
            self.rdr.logMsg("WARNING","..... loaded  Chassis Resource data from previous resource cache")

        # systems
        #   if systemsDb is not already loaded from cache, get it from static files
        if self.rdr.root.systems.systemsDbDiscovered is False:
            self.rdr.logMsg("INFO","........ loading Systems resource data from profile default files for: {}".format(rdr.rdProfile))

            # systemsDb
            self.rdr.root.systems.systemsDb = self.loadStaticResourceDbFile( profileDirPath, "systemsDb","SystemsDb.json")
            self.rdr.root.systems.updateStaticSystemsDbFile()

            # processorsDb
            self.rdr.root.systems.processorsDb = self.loadStaticResourceDbFile( profileDirPath, "systemsDb","ProcessorsDb.json")
            self.rdr.root.systems.updateStaticProcessorsDbFile()

            # simpleStorageDb
            self.rdr.root.systems.simpleStorageDb = self.loadStaticResourceDbFile( profileDirPath, "systemsDb","SimpleStorageDb.json")
            self.rdr.root.systems.updateStaticStorageDbFile()

            # ethernetInterfacesDb
            self.rdr.root.systems.ethernetInterfaceDb = self.loadStaticResourceDbFile( profileDirPath, "systemsDb","EthernetInterfacesDb.json")
            self.rdr.root.systems.updateStaticEthernetInterfacesDbFile()

            # memoryDb
            self.rdr.root.systems.memoryDb = self.loadStaticResourceDbFile( profileDirPath, "systemsDb","MemoryDb.json")
            self.rdr.root.systems.updateStaticMemoryDbFile()

            # set discovered flag true
            self.rdr.root.systems.systemsDbDiscovered=True

        else:
            self.rdr.logMsg("WARNING","..... loaded  Systems Resource data from previous resource cache")


        self.rdr.logMsg("INFO","........ resource Databases loading Completed: Profile: {}".format(self.rdr.rdProfile ))
        return(0)

  

    # worker function to load STATIC Resource db file into dict 
    def loadStaticResourceDbFile( self, profileDirPath, subDir, filename ):
        # get full path to the static resource file for this profile
        filePath=os.path.join( profileDirPath, subDir, filename)    

        # read the data into a dict
        if os.path.isfile(filePath):
            resourceData=json.loads( open(filePath,"r").read() )
            return(resourceData)
        else:
            errMsg="*****ERROR: Resource Json DataBase file:{} Does not exist. Exiting."
            self.rdr.logMsg("CRITICAL",errMsg.format(filePath))
            sys.exit(10)
        return(None)
