from PodStatus import PodStatus
import time
import random
import threading

class Node:
    def __init__(self, name, maxCpu, maxMemory, maxDisk):
        self.name = name
        self.maxCpu = maxCpu
        self.maxMemory = maxMemory
        self.maxDisk = maxDisk
        self.availableCpu = maxCpu
        self.availableMemory = maxMemory
        self.availableDisk = maxDisk
        self.allocatedPods = []
        self.role = None

    def allocatePod(self, pod):
        pod.node = self
        self.allocatedPods.append(pod)

        # Update node available resources
        self.availableCpu -= pod.cpuRequest
        self.availableMemory -= pod.memoryRequest
        self.availableDisk -= pod.diskRequest

        # Thread usage to run and update a pod
        thread = threading.Thread(target=self.runPod, args=(pod, ))
        thread.start()

    def runPod(self, pod):
        pod.status = PodStatus.Running
        try:
            pod.runPod()
            minimunLifetime = 10
            maximumLifetime = 20
            randomTime = random.randint(minimunLifetime, maximumLifetime)
            time.sleep(randomTime)

            print(f"\nPod {pod.name} succeeded\n")
            pod.status = PodStatus.Succeeded
        except Exception as error:
            print(f"\nPod {pod.name} failed\n")
            pod.status = PodStatus.Failed

        self.freeResources(pod)

    def freeResources(self, pod):
        # Update node available resources
        self.availableCpu += pod.cpuRequest
        self.availableMemory += pod.memoryRequest
        self.availableDisk += pod.diskRequest

    def nodeInfo(self):
        memoryPercentage = round((self.availableMemory / self.maxMemory) * 100, 2)
        diskPercentage = round((self.availableDisk / self.maxDisk) * 100, 2)
        return (
                f"{self.name} [{self.availableCpu}/{self.maxCpu}] [{self.availableMemory}/{self.maxMemory}MB] {memoryPercentage}% "
                f"[{self.availableDisk}/{self.maxDisk}MB] {diskPercentage}% {self.role.value}"
        )