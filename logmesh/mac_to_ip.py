def mac_to_ip():
    
    '''Figures out what the IP address of each mac address is.'''

    import os
    
    # get a list of unique node IPs
    nodes = []
    for i in os.popen('ls cleaned_logs').readlines():
        i = i.strip()
        nodes.append(i.split('_')[0])
        nodes = list(set(nodes))
    
    final = {}
    for node in nodes:

        # open and read the file for the given node
        f = open('cleaned_logs/' + node + '_routing.log', 'r')
        out = f.readlines()
        mac = out[1].split()[4].split('/')[1]
        
        # add the record to dictionary
        final[mac] = node
    
    return final
