Reality Mismatch Labs Gateway
=============================

The Labs Gateway project is stored in the following repository:
https://github.com/ElChicoDePython/RealityMismatch-LabsGateway


The Labs GW is an API used by RealityMismatch for creating
and destroying laboratories.

The labs API GW should serve as an abstraction between infrastructure
deployments and RealityMismatch game. This will receive
labs requests and will response with labs access data.

Installation of levels
----------------------

When a level gets installed the labs gw should be notified if the
level has any kind of lab deployment requirements.

This requirements are going to be specified inside the `manifest.json`
file of the level with a structure that has to be defined.

Once the API receive the new level installation should prepare
internally resources for it.

The relationship between containers, machines, networks, etc. should
be specified inside the `manifest.json` with a SDL to be defined.

Labs requests
-------------

To be defined.

Labs removals
-------------

There should be a way to cleanup labs of a level if this its
uninstalled from the system.