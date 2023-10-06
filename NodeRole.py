from enum import Enum

class NodeRole(Enum):
    controlplane = "control-plane"
    worker = "worker"
