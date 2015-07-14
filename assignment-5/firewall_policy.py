#!/usr/bin/python

"Assignment 5 - This creates the firewall policy. "

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pprint import pprint as pp

def make_firewall_policy(config):
    # TODO - This is where you need to write the functionality to create the
    # firewall. What is passed in is a list of rules that you must implement
    # using the Pyretic syntax that was used in Assignment 2. 

    # feel free to remove the following "print config" line once you no longer need it
    print '============== PRINTING CONFIG ==============='
    pp(config) # for demonstration purposes only, so you can see the format of the config
    print '============== PRINTING CONFIG DONE ==============='
    rules = []
     # {'dstip': '*',
     #  'dstmac': '*',
     #  'dstport': '*',
     #  'rulenum': '2',
     #  'srcip': '*',
     #  'srcmac': '*',
     #  'srcport': '1080'}]

    def convert(entry):
        print 'rule num', entry.pop('rulenum')
        entry = {k:v for k, v in entry.items() if not v == '*'}
        mappings = {EthAddr: ['srcmac', 'dstmac'], 
                    int: ['srcport', 'dstport'],
                    IPAddr: ['srcip', 'dstip']}
        for f, props in mappings.items():
            for p in props:
                try:
                    entry[p] = f(entry[p])
                except:
                    # print '{0} not in entry:{1}'.format(p, entry)
                    pass
        
        entry.update({'ethtype':0x0800, 'protocol':6})

        return entry

    for i, entry in enumerate(config):
        # TODO - build the individual rules
        entry = convert(entry)
        pp('============== CONFIG {0} ==============='.format(i))
        pp(entry)
        rule = match(**entry)

        # examples: 
        # rule = match(dstport=entry['dstport']) 
        # rule = match(srcmac=MAC(entry['srcmac']))
        # rule = match(srcip=entry['srcip'])
        # rule = match(dstmac=MAC(entry['dstmac']), srcport=entry['srcport'])
        rules.append(rule)
    
    allowed = ~(union(rules))

    return allowed
