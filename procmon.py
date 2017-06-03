import collectd
import requests
import re
import collections
import time
import psutil

processList = []
INTERVAL = 10


def config_callback(conf):

	for node in conf.children:
        	try:
            		if node.key == 'ProcessList':
            			global processList
                		processList = node.values[0].split(",")
            		elif node.key == 'Interval':
                		global INTERVAL
                		INTERVAL = node.values[0]
        	except Exception as e:
            		collectd.error('Failed to load the configuration %s due to %s' % (node.key, e))
            		raise e
	if not processList:
    		collectd.error('Failed to load the configuration due to unspecified process List')

def init_callback():
	collectd.register_read(read_callback,interval=INTERVAL)

	#collectd.info('Matching pattern %s from URL %s and sending total matches as %s at a frequency of %s s' % (REGEX,URL,METRIC_NAME,INTERVAL))
	return True	

def read_callback():

# pid should be a dimension, as you can have multiple processes
# status should be binary - 0 if not found or dead. 1 if running (and not zombie)


	returnlist = {}
	global processList
	processes = []

	try:
		for p in psutil.process_iter():
		        #print('name:',p.name(),',PID:',p.pid,'cpu%:',p.is_running())
		        cmdline = p.cmdline()
		        cmdline.append(p.name())
		        appString = " ".join(cmdline)
		        for pattern in processList:
		                if pattern in appString:
		                        if (p.status() != psutil.STATUS_ZOMBIE) and (p.status() != psutil.STATUS_DEAD) and (p.status() != psutil.STATUS_STOPPED):
		                                # process is in running state. So add it.
		                                processDetails = {}
		                                processDetails["name"]=p.name()
		                                processDetails["pid"]=p.pid
		                                processDetails["isRunning"]=1
		                                if pattern in returnlist:
		                                        processes = returnlist[pattern]
		                                        processes.append(processDetails)
		                                else:
		                                        processes = [processDetails]
		                                        returnlist[pattern]=processes
		
		
		dispatch_values(returnlist)

	except Exception as e:
		collectd.error('Failed to fetch and transfer data due to %s' % (e))

def dispatch_values(returnlist):
	
	collectd.info('Returnlist - %s' % returnlist)

	# nothing to report
	if not returnlist:
		return

	val = collectd.Values(type='gauge',plugin='process-mon-plugin')
	for processes in returnlist:
		val.type_instance = processes
		for process in returnlist[processes]:
			val.plugin_instance = 'pid-'+str(process["pid"])
			val.values=[process["isRunning"]] 
			collectd.info('Dispatching - %s' %val)
			val.dispatch()


collectd.register_config(config_callback)
collectd.register_init(init_callback)
