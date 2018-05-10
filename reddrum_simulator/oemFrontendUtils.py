
# Copyright Notice:
#    Copyright 2018 Dell, Inc. All rights reserved.
#    License: BSD License.  For full license text see link: https://github.com/RedDrum-Redfish-Project/RedDrum-Frontend/LICENSE.txt

# OEM-specific ID construction and interpretation utilities
# NOTE:
#  in Redfish, it is generally not safe for a client to construct of assume construction of a URI
#  However, the RedDrum fronend interprets some IDs loaded during discovery for some response construction.
#  These OEM utilities contain any special rules re interpreting IDs 

import re

class DellESI_FrontendOemUtils():
    def __init__(self,rdr):
        self.rdr=rdr
        self.isBlockRe=re.compile("^Rack[1-9][0-9]{0,3}-Block([1-9]|10)$")
        self.isPowerBayRe=re.compile("^Rack[1-9][0-9]{0,3}-PowerBay[1-4]$")
        self.subId=re.compile("^(Rack[0-9]{0,4})-*([^-]*)-?(.*)$")

    def getDss9000ChassisSubIds(self, chassid):
        subIds=re.search(self.subId, chassid)
        rack=subIds.group(1)
        chas=subIds.group(2)
        sled=subIds.group(3)
        if chas == "":
            chas = None
        if sled == "":
            sled = None
        return(rack,chas,sled)

    def getAggregator(self, chassid):
        subIds=re.search(self.subId, chassid)
        rack=subIds.group(1)
        chas=subIds.group(2)
        sled=subIds.group(3)
        if chas == "":
            chas = None
        if sled == "":
            sled = None
        return(rack,chas,sled)


    def rsdLocation(self, chassid):
        idRule = self.rdr.backend.rdBeIdConstructionRule
        #   valid rdBeIdConstructionRule values are:  "Monolythic", "Dss9000", "Aggregator"
        if(idRule=="Dss9000"):
            rack,chas,sled=self.getDss9000ChassisSubIds(chassid)
            if chas is None:
                rid=rack
                parent=None
            elif sled is None:
                rid=chas
                parent=rack
            else:
                rid=sled
                parent=chas
            #print("rack: {}, chas: {}, sled: {}".format(rack,chas,sled))
        elif (idRule=="Monolythic"):
            rid=chassid
            parent=None
        elif (idRule=="Aggregator"):
            rid=chassid
            parent=None
            if chassid in self.rdr.root.chassis.chassisDb:
                if "ContainedBy" in self.rdr.root.chassis.chassisDb[chassid]:
                    parent = self.rdr.root.chassis.chassisDb[chassid]["ContainedBy"]
        return( rid, parent)

    def isBlock(self,chassid):
        if re.search(self.isBlockRe, chassid) is not None:
            return True
        else:
            return False

    def isPowerBay(self,chassid):
        if ( re.search(self.isPowerBayRe, chassid)) is not None:
            return True
        else:
            return False
