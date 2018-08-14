
# Copyright Notice:
#    Copyright 2018 Dell, Inc. All rights reserved.
#    License: BSD License.  For full license text see link: https://github.com/RedDrum-Redfish-Project/RedDrum-Simulator/LICENSE.txt

import os
import sys
import json
import inspect

# Backend root class for Simulator
from .chassisBackend   import RdChassisBackend
from .managersBackend  import RdManagersBackend
from .systemsBackend   import RdSystemsBackend

from .simulatorLoadResources  import RdLoadSimulatorStaticResources
from .oemFrontendUtils  import FrontendOemUtils

class RdBackendRoot():
    def __init__(self, rdr):
        # initialize data
        self.version = "0.9"
        self.backendStatus=0
        self.discoveryState=0
        self.oemUtils=FrontendOemUtils(rdr)
        self.rdBeIdConstructionRule=None

        # include properties used by some OEM simulations eg rackNum for DSS9000
        self.rackNum="1"             # the rack number used to calculate IDs eg Rack1-Block1-Sled1  # getSystemsHostList

        # initial states
        self.powerOnState = "On"

        # create backend sub-classes
        self.createSubObjects(rdr)

        # run startup tasks
        self.startup(rdr)


    def createSubObjects(self,rdr):
        #create subObjects that implement backend APIs
        self.chassis=RdChassisBackend(rdr)
        self.managers=RdManagersBackend(rdr)
        self.systems=RdSystemsBackend(rdr)
        self.backendStatus=1
        return(0)

    def startup(self,rdr):
        # set the data paths for standard Linux
        #   if running w/ -L (isLocal) option, the varDataPath is modified from this by Main
        rdSvcPath=os.getcwd()

        # get path to the simulator backend package
        rdr.simulatorPkgPath=os.path.dirname( inspect.getfile(RdBackendRoot))  

        # get the path to frontend data
        #rdr.baseDataPath=os.path.join(rdSvcPath, "reddrum_frontend", "Data")
        rdr.baseDataPath=os.path.join(rdr.frontEndPkgPath, "Data")
        print("EEEEEEEE: baseDataPath: {}".format(rdr.baseDataPath))

        rdr.varDataPath=os.path.join( "/var", "www", "rf"  )
        print("EEEEEEEE: varDataPath: {}".format(rdr.varDataPath))

        # if we have a RedDrum.conf file in /etc/ use it. otherwise use the default
        #rdr.RedDrumConfPath=os.path.join(rdSvcPath, "RedDrum.conf" )
        redDrumConfPathEtc=os.path.join("/etc",  "RedDrum.conf" )
        redDrumConfPathFrontend=os.path.join(rdr.frontEndPkgPath, "RedDrum.conf")
        redDrumConfPathSimulator=os.path.join(rdr.simulatorPkgPath,"RedDrum.conf")
        if os.path.isfile(redDrumConfPathEtc):
            rdr.RedDrumConfPath=redDrumConfPathEtc
        else:
            rdr.RedDrumConfPath=redDrumConfPathSimulator
        print("EEEEEEEE: RedDrumConfPath: {}".format(rdr.RedDrumConfPath))

        # get path to Simulator Static config files
        rdr.staticConfigDataPath=os.path.join(rdr.simulatorPkgPath, "Data")
        print("EEEEEEEE: StaticConfigDataPaths: {}".format(rdr.staticConfigDataPath))

        rdr.schemasPath = os.path.join(rdSvcPath, "schemas") # not used now

        # note that syslog logging is enabled on Simulator by default unless -L (isLocal) option was specified
        # turn-on console messages also however
        rdr.printLogMsgs=True

        # Simulator uses static Resource Discovery pointing at specified profile, and cached database
        # rdr.rdProfile will point to the specified profile.  This is the dir holding static config
        rdr.useCachedDiscoveryDb=True
        rdr.useStaticResourceDiscovery=True

        self.backendStatus=2
        return(0)

    # runStartupDiscovery is called from RedDrumMain once both the backend and frontend resources have been initialized
    #   it will discover resources and then kick-off any hardware monitors in separate threads
    def runStartupDiscovery(self, rdr):
        # For the simulator, Discovery loads the static config defined by rdr.rdProfile into the databases
        rdr.logMsg("INFO"," .... Starting RedDrum Simulator Discovery for Config Profile: {}".format(rdr.rdProfile))

        discvr=RdLoadSimulatorStaticResources(rdr)
        rc=discvr.loadStaticResourceDatabases(rdr)
        if( rc != 0):
            self.discoveryState = 1001 # failed trying to discovery phase1
            rdr.logMsg("CRITICAL"," ****Discovery Initialization Failed rc={}. Exiting ".format(rc))
            sys.exit(9) 
        else:
            self.discoveryState = 1

        # initialize the volatile dicts
        rdr.logMsg("INFO"," .... Initializing Front-end Volatile databases ")

        # initialize the Chassis volatileDicts
        rdr.logMsg("INFO"," ........ initializing Chassis VolatileDicts")
        rdr.root.chassis.initializeChassisVolatileDict(rdr)

        # initialize the Managers volatileDicts
        rdr.logMsg("INFO"," ........ initializing Managers VolatileDicts")
        rdr.root.managers.initializeManagersVolatileDict(rdr)

        # initialize the Systems volatileDict
        rdr.logMsg("INFO"," ........ initializing Systems VolatileDicts")
        rdr.root.systems.initializeSystemsVolatileDict(rdr)


        rc=0
        return(rc)


    # Backend APIs  
    # POST to Backend
    def postBackendApi(self, request, apiId, rdata):
        # handle backend auth based on headers in request
        # handle specific post request based on apiId and rdata
        rc=0
        statusCode=204
        return(rc,statusCode,"","",{})

    # GET from  Backend
    def getBackendApi(self, request, apiId):
        # handle backend auth based on headers in request
        # handle specific post request based on apiId and rdata
        rc=0
        statusCode=200
        resp={}
        jsonResp=(json.dumps(resp,indent=4))
        statusCode=200
        return(rc,statusCode,"",jsonResp,{})


