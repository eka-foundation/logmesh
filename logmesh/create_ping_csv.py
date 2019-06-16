def create_ping_csv():
    
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
        data = _ping_stats(node)
        out += data

    
    # create a dataframe from the records
    ping_df = pd.DataFrame(out)
    ping_df.columns = ['node_ip', 'timestamp', 'min', 'avg', 'max', 'mdev']
    ping_df[['min', 'avg', 'max', 'mdev']] = ping_df[['min', 'avg', 'max', 'mdev']].astype(float)
    
    # convert the timestamp string into datetime column
    ping_df.timestamp = pd.DatetimeIndex(ping_df.timestamp)

    # export to CSV in pwd
    ping_df.to_csv('ping.csv', index=None)


# helper function for create_ping_csv()
def _ping_stats(node_ip):

    # open and read the file for the given node
    f = open('cleaned_logs/' + node_ip + '_ping.log', 'r')
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
        elif 'rtt' in i:
            data = i.split('=')[-1].split(' ')[1]
            data = data.split('/')
            final.append([node_ip, date] + data)
    
    # return the cleaned records
    return final
