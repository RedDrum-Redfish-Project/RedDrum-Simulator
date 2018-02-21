
# Copyright Notice:
#    Copyright 2018 Dell, Inc. All rights reserved.
#    License: BSD License.  For full license text see link: https://github.com/RedDrum-Redfish-Project/RedDrum-Simulator/LICENSE.txt

# BullRed-RackManager managersBackend resources
#
class  RdManagersBackend():
    # class for backend managers resource APIs
    def __init__(self,rdr):
        self.version=1
        self.rdr=rdr


    # update resourceDB and volatileDict properties
    def updateResourceDbs(self,managerid, updateStaticProps=False, updateNonVols=True ):
        self.rdr.logMsg("DEBUG","--------BACKEND updateResourceDBs. updateStaticProps={}".format(updateStaticProps))

        # the simulator backend does not update database after discovery, so we can return 0 False here
        return(0,False)


    # DO action:  "Reset", "action
    def doManagerReset(self,managerid,resetType):
        self.rdr.logMsg("DEBUG","--------BACKEND managerReset. resetType={}".format(resetType))

        rc=0
        return(rc)


    # DO Patch to Manager  (DateTime, DateTimeOffset)
    def doPatch(self, managerid, patchData):
        # the front-end has already validated that the patchData and managerid is ok
        # so just send the request here
        self. rdr.logMsg("DEBUG","--------BACKEND Patch manager: {} data. patchData={}".format(managerid,patchData))
        rc=0
        return(rc)

    # update NetworkProtocolsDb Info
    def updateManagerNetworkProtocolsDbFromBackend(self, mgrid, noCache=False):
        return(0)

    # update EthernetInterface Info
    def updateManagerEthernetEnterfacesDbFromBackend(self, mgrid, noCache=False, ethid=None):
        return(0)



