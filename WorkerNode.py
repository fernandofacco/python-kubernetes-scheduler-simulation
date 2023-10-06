from Node import Node
from NodeRole import NodeRole

class WorkerNode(Node):
    def __init__(self, name, maxCpu, maxMemory, maxDisk):
        super().__init__(name, maxCpu, maxMemory, maxDisk)
        self.allocatedPods = []
        self.availableCpu = maxCpu
        self.availableMemory = maxMemory
        self.availableDisk = maxDisk
        self.role = NodeRole.worker
        print("Worker node created")