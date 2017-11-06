
#Importing Standard Liberaries

import csv
import sys
import os
import os.path
import heapq

#Printing Options to Select From.

print("\n**************************************************************************************************************************************")
print(" < CS542 Link State Routing Simulator >")
print("**************************************************************************************************************************************\n")
print("Select one of the options given below:\n")
print("(1) Create a Network Topology")
print("(2) Build a Connection Table")
print("(3) Shortest Path to Destination Router")
print("(4) Modify a Topology")
print("(5) Best Router for Broadcast")
print("(6) Exit\n")
print("**************************************************************************************************************************************")
print("**************************************************************************************************************************************\n")

#Initialization of the variables.

graph = []
cost_dict = {}
vertex = []
link_interface = {}
path = []

#Class for Implementing Switch Cases.

class switch(object):
    command = None

    def __new__(prompt, command):
        prompt.command = command
        return True

def case(*choice):
    return any((option == switch.command for option in choice))

#Implementing Dijkstra's Algorithm to find the Shortest Path and Distance from Source to Destination Router.

def dijkstra(start):
    global cost_dict
    global unSeen
    global prevNode
    global seenNode
    global link_interface

    unSeen = {v: float('inf') for v in vertex}
    seenNode = {}
    prevNode = {}
    currentNode = start
    currentDistance = 0
    link_interface = {v: [] for v in vertex}
    unSeen[currentNode] = currentDistance


    while len(unSeen) > 0:

        for nextN, cost in cost_dict[currentNode].items():

            if nextN not in unSeen:
                continue
            newDistance = currentDistance + cost
            if newDistance < unSeen.get(nextN, float('inf')):

                unSeen[nextN] = newDistance
                prevNode[nextN] = currentNode

                if not link_interface[currentNode]:
                    link_interface[nextN] = [nextN]
                else:
                    link_interface[nextN] = list(link_interface[currentNode])
        seenNode[currentNode] = currentDistance

        del unSeen[currentNode]
        if not unSeen:
            break
        currentStatus = [v for v in unSeen.items() if v[1]]
        currentNode, currentDistance = sorted(currentStatus, key=lambda x: x[1])[0]

#Checking whether user command is valid or not!.

while True:
  try:
     n = int(input("Enter Command: \n"))
  except ValueError:
     print("Not an integer! Please enter between option 1 to 6")
     continue
  else:
     break

if n != 1:
    print("First Import input File by Choosing option 1")
    while True:
        try:
            n = int(input("Enter Command: \n"))
        except ValueError:
            print("Not an integer! Please enter option 1")
            continue
        else:
            break

#Implementing switch case to select the given options.

