# Goal:
Generate protobuf files in python and C++ to be used for remote access to RL environment.

**Supported version:**
* protoc 3.13.0
* grpc 1.34.1

# How to use?
- pip install sasrl-env
- In python:
  - from sasrl_env import gymServer
  - gymServer.start('YOUR_PORT_NUMBER')
