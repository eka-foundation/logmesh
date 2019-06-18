def mac_to_ip():
    
    '''Figures out what the IP address of each mac address is.'''

    # get a list of all nodes in the network
    nodes = sorted(pd.read_csv('ping.csv').node_ip.unique())
    
    final = {}
    for node in nodes:

        # open and read the file for the given node
        f = open('cleaned_logs/' + node + '_routing.log', 'r')
        out = f.readlines()
        mac = out[1].split()[4].split('/')[1]
        
        # add the record to dictionary
        final[mac] = node
    
    return final
