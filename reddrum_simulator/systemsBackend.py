
# Copyright Notice:
#    Copyright 2018 Dell, Inc. All rights reserved.
#    License: BSD License.  For full license text see link: https://github.com/RedDrum-Redfish-Project/RedDrum-Simulator/LICENSE.txt

# systemBackend resources for RedDrum Simulator 
#
class  RdSystemsBackend():
    # class for backend systems resource APIs
    def __init__(self,rdr):
        self.version=1
        self.rdr=rdr
        self.nonVolatileDataChanged=False


    # update resourceDB and volatileDict properties
    def updateResourceDbs(self,systemid, updateStaticProps=False, updateNonVols=True ):
        # for the simulator, just return (0,False).   The Sim backend currently doesnt update resources after discovery
        return(0,False)


    # DO action:   Reset Simulation
    def doSystemReset(self,systemid,resetType):
        self.rdr.logMsg("DEBUG","--------SIM BACKEND systemReset. resetType={}".format(resetType))

        # Simulator: set powerState as a function of resetType
        powerOnStates  = ["On", "GracefulRestart", "ForceRestart", "ForceOn", "PowerCycle"]
        powerOffStates = ["ForceOff","GracefulShutdown" ]
        if resetType in powerOnStates:
            newPowerState = "On"
        elif resetType in powerOffStates:
            newPowerState = "Off"
        else:
            newPowerState = None # dont change it

        # Simulator: set powerState for the system
        if newPowerState is not None:
            if "Volatile" in self.rdr.root.systems.systemsDb[systemid]:
                if "PowerState" in self.rdr.root.systems.systemsDb[systemid]["Volatile"]:
                    self.rdr.root.systems.systemsVolatileDict[systemid]["PowerState"] = newPowerState

            # Simulator: set powerState for the associated chassis
            if "Chassis" in self.rdr.root.systems.systemsDb[systemid]:
                for chassisid in self.rdr.root.systems.systemsDb[systemid]["Chassis"]:
                    if chassisid in self.rdr.root.chassis.chassisDb:
                        if "Volatile" in self.rdr.root.chassis.chassisDb[chassisid]:
                            if "PowerState" in self.rdr.root.chassis.chassisDb[chassisid]["Volatile"]:
                                self.rdr.root.chassis.chassisVolatileDict[chassisid]["PowerState"] = newPowerState

        return(0)


    # DO Patch to System  (IndicatorLED, AssetTag, or boot overrides
    # the front-end will send an individual call for IndicatorLED and AssetTag or bootProperties
    # multiple boot properties may be combined in one patch
    def doPatch(self, systemid, patchData):
        # the front-end has already validated that the patchData and systemid is ok
        # so just send the request here
        self.rdr.logMsg("DEBUG","--------BACKEND Patch system data. patchData={}".format(patchData))

        # for the simulator, just return(0).   The frontEnd databases have been updated
        return(0)


    # update ProcessorsDb 
    def updateProcessorsDbFromBackend(self, systemid, procid=None, noCache=False ):
        # for the simulator, just return (0).   The Sim backend currently doesnt update resources after discovery
        return(0)

    # update MemoryDb 
    def updateMemoryDbFromBackend(self, systemid, memid=None, noCache=False ):
        # for the simulator, just return (0).   The Sim backend currently doesnt update resources after discovery
        return(0)


    # update SimpleStorageDb 
    def updateSimpleStorageDbFromBackend(self, systemid, cntlrid=None, noCache=False ):
        # for the simulator, just return (0).   The Sim backend currently doesnt update resources after discovery
        return(0)

    # update EthernetInterfaceDb 
    def updateEthernetInterfaceDbFromBackend(self, systemid, ethid=None, noCache=False ):
        # for the simulator, just return (0).   The Sim backend currently doesnt update resources after discovery
        return(0)
