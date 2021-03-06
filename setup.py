from setuptools import setup

setup(name='RedDrum-Simulator',
      version='0.9.5',
      description='A python simulator of a Redfish Service for various server configurations and feature profiles',
      author='RedDrum-Redfish-Project / Paul Vancil, Dell ESI',
      author_email='redDrumRedfishProject@gmail.com',
      license='BSD License',
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3.4',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: Libraries :: Embedded Systems',
          'Topic :: Communications'
      ],
      keywords='Redfish RedDrum SPMF OpenBMC ',
      url='https://github.com/RedDrum-Redfish-Project/RedDrum-Simulator',
      download_url='https://github.com/RedDrum-Redfish-Project/RedDrum-Simulator/archive/0.9.5.tar.gz',
      packages=['reddrum_simulator'],
      scripts=['scripts/redDrumSimulatorMain'],
      install_requires=[
          'RedDrum-Frontend==0.9.5', # the common RedDrum Frontend code that has dependency on Flask
          'passlib==1.7.1',          # used by Frontend
          'Flask',                   # used by Frontend
          'pytz'                     # used by Frontend
      ],
      include_package_data = True,
      package_data={'reddrum_simulator': [
        'RedDrum.conf',
        'Data/BaseServer1/chassisDb/*.json', 'Data/BaseServer1/managersDb/*.json', 'Data/BaseServer1/systemsDb/*.json',
        'Data/Dss9000-4nodes/chassisDb/*.json', 'Data/Dss9000-4nodes/managersDb/*.json', 'Data/Dss9000-4nodes/systemsDb/*.json'
        ]}
)
