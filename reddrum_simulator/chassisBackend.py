
# Copyright Notice:
#    Copyright 2018 Dell, Inc. All rights reserved.
#    License: BSD License.  For full license text see link: https://github.com/RedDrum-Redfish-Project/RedDrum-Simulator/LICENSE.txt

# BullRed-RackManager chassisBackend resources
#
class  RdChassisBackend():
    # class for backend chassis resource APIs
    def __init__(self,rdr):
        self.version=1
        self.rdr=rdr

    # update resourceDB and volatileDict properties
    def updateResourceDbs(self, chassisid, updateStaticProps=False, updateNonVols=True ):
        #self.rdr.logMsg("DEBUG","--------BACKEND updateResourceDBs. updateStaticProps={}".format(updateStaticProps))

        # for the simulator, just return--the front-end databases are not updated by the current SIM backend
        return(0,False)
      
    # Reset Chassis sled
    # resetType is a property string (not a dict)
    def doChassisReset(self,chassisid,resetType):
        self.rdr.logMsg("DEBUG","--------BACKEND chassisReset: chassisid: {}, resetType: {}".format(chassisid,resetType))

        # Simulator: set powerState as a function of resetType
        powerOnStates  = ["On", "GracefulRestart", "ForceRestart", "ForceOn", "PowerCycle"]
        powerOffStates = ["ForceOff","GracefulShutdown" ]
        if resetType in powerOnStates:
            newPowerState = "On"
        elif resetType in powerOffStates:
            newPowerState = "Off"
        else:
            newPowerState = None # dont change it



        # Simulator: set powerState to reseat powerstate for this chassis
        if newPowerState is not None:
            if "Volatile" in self.rdr.root.chassis.chassisDb[chassisid]:
                if "PowerState" in self.rdr.root.chassis.chassisDb[chassisid]["Volatile"]:
                    self.rdr.root.chassis.chassisVolatileDict[chassisid]["PowerState"] = newPowerState

            # xg TODO: set power-state for any down-stream chassis that this chassis powers to same value
            # xg for now, just set the power state and don't worry about it

            # Simulator: set powerState to reseat powerstate for any system that this chassis is a part of 
            #    If the chassis is a jbod sled, this may not be totally correct, but is all we can do with current model
            if "ComputerSystems" in self.rdr.root.chassis.chassisDb[chassisid]:
                for systemid in self.rdr.root.chassis.chassisDb[chassisid]["ComputerSystems"]:
                    if systemid in self.rdr.root.systems.systemsDb:
                        if "Volatile" in self.rdr.root.systems.systemsDb[systemid]:
                            if "PowerState" in self.rdr.root.systems.systemsDb[systemid]["Volatile"]:
                                self.rdr.root.systems.systemsVolatileDict[systemid]["PowerState"] = newPowerState
        return(0)

    # Reseat Chassis sled
    def doChassisOemReseat(self, chassisid):
        self.rdr.logMsg("DEBUG","--------BACKEND chassisReseat: chassisid: {} ".format(chassisid))

        # Simulator: set powerState to reseat powerstate for this chassis
        #    only a leaf chassis (sled) can be reseated
        if "Volatile" in self.rdr.root.chassis.chassisDb[chassisid]:
            if "PowerState" in self.rdr.root.chassis.chassisDb[chassisid]["Volatile"]:
                self.rdr.root.chassis.chassisVolatileDict[chassisid]["PowerState"] = self.rdr.backend.powerOnState

        # Simulator: set powerState to reseat powerstate for any system that this chassis is a part of 
        #    If the chassis is a jbod sled, this may not be totally correct, but is all we can do with current model
        if "ComputerSystems" in self.rdr.root.chassis.chassisDb[chassisid]:
            for systemid in self.rdr.root.chassis.chassisDb[chassisid]["ComputerSystems"]:
                if systemid in self.rdr.root.systems.systemsDb:
                    if "Volatile" in self.rdr.root.systems.systemsDb[systemid]:
                        if "PowerState" in self.rdr.root.systems.systemsDb[systemid]["Volatile"]:
                            self.rdr.root.systems.systemsVolatileDict[systemid]["PowerState"] = self.rdr.backend.powerOnState
        return(0)


    # DO Patch to chassis  (IndicatorLED, AssetTag)
    # patchData is a dict with one property
    #    the front-end will send an individual call for IndicatorLED and AssetTag 
    def doPatch(self, chassisid, patchData):
        # the front-end has already validated that the patchData and chassisid is ok
        # so just send the request here
        self.rdr.logMsg("DEBUG","--------BACKEND Patch chassis data. patchData={}".format(patchData))

        # for the simulator, just return--the front-end databases are not updated by the current SIM backend
        return(0)


    # update Temperatures resourceDB and volatileDict properties
    # returns: rc, updatedResourceDb(T/F).  rc=0 if no error
    def updateTemperaturesResourceDbs(self, chassisid, updateStaticProps=False, updateNonVols=True ):
        self.rdr.logMsg("DEBUG","--------BE updateTemperaturesResourceDBs. updateStaticProps={}".format(updateStaticProps))
        return (0,False)

    # update Fans resourceDB and volatileDict properties
    # returns: rc, updatedResourceDb(T/F).  rc=0 if no error
    def updateFansResourceDbs(self, chassisid, updateStaticProps=False, updateNonVols=True ):
        self.rdr.logMsg("DEBUG","--------BE updateFansResourceDBs. updateStaticProps={}".format(updateStaticProps))
        return (0,False)


    # update Voltages resourceDB and volatileDict properties
    # returns: rc, updatedResourceDb(T/F).  rc=0 if no error
    def updateVoltagesResourceDbs(self, chassisid, updateStaticProps=False, updateNonVols=True ):
        self.rdr.logMsg("DEBUG","--------BE updateVoltagesResourceDBs. updateStaticProps={}".format(updateStaticProps))
        return (0,False)

    # update PowerControl resourceDB and volatileDict properties
    # returns: rc, updatedResourceDb(T/F).  rc=0 if no error
    def updatePowerControlResourceDbs(self, chassisid, updateStaticProps=False, updateNonVols=True ):
        self.rdr.logMsg("DEBUG","--------BE updatePowerControlResourceDBs. ")
        resDb=self.rdr.root.chassis.powerControlDb[chassisid]
        resVolDb=self.rdr.root.chassis.powerControlVolatileDict[chassisid]
        updatedResourceDb=False
        rc=0     # 0=ok
        return(rc,updatedResourceDb)


    # DO Patch to chassis  PowerControl 
    # the front-end will send an individual call for each property
    def patchPowerControl(self, chassisid, patchData):
        self.rdr.logMsg("DEBUG","--------BACKEND Patch chassis PowerControl data. patchData={}".format(patchData))
        # just call the dbus call to set the prop
        return(0)


   # update PowerSupplies resourceDB and volatileDict properties
    #   updated volatiles:  LineInputVoltage, LastPowerOutputWatts, Status
    # returns: rc, updatedResourceDb(T/F).  rc=0 if no error
    def updatePowerSuppliesResourceDbs(self, chassisid, updateStaticProps=False, updateNonVols=True ):
        self.rdr.logMsg("DEBUG","--------BE updatePowerSuppliesResourceDBs. updateStaticProps={}".format(updateStaticProps))
        resDb=self.rdr.root.chassis.powerSuppliesDb[chassisid]
        resVolDb=self.rdr.root.chassis.powerSuppliesVolatileDict[chassisid]

        return (0,False)

