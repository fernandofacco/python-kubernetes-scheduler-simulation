from Cluster import Cluster
from MasterNode import MasterNode
from WorkerNode import WorkerNode
from Pod import Pod
import random
import time

def addMultiplePods (quant, cluster):
    podNamesAdjectives = ["Red", "Green", "Blue", "Yellow", "Purple", "Orange", "Crimson", "Azure"]
    podNames = ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliet", "Kilo", "Lima", "Mike", "November", "Oscar", "Papa", "Quebec", 
                 "Romeo", "Sierra", "Tango", "Uniform", "Victor", "Whiskey", "Xray", "Yankee", "Zulu", "Aurora", "Orion", "Cassiopeia", "Lyra", "Pegasus", "Sirius", "Gemini", 
                 "Leo", "Scorpio", "Aquarius", "Capricorn", "Libra", "Virgo", "Aries"]
    for i in range(quant):
        name = f"{random.choice(podNamesAdjectives)}{random.choice(podNames)}"
        cpuRequest = random.randint(1, 2)
        memoryRequest = random.randint(100, 1500)
        diskRequest = random.randint(100, 4000)
        containerImage = random.choice(["ubuntu", "debian", "alpine", "centos", "nginx", "httpd", "mysql", "postgres", "redis", "mongo", "node", "python", "golang", "ruby", "php"])

        pod = Pod(name, cpuRequest, memoryRequest, diskRequest, containerImage)
        cluster.addPod(pod)

if __name__ == "__main__":
    print("\nAvailable commands: get nodes | get pods | add pod | get [NODE-NAME] pods\n")
    time.sleep(2)

    cluster = Cluster("Cluster Teste")
    master = MasterNode("Master", 8, 4000, 10000, cluster)
    cluster.addNode(master)
    worker1 = WorkerNode("Worker1", 4, 2000, 5000)
    cluster.addNode(worker1)
    worker2 = WorkerNode("Worker2", 4, 2000, 5000)
    cluster.addNode(worker2)
    addMultiplePods(40, cluster)

    while True:
        userInput = input()
        if (userInput == "get nodes"):
            cluster.printAllNodesData()
        elif (userInput == "get pods"):
            cluster.printAllPodsData(cluster.pods)
        elif (userInput == "add pod"):
            userInput = input("Enter pod name, cpu(core), memory(MB) and disk(MB) requests and container image: ")
            podData = userInput.split()
            if len(podData) == 5:
                podName = podData[0]
                podCpu = int(podData[1])
                podMemory = float(podData[2])
                podDisk = float(podData[3])
                podCImage = podData[4]

                cluster.addPod(Pod(podName, podCpu, podMemory, podDisk, podCImage))
            else:
                print("Invalid input... Expected input: [NAME] [CPU] [MEMORY] [DISK] [CONTAINER-IMAGE]")
        else:
            userInputSplit = userInput.split()
            if (userInputSplit[0] == "get" and userInputSplit[2] == "pods" and len(userInputSplit) == 3):
                cluster.printNodeAllocatedPodsData(userInputSplit[1])
            else:
                print("Invalid input... Available commands: get nodes | get pods | add pod | get [NODE-NAME] pods\n")

