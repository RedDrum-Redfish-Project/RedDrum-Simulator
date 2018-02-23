# RedDrum-Simulator  
A "high-fidelity" Redfish Service Simulation with https and authentication for various feature profiles and server configurations.

## About ***RedDrum-Simulator***

***RedDrum-Simulator*** is a python app that leverages the RedDrum-Frontend and implements a full feature Simulation of a Redfish Service for various SPMF Feature profiles and  and server configurations.

As a RedDrum Redfish Service implementation, the Frontend is implemented by RedDrum-Frontend.
* see RedDrum-Frontend/README.md and RedDrum-Frontend/reddrum_frontend/README.txt for details

The Simulator Backend  is implemented as a package from this  repo -- named **reddrum_Simulator**

The RedDrum-Simulator/***RedDrumMain.py*** startup script (also in scripts dir) implements the calls to the frontend
and backend to start-up the service.

## Currently Supported Simulator "Profiles" or "configurations":
The initial release includes the following Configurations:
* BaseServer1 - a simple monolythic server implementing the OCP Base Server profile
* Dss9000-4nodes - a 4-node Redfish simulation of the Dell DSS9000 Rackmanager (with only 4 nodes) as a multi-node Redfish example


## About the ***RedDrum Redfish Project***
The ***RedDrum Redfish Project*** includes several github repos for implementing python Redfish servers.
* RedDrum-Frontend  -- the Redfish Service Frontend that implements the Redfish protocol and common service APIs
* RedDrum-Httpd-Configs -- docs and setup scripts to integrate RedDrum with common httpd servers eg Apache and NGNX
* RedDrum-Simulator -- a "high-fidelity" simulator built on RedDrum with several feature profiles and server configs
* RedDrum-OpenBMC -- a RedDrum Redfish service integrated with the OpenBMC platform

## Architecture 
RedDrum Redfish Service Architecture breaks the Redfish service into three parts:
* A standard httpd service
  * The RedDrum-Simulator uses an Apache httpd to implement a reverse proxy to the RedDrum-Frontend
  * A virtual server is defined for both http(port 80) and https(port 443) 
  * The Reverse Proxy Config directs Apache to reverse-proxy all incoming http[s] requests having URIs starting with `/redfish` reverse proxied" to the RedDrum-Frontend using http
  * the RedDrum-Frontend listens on http:<127.0.0.1:5001> (localhost port 5001 http) and only processes defined URIs
  * SSL is handled by Apache and reverse proxied over to the RedDrum-Frontend as an internal http connection
    * this architecture allows other http services to use the same standard http ports
    * SEE RedDrum-Redfish-Project/RedDrum-Httpd-Config  Repo for description of how to configure Apache 
    * a script is included that will create the needed httpd.conf file and create a self-signed https certificate
  * other httpd interfaces could be used but are not currently supported by RedDrum Simulator code
  * As explained in the RedDrum-Httpd-Configs README, for testing w/o HTTPS, the builting Web server in the Frontend can be 
started at any IP address and port but would not support https

* The RedDrum-Frontend -- profies implementation independent frontend code in RedDrum-Frontend 
  * All authentication is implemented by the Frontend
  * The Redfish protocol is implemented by the Frontend -- along with the AccountService, SessionService, rootService,
and top-level APIs for JsonSchemas, Registries, odata, and $metadata
  * the frontend is single threaded but blazing fast since much of the data is cached in the frontend dictionaries

* The RedDrum-Backend -- implements implementation-depended interfaces to the real hardware resources
  * The full Backend code for the RedDrum-Simulator is included in this repo

* `redDrum[Simulator]Main.py` Startup Script -- used to start the service.  uses APIs to the Frontend and Backend to initialize Resource,
initiate HW resource discovery, and Startup the Frontend Flask app.
  * the RedDrum-Simulator/redDrumSimulatorMain.py does this for the Simulator
  * the `--Profile=<profile>` option is used to specify the simulator ***Profile*** (or configuration) to simulate:
    * initial profiles are BaseServer1 and Dss9000-4nodes

## Conformance Testing
Re-running of SPMF conformance tests is currently in progress.
(earlier versions  of the Simulator and conformance tests passed--but did not include the Profile Conformance Test)
* List of DMTF/SPMF Conformance tools being used:
  * Mockup-Creator
  * Service-Validator
  * JsonSchema-Response-Validator
  * Conformance-Check
  * (new) Ocp Base Server Profile Tester

* RedDrum-specific tests (not yet open sourced)
  * RedDrum-URI-Tester -- tests against all supported URIs for specific simulator profiles
  * RedDrum-Stress-Tester -- runs 1000s of simultaneous requests in parallel

---
## How to Install and run the RedDrum-Simulator 


#### Install Centos and httpd (for https reverse proxy)

```
 1. Install Centos 7.1 or later linux OS
      -- a minimum install works, but you probably want the knome desktop
      -- then yum install python3.4 or python3.5

 2. Install httpd, generate ssl cert, and configure to create a reverse proxy
     yum install httpd
     cd  <your_path_to_Directory_Holding_RedDrumSimulator_code>
     git clone https://github.com RedDrum-Redfish-Project/RedDrum-Httpd-Configs    # creates ./RedDrum-Httpd-Configs
     cd RedDrum-Httpd-Configs/Apache-ReverseProxy
     ./subSystem_config.sh # creates a httpd.conf file in etc/httpd and creates self-signed ssl certificates

 3. Start httpd:
     systemctl enable httpd   # httpd will auto-start now any time the server reboots
     systemctl restart httpd  # start it up now

```

#### Manual Install of RedDrum-Frontend and RedDrum-Simulator using git clone 

```
     # create a directory to install editable RedDRum repos
     mkdir  <your_path_to_Directory_Holding_RedDrumSimulator_code>
     cd  <your_path_to_Directory_Holding_RedDrumSimulator_code>

     # git clone the RedDrum-Frontend code and install
     git clone https://github.com/RedDrum-Redfish-Project/RedDrum-Frontend  #creates ./RedDrum-Frontend
     # install to site-packages as editable package
     pip install -e ./RedDrum-Frontend

     # git clone the RedDrum-Simulator code and install
     git clone https://github.com/RedDrum-Redfish-Project/RedDrum-Simulator  #creates ./RedDrum-Simulator
     pip install -e ./RedDrum-Simulator

```

#### Normal install `pip install` from github 

```
     # create a directory to install editable RedDRum repos
     mkdir  <your_path_to_Directory_Holding_RedDrumSimulator_code>
     cd  <your_path_to_Directory_Holding_RedDrumSimulator_code>

     # pip install Frontend into site-packages
     pip install git+https://github.com/RedDrum-Redfish-Project/RedDrum-Frontend.git   # gets latest code in master

     # pip install RedDrum-Simulator into site-packages
     pip install git+https://github.com/RedDrum-Redfish-Project/RedDrum-Simulator.git  # gets latest code in master

```

#### Install using `pip install` from pypi (not working yet)
* RedDrum-Frontend and RedDrum-Simulator are not in pypi system yet


## STARTING  the RedDrum-Simulator
#### Starting RedDrum-Simulator --if you cloned editable RedDrum repos

```
     cd  <your_path_to_Directory_Holding_RedDrumSimulator_code>
     cd RedDrum-Simulator/scripts
     su root     # the simulator will try to store files in /var/www/... so it needs to run as root
     <enter password>

     # start the simulator using runSimulator script
     # ./runSimulator <profile>  where <profile>= oneOf: BaseServer1, Dss9000-4nodes
     ./runSimulator BaseServer1  # to run the Ocp Base Server Profile for a simple monalythic server
       --or--
     ./runSimulator Dss9000-4nodes  # to run the simulation of  a Dell ESS9000 rack-level redfish service w/ 4 nodes present

     # to stop the simulator, hit control-C

     # to clear data caches so that any changes you made to the resources (like users) is deleted:
     ./clearCaches
```
#### 
#### Starting RedDrum-Simulator --if you installed with pip install from github or pypi

```
     su root     # the simulator will try to store files in /var/www/... so it needs to run as root
     <enter password>

     # from any directory
     #redDrumSimulatorMain [--Target=<target>]  $ where <target> = oneof: BaseServer1(default) or Dss9000-4nodes
     redDrumSimulatorMain  # default is BaseServer1

     # to stop the simulator, hit control-C

     # to clear data caches so that any changes you made to the resources (like users) is deleted:
     cd /var/www
     rm -R -f rf
```

### How to Clear Data Caches
The Simulator Frontend keeps resource data for non-volatile resource models cached in files, so if you add/delete users, change passwords, set AssetTags, etc, the changes will persist stopping and re-starting the simulator
* To clear all data caches to defaults and also clear python caches, run:

```
     su root     # the simulator will try to store files in /var/www/... so it needs to run as root
     cd  <your_path_to_Directory_Holding_RedDrumSimulator_code>/RedDrum-Simulator/scripts
     ./clearCaches
```

* To clear data caches to defaults if you installed the packages directly to sitepackages

```
     su root     
     cd /var/www
```

---
