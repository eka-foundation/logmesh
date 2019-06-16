def create_connections_csv():

    import pandas as pd
    import os

    # get a list of unique node IPs
    nodes = []
    for i in os.popen('ls cleaned_logs').readlines():
        i = i.strip()
        nodes.append(i.split('_')[0])
        nodes = list(set(nodes))

    # go through files for each and clean records
    out = []
    for node in nodes:
        data = _wifi_clients(node)
        out += data

    # create a dataframe from the records
    wifi_df = pd.DataFrame(out)
    wifi_df.columns = ['node_ip', 'timestamp', 'no_of_connections']
    wifi_df.no_of_connections = wifi_df.no_of_connections.astype(int)
    
    # convert the timestamp string into datetime column
    wifi_df.timestamp = pd.DatetimeIndex(wifi_df.timestamp)

    # export to CSV in pwd
    wifi_df.to_csv('logmesh_zanskar_wifi.csv', index=None)


# helper function for create_connections_csv()
def _wifi_clients(node_ip):

    # open and read the file for the given node
    f = open('cleaned_logs/' + node_ip + '_wifi.log', 'r')
    out = f.readlines()

    final = []

    # iterate through each record to clean it up
    for i in out:
        
        # remove extra markings
        i = i.strip()

        # the records start with date so store that first
        if i.startswith('###'):
            date = ' '.join(i.split()[2:])
            
        # then take the actual values and combine both into single record
        elif 'Number' in i:
            data = i.split(':')[-1]
            final.append([node_ip, date, data])
            
    # return the cleaned records
    return final
