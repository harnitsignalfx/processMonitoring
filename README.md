# processMonitoring

Collectd Python plugin that returns a value of 1 if a process path or name is found matching the text you've specified. If the process is not found, then nothing is reported.

## Install Instructions

1. Place the python file - procmon.py in an appropriate location such as /usr/share/collectd/procmon-collectd-plugin
2. Create a configuration file or use the default one - 10-procmon.conf and place it under /etc/collectd/managed_config/

By default the configuration file tries to find the python file in the default location given under Step 1. But feel free to modify the location in Step 1 and make the same adjustment within the configuration file.

## Configuration
Variables within the configuration file - <br/> 
ProcessList - comma separated values in quotes for processes to match e.g. "collectd,zookeeper" will match any processes that have either the process name containing collectd or zookeeper or the process path containing the same text. <br/> 
Interval - How frequently should the plugin poll (in seconds) the process list and try to match content + dispatch values. <br/>

The name of the metric is set as 'gauge.process' (e.g. 'gauge.collectd' or 'gauge.zookeeper') and the process Ids come in as a plugin_instance dimension (since a single process name can have multiple matches)
