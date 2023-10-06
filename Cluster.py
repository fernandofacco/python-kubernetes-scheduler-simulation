from NodeRole import NodeRole
import threading


class Cluster:
    def __init__(self, name):
        self.name = name
        self.nodes = []
        self.pods = []
        self.hasMaster = False
        print("Cluster created")

    def addNode(self, node):
        self.nodes.append(node)
        print("Node added to cluster")
        # Condition to guarantee that there will be only one master node scheduling
        if (node.role == NodeRole.controlplane and self.hasMaster == False):
            self.hasMaster = True;
            thread = threading.Thread(target=node.initiateScheduler)
            thread.start()
            
    def removeNode(self, node):
        self.nodes.remove(node)

    def addPod(self, pod):
        self.pods.append(pod)

    def printAllNodesData(self):
        nodesInfos = []
        for node in self.nodes:
            nodesInfos.append(f"{node.nodeInfo()}")

        spacing = 5

        # Getting highest column widths to print correctly
        name_width = max(len(row.split()[0]) if len(row.split()) >= 1 else 0 for row in nodesInfos) + spacing
        cpu_width = max(len(row.split()[1]) if len(row.split()) >= 2 else 0 for row in nodesInfos) + spacing
        memory_width = max(len(row.split()[2]) if len(row.split()) >= 3 else 0 for row in nodesInfos) + spacing
        memoryPercentage_width = max(len(row.split()[3]) if len(row.split()) >= 4 else 0 for row in nodesInfos) + spacing
        disk_width = max(len(row.split()[4]) if len(row.split()) >= 5 else 0 for row in nodesInfos) + spacing
        diskPercentage_width = max(len(row.split()[5]) if len(row.split()) >= 6 else 0 for row in nodesInfos) + spacing
        role_width = max(len(row.split()[6]) if len(row.split()) >= 7 else 0 for row in nodesInfos) + spacing

        # Printing header
        print(f"{'NAME':<{name_width}} {'CPU(cores)':<{cpu_width}} {'MEMORY':<{memory_width}} {'MEMORY%':<{memoryPercentage_width}} "
              f"{'DISK':<{disk_width}} {'DISK%':<{diskPercentage_width}} ROLE")

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
            print(f"{name:<{name_width}} {cpu:<{cpu_width}} {memory:<{memory_width}} {memory_percentage:<{memoryPercentage_width}} "
                  f"{disk:<{disk_width}} {disk_percentage:<{diskPercentage_width}} {role}")
        print()

    def printAllPodsData(self, pods):
        podsInfos = []
        for pod in pods:
            podsInfos.append(f"{pod.podInfo()}")

        spacing = 5

        # Getting highest column widths to print correctly
        name_width = max(len(row.split()[0]) if len(row.split()) >= 1 else 0 for row in podsInfos) + spacing
        status_width = max(len(row.split()[1]) if len(row.split()) >= 2 else 0 for row in podsInfos) + spacing
        cpu_width = max(len(row.split()[2]) if len(row.split()) >= 3 else 0 for row in podsInfos) + spacing + 4
        memory_width = max(len(row.split()[3]) if len(row.split()) >= 4 else 0 for row in podsInfos) + spacing
        disk_width = max(len(row.split()[4]) if len(row.split()) >= 5 else 0 for row in podsInfos) + spacing
        nodeName_width = max(len(row.split()[5]) if len(row.split()) >= 6 else 0 for row in podsInfos) + spacing
        containerImage_width = max(len(row.split()[6]) if len(row.split()) >= 7 else 0 for row in podsInfos) + spacing

        # Printing header
        print(f"{'NAME':<{name_width}} {'STATUS':<{status_width}} {'CPU(cores)':<{cpu_width}} {'MEMORY':<{memory_width}} " 
              f"{'DISK':<{disk_width}} {'NODE':<{nodeName_width}} {'CONTAINER-IMAGE':<{containerImage_width}} ")

        # Printing rows of information of the pods
        for row in podsInfos:
            parts = row.split()
            name = parts[0] if len(parts) >= 1 else ""
            status = parts[1] if len(parts) >= 2 else ""
            cpu = parts[2] if len(parts) >= 3 else ""
            memory = parts[3] if len(parts) >= 4 else ""
            disk = parts[4] if len(parts) >= 5 else ""
            nodeName = parts[5] if len(parts) >= 6 else ""
            containerImage = parts[6] if len(parts) >= 7 else ""
            print(f"{name:<{name_width}} {status:<{status_width}} {cpu:<{cpu_width}} {memory:<{memory_width}} " 
                  f"{disk:<{disk_width}} {nodeName:<{nodeName_width}} {containerImage:<{containerImage_width}}")
        print()
    
    def printNodeAllocatedPodsData(self, nodeName):
        foundNode = False
        for node in self.nodes:
            if (nodeName == node.name):
                self.printAllPodsData(node.allocatedPods)
                foundNode = True
                break
        if (not(foundNode)):
            print(f"Error: node with name {nodeName} do not exist.\n")