while switch(n):

    # Case 1 to process the input file.

    if case(1):
        print("\nInput original network topology matrix data file in (.txt) format:\n")

        file = input()

        graph = []
        cost_dict = {}
        vertex = []

        #checking whether the file is valid or not.

        if (not file.endswith('.txt')):
            print("Invalid file format")
            continue

        #checking whether the file is present or not.

        elif not os.path.isfile(file):
            print("File not Found")
            continue

        #checking whether the file is empty or not.

        elif os.stat(file).st_size == 0:
            print("File is empty")
            continue

        #Printing the topology file



        else:
            print("\nReview Original Topology Matrix")
            print("===============================================================================================================")
            with open(file) as net_topo:
                graph = [list(map(int, x.split())) for x in net_topo]

            for line in graph:
                for item in line:
                    print(item, end='    ')
                print()
            print("===============================================================================================================")

            total_nodes = len(graph)
            print("\nTotal number of nodes present: ", total_nodes)

            #Creating Graph dictionary

            for i in range(total_nodes):

                matrix = {}
                for j in range(total_nodes):

                    if i != j and graph[i][j] != -1:
                        matrix[j + 1] = graph[i][j]

                cost_dict[i + 1] = matrix
                vertex.append(i + 1)

            print("\nFinal Graph dictionary - ", cost_dict)

        print("\n**************************************************************************************************************************************")

        print("**************************************************************************************************************************************")

        # Checking Whether user command is valid or not!.

        while True:
            try:
                n = int(input("Enter Command: \n"))
            except ValueError:
                print("Not an integer! Please enter between option 1 to 6")
                continue
            else:
                break

        if n != 2 and n != 6:
            print("Please enter Option 2 to select Source router first or Option 6 to Exit")
            while True:
                try:
                    n = int(input("Enter Command: \n"))
                except ValueError:
                    print("Not an integer! Please enter option 3 or 6")
                    continue
                else:
                    break
        switch(n)

    #Case 2 to Find and printing Connection router of Source Router

    if case(2):
        print("\nSelect a source router:")

        #Checking whether the Source router is valid or not.

        while True:
            try:
                start = int(input())
            except ValueError:
                print("Not an integer! Please enter a valid router ID")
                continue
            else:
                break


        if  start < 1 or start > len(cost_dict) :
            print("Enter valid router")
            continue


        dijkstra(start)
        print("\nRouter %s Connection Table:"%start)
        print("==========================")
        print("Destination\tInterface")
        print("==========================")
        for key in link_interface:
            print("\t",key, "\t\t", link_interface[key])
        print("==========================")

        print("\n**************************************************************************************************************************************")

        print("**************************************************************************************************************************************")

        # Checking Whether user command is valid or not!.

        while True:
            try:
                n = int(input("Enter Command: \n"))
            except ValueError:
                print("Not an integer! Please enter between option 1 to 6")
                continue
            else:
                break

        if n != 3 and n != 6:
            print("Please enter Option 3 to select Destination router first or Option 6 to Exit")
            while True:
                try:
                    n = int(input("Enter Command: \n"))
                except ValueError:
                    print("Not an integer! Please enter between option 3")
                    continue
                else:
                    break

        switch(n)

    #Case 3 to Find the Shortest path and distance between Source and destination router

    if case(3):
        print("\nSelect the destination router:")

        # Checking whether the Destination router is valid or not.

        while True:
            try:
                destination = int(input())
            except ValueError:
                print("Not an integer! Please enter a valid router ID")
                continue
            else:
                break

        if  destination < 1 or destination > len(cost_dict) :
            print("Enter valid router")
            continue

        elif destination == start:
            print("Source and Destinaton Routers are Same")
            continue

        destination1 = destination

        print("\nMinimum Cost from %s to %s is %s" % (start, destination, seenNode[destination]))

        #Printing Shortest Path

        path = []
        while 1:

            path.append(destination)
            if destination == start:
                break
            destination = prevNode[destination]

        path.reverse()

        destination = destination1
        print("\nShortest Path from %s to %s is %s"%(start,destination,path))

        print("\n**************************************************************************************************************************************")
        print("**************************************************************************************************************************************")

        # Checking Whether user command is valid or not!.

        while True:
            try:
                n = int(input("Enter Command:\n 4 for modification: \n 5 for Best Router: \n"))
            except ValueError:
                print("Not an integer! Please enter between option 1 to 6")
                continue
            else:
                break
        if n != 4 and n != 5 and n != 6:
            print("Please enter Option 4 to modify, 5 for best router or Option 6 to Exit")
            while True:
                try:
                    n = int(input("Enter Command: \n"))
                except ValueError:
                    print("Not an integer! Please enter option 4, 5 or 6")
                    continue
                else:
                    break

        switch(n)

    #Case 4 to update the router if a router goes down

    if case(4):

        global unSeen

        print("\nSelect a Router to be Removed:")

        # Checking whether the router is valid or not.

        while True:
            try:
                down_router = int(input())
            except ValueError:
                print("Not an integer! Please enter a valid router ID")
                continue
            else:
                break

        if down_router < 1 or down_router > len(cost_dict):
            print("Enter valid Router")
            continue

        #Creating new Graph dictionary to process

        z = down_router - 1

        for i in range(total_nodes):

            matrix = {}
            for j in range(total_nodes):

                if i != j != z and i != j and graph[i][j] != -1:
                    matrix[j + 1] = graph[i][j]

            cost_dict[i + 1] = matrix


        del cost_dict[down_router]
        del vertex[z]

        #print("\nUpdated Graph Dictionary:",cost_dict)

        if down_router == start:
            start = int(input("Enter new start node\n"))

        dijkstra(start)

        #Updated Connection Table

        print("\nRouter %s Connection Table:" % start)
        print("==========================")
        print("Destination\tInterface")
        print("==========================")

        for key in link_interface:
            print("\t",key, "\t\t", link_interface[key])

        print("==========================\n")

        #Updated Path

        path = []
        destination2 = destination

        if down_router == destination:
            destination = int(input("Please enter new destination router"))
            destination2 = destination

        while 1:

            path.append(destination)

            if destination == start:
                break
            destination = prevNode[destination]

        path.reverse()
        destination = destination2
        print("Updated Shortest Path is:",path)
        print("Updated shortest distance",seenNode[destination])

        h = []
        for k,v in cost_dict.items():
            h.append(k)


        print("\n**************************************************************************************************************************************")
        print("**************************************************************************************************************************************")

        # Checking Whether user command is valid or not!.

        while True:
            try:
                n = int(input("Enter Command: \n"))
            except ValueError:
                print("Not an integer! Please enter between option 1 to 6")
                continue
            else:
                break

        if n != 5 and n != 6:
            print("Please enter Option 5 for best router or Option 6 to Exit")
            while True:
                try:
                    n = int(input("Enter Command: \n"))
                except ValueError:
                    print("Not an integer! Please enter option 5 or 6")
                    continue
                else:
                    break

        switch(n)

    #Case 5 to Find the Best Router having lowest cost to every other routers

    if case(5):

        lst = []
        lt = []

        print("\nSelect one of the options:\n")
        print("1 - If Topology not Updated: Best Router for original Graph")
        print("2 - If Topology updated: Best Router for updated Graph")

        while True:
            try:
                quest = int(input())
            except ValueError:
                print("Not an integer! Please enter a valid router ID")
                continue
            else:
                break

        if quest < 1 or quest > 2:

            print("Please choose either option 1 or option 2")
            continue


        print("\n==========================")
        print("Vertex\tTotal_Cost")
        print("==========================")

        #To find Best router for original graph

        if int(quest) == 1:

            for f in range(total_nodes):

                dijkstra(f + 1)
                l = 0
                for k, v in seenNode.items():
                    l = l + v
                print("\t",f + 1,"\t\t", l)

                lst.append(l)

            u = min(lst)
            v = lst.index(u)
            print("==========================")
            print("\nBest Router is %s with lowest cost %s" % (v + 1, u))

        #To find Best router for updated graph

        elif int(quest) == 2:

            for f in h:

                dijkstra(f)
                l = 0
                for k,v in seenNode.items():

                    l = l + v

                print("\t",f,"\t\t",l)

                lst.append(l)

                lt.append(f)


            u = min(lst)
            v = lst.index(u)
            t = lt[v]

            print("==========================")

            print("\nBest Router is %s with lowest cost %s"%(t,u))

        # Checking Whether user command is valid or not!.

        while True:
            try:
                n = int(input("Enter Command 6 to Exit: \n"))
            except ValueError:
                print("Not an integer! Please enter between option 1 to 6")
                continue
            else:
                break
        switch(n)

    #Case 6 to Exit the program

    if case(6):
        print("\nExit CS542-04 2016 Fall project. Good Bye!")
        break

    print("\nINVALID COMMAND. EXITING")
    break

