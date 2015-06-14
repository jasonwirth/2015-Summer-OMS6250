# Assignment 3 for OMS6250
#
# This defines a Node that can fun the Bellman-Ford algorithm. The TODOs are
# all related to implementing BF. Also defines a Topology, which is a collection
# of Nodes.
#
# Copyright 2015 Sean Donovan

from helpers import *
import pdb

class Node(object):
    #TODO: You need to have a structure that contains current distances

    def __init__(self, name, topolink, neighbors):
    # name is the name of the local node
    # links is a list of all neighbors's names. 
    # topology is a backlink to the Topology class. Used for accessing neighbors
    #   as follows: self.topology.topodict['A']
    # messages is a list of pending messages from neighbors to be processed.
    #   The format of the message is up to you; a tuple will work.
        self.name = name
        self.links = neighbors
        self.topology = topolink
        self.messages = []
        #TODO? You may need to initialize your distance data structure
        self.distance_table = {name: 0}
        neighbor_distances = {n: 1 for n in neighbors}
        self.distance_table.update(neighbor_distances) 

    def __len__(self):
        ''' Returns the length of the message queue. '''
        return len(self.messages)

    def __str__(self):
        ''' Returns a string representation of the node. '''
        #TODO? You may want to edit this with your distance info.
        distance_info = sorted([node + str(dist) for node, dist in self.distance_table.items()])
        distance_info = ','.join(distance_info)
        return '{0}:{1}'.format(self.name, distance_info)

    def __repr__(self):
        return self.__str__()

    def verify_neighbors(self):
        ''' Verify that all your neighbors has a backlink to you. '''
        for neighbor in self.links:
            if self.name not in self.topology.topodict[neighbor].links:
                raise Exception(neighbor + " does not have link to " + self.name)

    def send_msg(self, msg, dest):
        ''' Performs the send operation, after verifying that the neighber is
            valid.
        '''
        if dest not in self.links:
            raise Exception("Neighbor " + dest + " not part of neighbors of " + self.name)
        self.topology.topodict[dest].queue_msg(msg)

    def queue_msg(self, msg):
        ''' Allows neighbors running Bellman-Ford to send you a message, to be
            processed next time through self.process_BF(). '''
        self.messages.append(msg.copy())

    def process_BF(self):
        # TODO: The Bellman-Ford algorithm needs to be implemented here.
        # 1. Process queued messages
        # 2. Send neighbors updated distances

        # Process queue:
        print '===================================='
        print "Node {0} is processing messages".format(self.name)
        print "Current distance table:{0}".format(self.distance_table)
        send_updates = False
        for msg in self.messages:
            # TODO: Do something
            # pdb.set_trace()
            msg.pop(self.name)
            # Who is the message from?
            sender, dist = [(node, dist) for node, dist in msg.items() if dist == 0][0]
            msg.pop(sender)
            # This message is from a neighbor node, which by definition is 1-unit away. 
            # we could get variable distances by doing self.distance_table[sender]
            assert self.distance_table[sender] == 1
            # msg = {node: dist + 1 for node, dist in msg}
            for node in msg:
                msg[node] += 1

            print '------------------------'
            print "{1} message: {0}".format(msg, sender)
            for node, distance in msg.items():
                current_dist = self.distance_table.get(node, float('inf'))
                print "{sender}->{node}:{distance}, {self.name}->{node}:{current_dist}".format(**locals())
                if distance < current_dist:
                    print "Updating to use node {0}:{1}".format(node, distance)
                    send_updates = True
                    self.distance_table[node] = distance
                else:
                    print 'Current distance is shorter'

        # Empty queue
        self.messages = []

        # Send neighbors udpated distances:
        if send_updates:
            for neighbor in self.links:
                # self.distance_table
                print "sending {0} updated distance table: {1}".format(neighbor, self.distance_table)
                self.send_msg(self.distance_table, neighbor)

    def log_distances(self):
        ''' Prints distances in the following format (no whitespace either end):
        A:A0,B1,C2
        A is the node were on,
        B is the neighbor, 1 is it's distance
        A0 shows that the distance to self is 0
        Taken from topo1.py
        '''
        # TODO: The string in the format above (no newlines, no whitepsace) must
        # be defined. THen log with write_entry, example below.
        logstring = str(self)
        write_entry(logstring)


class Topology(object):

    def __init__(self, conf_file):
        ''' Initializes the topology. Called from outside of Node.py '''
        self.topodict = {}
        self.nodes = []
        self.topo_from_conf_file(conf_file)
    
    def topo_from_conf_file(self, conf_file):
        ''' This created all the nodes in the Topology  from the configuration
            file passed into __init__(). Can throw an exception if there is a
            problem with the config file. '''
        try:
            conf = __import__(conf_file)
            for key in conf.topo.keys():
                new_node = Node(key, self, conf.topo[key])
                self.nodes.append(new_node)
                self.topodict[key] = new_node
                
        except:
            print "error importing conf_file" + conf_file
            raise

        self.verify_topo()

    def verify_topo(self):
        ''' Once the topology is imported, we verify the topology to make sure
            it is actually valid. '''
        print self.topodict

        for node in self.nodes:
            try:
                node.verify_neighbors()
            except:
                print "error with neighbors of " + node.name
                raise

    def run_topo(self):
        ''' This is where most of the action happens. First, we have to "prime 
        the pump" and send to each neighbor that they are connected. 

        Next, in a loop, we go through all of the nodes in the topology running
        their instances of Bellman-Ford, passing and receiving messages, until 
        there are no further messages to service. Each loop, print out the 
        distances after the loop instance. After the full loop, check to see if 
        we're finished (all queues are empty).
        '''
        #Prime the pump
        for node in self.nodes:
            for neighbor in node.links:
                # TODO - Build message
                msg = node.distance_table
                print "Node {0} sending message to neighbor {1}".format(node.name, neighbor)
                # pdb.set_trace()
                # Send message to neighbor
                node.send_msg(msg, neighbor)

        done = False
        while done == False:
            for node in self.nodes:
                node.process_BF()
                node.log_distances()
            
            # Log a break.
            next_entry()

            done = True
            for node in self.nodes:
                if len(node) != 0:
                    done = False
                    break


    

