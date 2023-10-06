from Node import Node
from NodeRole import NodeRole
from PodStatus import PodStatus
import threading

class MasterNode(Node):
    def __init__(self, name, maxCpu, maxMemory, maxDisk, cluster):
        super().__init__(name, maxCpu, maxMemory, maxDisk)
        self.availableCpu = maxCpu
        self.availableMemory = maxMemory
        self.availableDisk = maxDisk
        self.allocatedPods = []
        self.cluster = cluster
        self.role = NodeRole.controlplane
        print("Master node created")

    def initiateScheduler(self):
        self.watchPendingPods()

    def watchPendingPods(self):
        while True:
            pods = self.cluster.pods
            for pod in pods:
                if (pod.status == PodStatus.Pending):
                    try:
                        print(f"\nScheduling pod {pod.name} requests: CPU(cores) {pod.cpuRequest} MEMORY {pod.memoryRequest}MB DISK {pod.diskRequest}MB\n")
                        self.schedulePod(pod)
                    except Exception as error:
                        print(f"Failure scheduling pod {pod.name}: {error}")

    def schedulePod(self, pod):
        nodeScores = []
        print("Selecting best node...")
        while len(nodeScores) == 0:
            nodeScores.clear()
            # Variable to identify if there is atlest one node that has enough maximum resources to run the pod
            podResourcesExceedNodes = True
            for node in self.cluster.nodes:
                if (node.role == NodeRole.worker):
                    # If true, the is atleast one node that has enough maximum resources to run the pod
                    if (self.podRequestDontExceedNodesMaxResources(node, pod)):
                        podResourcesExceedNodes = False

                    if (self.nodeHasEnoughResources(node, pod)):
                        maxCpu = node.maxCpu
                        maxMemory = node.maxMemory
                        maxDisk = node.maxDisk

                        availableCpu = node.availableCpu
                        availableMemory = node.availableMemory
                        availableDisk = node.availableDisk

                        # Calculate the score for the node based on resource availability. High resources availability results in higher score
                        score = ((availableCpu / maxCpu * 0.34) + (availableMemory / maxMemory * 0.33) + (availableDisk / maxDisk * 0.33)) * 100

                        nodeScores.append([node, round(score, 2)])

            if (podResourcesExceedNodes):
                print(f"Failure scheduling pod {pod.name}: pod resource requests exceeds nodes maximum resources.\n")
                pod.status = PodStatus.Failed
                break

            if (len(nodeScores) > 0):
                nodeScores.sort(key=lambda x: x[1], reverse=True)
                self.printWorkerNodesDataWithScore(nodeScores)
            
                bestNode = nodeScores[0][0]
                print(f"Best node {bestNode.name}")

                try:
                    bestNode.allocatePod(pod)
                    thread = threading.Thread
                    print(f"Pod {pod.name} scheduled to node {bestNode.name}")
                except Exception as error:
                    print(f"Error scheduling pod {pod.name} into node {bestNode.name}: {error}\n")

    def podRequestDontExceedNodesMaxResources(self, node, pod):
        if (node.maxCpu >= pod.cpuRequest and node.maxMemory >= pod.memoryRequest and node.maxDisk >= pod.diskRequest):
            return True
        return False

    def nodeHasEnoughResources(self, node, pod):
        if (node.availableCpu < pod.cpuRequest or node.availableMemory < pod.memoryRequest or node.availableDisk < pod.diskRequest):
            return False
        return True
    
    def printWorkerNodesDataWithScore(self, nodeScores):
        nodesInfos = []
        for node in nodeScores:
            nodesInfos.append(f"{node[0].nodeInfo()} {node[1]}")

        spacing = 5

        # Getting highest column widths to print correctly
        name_width = max(len(row.split()[0]) if len(row.split()) >= 1 else 0 for row in nodesInfos) + spacing
        cpu_width = max(len(row.split()[1]) if len(row.split()) >= 2 else 0 for row in nodesInfos) + spacing
        memory_width = max(len(row.split()[2]) if len(row.split()) >= 3 else 0 for row in nodesInfos) + spacing
        memoryPercentage_width = max(len(row.split()[3]) if len(row.split()) >= 4 else 0 for row in nodesInfos) + spacing
        disk_width = max(len(row.split()[4]) if len(row.split()) >= 5 else 0 for row in nodesInfos) + spacing
        diskPercentage_width = max(len(row.split()[5]) if len(row.split()) >= 6 else 0 for row in nodesInfos) + spacing
        role_width = max(len(row.split()[6]) if len(row.split()) >= 7 else 0 for row in nodesInfos) + spacing
        score_width = max(len(row.split()[7]) if len(row.split()) >= 8 else 0 for row in nodesInfos) + spacing

        # Printing header
        print(f"{'NAME':<{name_width}} {'CPU(cores)':<{cpu_width}} {'MEMORY':<{memory_width}} {'MEMORY%':<{memoryPercentage_width}} "
              f"{'DISK':<{disk_width}} {'DISK%':<{diskPercentage_width}} {'ROLE':<{role_width}} SCORE")

        # Printing rows of information of the nodes
        for row in nodesInfos:
            parts = row.split()
            name = parts[0] if len(parts) >= 1 else ""
            cpu = parts[1] if len(parts) >= 2 else ""
            memory = parts[2] if len(parts) >= 3 else ""
            memory_percentage = parts[3] if len(parts) >= 4 else ""
            disk = parts[4] if len(parts) >= 5 else ""
            disk_percentage = parts[5] if len(parts) >= 6 else ""
            role = parts[6] if len(parts) >= 7 else ""
            score = parts[7] if len(parts) >= 8 else ""
            print(f"{name:<{name_width}} {cpu:<{cpu_width}} {memory:<{memory_width}} {memory_percentage:<{memoryPercentage_width}} "
                  f"{disk:<{disk_width}} {disk_percentage:<{diskPercentage_width}} {role:<{role_width}} {score}")
        print()
        