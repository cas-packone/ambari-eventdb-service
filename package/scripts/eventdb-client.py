import os
import base64
from time import sleep
from resource_management import *

class EventdbClient(Script):
    
    def install(self, env):
        import params
        self.install_packages(env)
        Directory([params.eventdb_dir],
              mode=0755,
              cd_access='a',
              create_parents=True
        )
        Execute('cd ' + params.eventdb_dir + '; wget http://repo/hdp/eventdb/eventdb.tar.gz -O eventdb.tar.gz; tar -xzf eventdb.tar.gz; rm -rf eventdb.tar.gz')
        Execute('cd ' + params.eventdb_dir  + ';  rm  -rf eventdb-java; mv  eventdb eventdb-java')
        Execute('cd ' + params.eventdb_dir  + '/eventdb-java; chmod +x eventdb; sed -i "s/\r//" eventdb')    
    def configure(self, env):
        import params
        env.set_params(params)
        server_cnf_config = InlineTemplate(params.server_cnf_config)   
        File(format("{eventdb_dir}/eventdb-java/config.properties"), content=server_cnf_config)

if __name__ == "__main__":
    EventdbClient().execute()