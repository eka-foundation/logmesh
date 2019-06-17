def create_routing_csv():
    
    '''Creates the csv file with routing records'''
    
    import os
    import numpy as np
    import pandas as pd

    # get the node IPs
    nodes = list(set([i.split('_')[0] for i in os.popen('ls cleaned_logs/').readlines()]))

    out = []

    for node in nodes:
        records = _routing(node)
        out += records
    
    # create a dataframe from the records
    routing_df = pd.DataFrame(out).drop_duplicates()
    routing_df.columns = ['timestamp', 'originator', 'node_ip', 'next_hop']
    
    # convert timestamp string to datetime column
    routing_df.timestamp = pd.DatetimeIndex(routing_df.timestamp)

    # export to csv
    routing_df.to_csv('mesh.csv', index=None)
    
    return data

def _routing(node_ip):

    # open and read the file for the given node
    f = open('cleaned_logs/' + node_ip + '_routing.log', 'r')
    out = f.readlines()
    
    self_ip = out[1].split()[4].split('/')[1]
    
    final = []
    
    for i in out:

        # get the header with timestamp
        if i.startswith('###'):
            timestamp = i.replace('###', '').strip()

        # only use the records with actual routing info
        if 'wlan0-1' in i and 'B.A.T.M.A.N.' not in str(i):

            # remove mess from original records
            i = i.replace('*', '')
            i = i.replace('(', '')
            i = i.replace(')', '')

            # break down to individual datapoints (columns)
            i = i.strip().split()
            final.append([timestamp, i[0], self_ip, i[3]])
            
    return final
    
