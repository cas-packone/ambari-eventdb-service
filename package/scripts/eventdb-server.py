import os
import base64
from time import sleep
from resource_management import *

class EventdbServer(Script):
    
    def configure(self, env):
        import params
        env.set_params(params)
        server_cnf_config = InlineTemplate(params.server_cnf_config)
        File(params.eventdb_dir + "/eventdb-java/config.properties", content=server_cnf_config)

    def install(self, env):
        import params
        self.install_packages(env)
        Directory([params.eventdb_dir,params.eventdb_dir+"/demo/data"],
              mode=0755,
              cd_access='a',
              create_parents=True
        )
        Execute('cd ' + params.eventdb_dir + '; wget http://repo/hdp/eventdb/eventdb.tar.gz -O eventdb.tar.gz; tar -xzf eventdb.tar.gz; rm -rf eventdb.tar.gz')
        Execute('cd ' + params.eventdb_dir  + '; rm -rf eventdb-java; mv eventdb eventdb-java')
        Execute('cd ' + params.eventdb_dir  + '/eventdb-java; chmod +x eventdb; sed -i "s/\r//" eventdb')
        Execute('cd ' + params.eventdb_dir + "/demo/data" + '; wget http://repo/hdp/eventdb/demo/data/demo.FITS -O demo.FITS')
        # Execute('sudo -u hdfs -E hadoop fs -test -e '+params.eventdb_hdfs_dir+'; [ $? -ne 0 ] && sudo -u hdfs -E hadoop fs -mkdir -p '+params.eventdb_hdfs_dir, ignore_failures=True)
        # Execute('sudo -u hdfs -E hadoop fs -test -e '+params.eventdb_hdfs_dir+'/eventdb.jar; [ $? -ne 0 ] && sudo -u hdfs -E hadoop fs -put '+params.eventdb_dir+'/eventdb-java/target/eventdb-1.0.0.jar '+params.eventdb_hdfs_dir+'/eventdb.jar; sudo -u hdfs -E hadoop fs -chown -R hbase:hadoop '+params.eventdb_hdfs_dir, ignore_failures=True)
        Execute('cd ' + params.eventdb_dir + '; wget http://repo/hdp/eventdb/demo/droptables.hql; hbase shell<droptables.hql')
        self.configure(env)
        Execute('cd ' + params.eventdb_dir + '/eventdb-java; source /etc/profile.d/java.sh; ./eventdb init')
        Execute('cd ' + params.eventdb_dir + '/eventdb-java; source /etc/profile.d/java.sh; ./eventdb createTable HeFits 6')
        # Execute('cd ' + params.eventdb_dir + '/eventdb-java;./eventdb observer HeFits org.osv.eventdb.fits.FitsObserver '+params.eventdb_hdfs_dir+'/eventdb.jar')
        Execute('cd ' + params.eventdb_dir + '/eventdb-java; source /etc/profile.d/java.sh; ./eventdb insertHeFits ../demo/data/demo.FITS HeFits 3')
    
    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        service_packagedir = params.service_packagedir
        Execute('find '+params.service_packagedir+' -iname "*.sh" | xargs chmod +x')
        Execute("echo \"source /etc/profile.d/java.sh; nohup " + params.eventdb_dir + "/eventdb-java/eventdb server 8081  2>&1 >/dev/null &\"|at now +1 min")
        Execute(format("echo \"nohup {service_packagedir}/scripts/eventdb_metric_send.sh {collector_host} {current_host_name} &\"|at now +1 min"))
        sleep(60)
        Execute("ps -ef | grep -v grep | grep \"eventdb.Run server\" | awk '{print $2}' >/tmp/eventdb.pid")

    def stop(self, env):
        cmd = format("ps -ef|grep \"eventdb_metric\" |grep -v grep|cut -c 9-15|xargs kill -9 ")
        Execute(cmd, ignore_failures=False)
        cmd = format("ps -ef|grep \"eventdb.Run server\" |grep -v grep|cut -c 9-15|xargs kill -9 ")#must kill this process, not the bash script
        Execute(cmd, ignore_failures=False)

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status("/tmp/eventdb.pid")

if __name__ == "__main__":
    EventdbServer().execute()
