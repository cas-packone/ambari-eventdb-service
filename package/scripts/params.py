from resource_management import *
from resource_management.libraries.script.script import Script
import sys, os, glob,socket

# server configurations
config = Script.get_config()
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
eventdb_dir = "/data/eventdb"
# eventdb_hdfs_dir = config['configurations']['eventdb']['eventdb.hdfs.dir']
server_cnf_config=config['configurations']['eventdb']['config']
collector_host= config['clusterHostInfo']['metrics_collector_hosts'][0]
current_host_name = socket.gethostname()
