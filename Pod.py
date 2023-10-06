from PodStatus import PodStatus

class Pod:
    def __init__(self, name, cpuRequest, memoryRequest, diskRequest, containerImage):
        self.name = name
        self.status = PodStatus.Pending
        self.cpuRequest = cpuRequest
        self.memoryRequest = memoryRequest
        self.diskRequest = diskRequest
        self.node = None
        self.containerImage = containerImage

    def runPod(self):
        self
        # Pod running
    
    def podInfo(self):
        if (self.node is not None):
            return f"{self.name} {self.status.value} {self.cpuRequest} {self.memoryRequest}MB {self.diskRequest}MB {self.node.name} {self.containerImage}"
        return f"{self.name} {self.status.value} {self.cpuRequest} {self.memoryRequest}MB {self.diskRequest}MB none {self.containerImage}"