def create_mesh_csv():
    
    import os
    import numpy as np
    import pandas as pd

    # get the node IPs
    nodes = list(set([i.split('_')[0] for i in os.popen('ls cleaned_logs/').readlines()]))

    # clean up the records for each node
    out = []
    for node in nodes:
        data = _mesh(node)
        out += data
    
    # create a dataframe from the cleaned records
    mesh_df = pd.DataFrame(out)
    mesh_df.columns = ['node_ip',
                       'timestamp',
                       'node_mac',
                       'signal_dbm',
                       'noise_dbm',
                       'ago_ms',
                       'rx_mbps',
                       'rx_MCS',
                       'rx_MHz',
                       'rx_pkts',
                       'tx_mbps',
                       'tx_MCS',
                       'tx_MHz',
                       'tx_pkts']

    # clean up various mess from the original records
    mesh_df = mesh_df.replace('NA', np.nan)
    mesh_df = mesh_df.replace('unknown', np.nan)
    mesh_df = mesh_df.replace('ms', np.nan)
    mesh_df = mesh_df.replace('dBm', np.nan)
    mesh_df.rx_MHz = mesh_df.rx_MHz.str.replace('MHz', '')
    mesh_df.tx_MHz = mesh_df.tx_MHz.str.replace('MHz', '')
    mesh_df.rx_MCS = mesh_df.rx_MCS.str.replace(',', '')
    mesh_df.tx_MCS = mesh_df.tx_MCS.str.replace(',', '')

    # convert to float what readily converts
    for col in mesh_df.columns:
        try:
            mesh_df[col] = mesh_df[col].astype(float)
        except:
            pass

    # drop bad records
    mesh_df = mesh_df[~mesh_df.timestamp.str.contains('###')]

    # convert timestamp string to datetime column
    mesh_df.timestamp = pd.DatetimeIndex(mesh_df.timestamp)

    # export to csv
    mesh_df.to_csv('mesh.csv', index=None)


def _mesh(node_ip):

    f = open('cleaned_logs/' + node_ip + '_mesh.log', 'r')
    out = f.readlines()

    final = []

    for i in out:

        i = i.strip()

        if i.startswith('###'):
            date = ' '.join(i.split()[2:])
        
        elif 'ms ago' in i:
            header = i.split()
            header = [header[0], header[1], header[4], header[8]]
            
        elif 'RX:' in i:
            rx = i.split()
            try:
                rx = [rx[1], rx[4], rx[5], rx[6]]
            except IndexError:
                rx = ['NA', 'NA', 'NA', 'NA']
            
        elif 'TX:' in i:
            tx = i.split()
            try:
                tx = [tx[1], tx[4], tx[5], tx[6]]
            except IndexError:
                tx = ['NA', 'NA', 'NA', 'NA']
            
            final.append([node_ip, date] + header + rx + tx)
            
    return final
