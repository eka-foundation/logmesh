def prepare():
    
    # note that you should have batman.zip in pwd

    import os
    import gzip
    
    os.mkdir('mesh_logs')
    os.system('unzip batman.zip')
    os.system('mv batman/* mesh_logs')
    os.system('rm -r batman')

    # get the list of the nodes
    nodes = os.popen('ls mesh_logs').readlines()

    # convert the names to standard ip format
    for node in nodes:

        current = node.strip()
        new = node.strip().replace('_', '.')

        os.system('mv mesh_logs/' + current + ' mesh_logs/' + new)

    # first we get the list of the node IPs
    for node in os.popen('ls mesh_logs').readlines():

        # remove newlines
        node = node.strip()

        os.system('gzip -d mesh_logs/' + node + '/*.gz')

    for node in os.popen('ls mesh_logs').readlines():

        # remove newlines
        node = node.strip()

        os.system('cat mesh_logs/' + node + '/bat*.lo* > ' + node + '_routing.log')
        os.system('cat mesh_logs/' + node + '/mesh*.lo* > ' + node + '_mesh.log')
        os.system('cat mesh_logs/' + node + '/ping_stats*.lo* > ' + node + '_ping.log')
        os.system('cat mesh_logs/' + node + '/wifi*.lo* > ' + node + '_wifi.log')

    os.mkdir('cleaned_logs')
    os.system('mv *.log cleaned_logs')
    os.system('rm -rf mesh_logs/')
