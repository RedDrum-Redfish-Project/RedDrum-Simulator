
This is the Backend RedDrum implementation for the Simulator backend

The Simulator currently  has minimal backend processing:
  1) to translate Actions (eg power-off) into the appropriaate property statechanges in Chassis and System PowerState
  2) to remember and state changes of resources eg AssetTag, LEDstate, etc

Note that accountService, SessionService, and account settings (eg users, passwords) are fully implemented in the Frontend
     so while the backend has no processing, they operate exactly like a real system

The Simulator relies of choosing a static resource discovery data in the reddrum_simulator/Data directory 
to discovery simulated resources:
    -- This effectively "discovers" the Simlator resources from predefined static files 
       The files are essentially file copies of the database Cache that the RedDrum-Frontend keeps when it wants to start
         and reload its old resource cache instead of re-discovering everything.
    -- Note that the RedDrum-Frontend is configured to restart from cache, 
       The files under /Data are the default configs  if no cache exists.
       So the data is persistent--if you change users data, it persists re-starting the simulator

    -- to clear the caches, go to RedDrum-Simulator/Scripts, and run ./clearCaches


