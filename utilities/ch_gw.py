""" ch_gw.py

python hack to read "thethings network" gateway page and check if one's own gateway is active

The program is executed by: $python ch_gw.py

Depending on the settings various information will be printed on the console. If verbose is true then
when a gateway is found all information is returned, if verbose is false only a '0' or '1' are returned
to indicate if the gateway is available or not.

(c)2016 by Roland van Straten, All Rights Reserved.

This program is free to use by anyone! Sharing any improvement is appreciated!


01-07-2016 ROLAND Quick way to check status of the gateway from anywhere

TODO: add cli and frozen
TODO: put the config into a json config file and use this by default
TODO: improve error checking if needed
TODO: improve by interpreting the states of the gateway and report this back in non-verbose mode
      so it is easier to integrate in an shell script or the like.

"""


from urllib2 import Request, urlopen, URLError
import json

config = {	'url' 		: 'http://staging.thethingsnetwork.org/gatewaystatus/' ,
			'gw'		: '0000024B080503B8' ,
			'debug' 	: False ,
			'verbose' 	: True ,
		}


# get the page of gateways from thethings network
req = Request(config['url'])
# my private gateway
myGateway = config['gw']
# debugging
debug = config['debug']
# informative :-)
verbose = config['verbose']


def main():
	""" main program
		importing this script will not lead to execution
	"""
	# so try to open the URL and read from it
	try:
		response = urlopen(req)
	except URLError as e:
		if hasattr(e, 'reason'):
			print("Failed to reach server due to ", e.reason)
		elif hasattr(e, 'code'):
			print("Server could not fullfil request due to error ", e.code)
	else:
		found = False
		# read all data lines one by one
		for line in response.readlines():
			lizt = line.split("\n'")
			# show all entries
			if debug:
				print(lizt[0]) # [0][0:16] is only number, now all info
			# check existence of my gateway
			if myGateway == lizt[0][0:16]:
				if verbose:
					print("Found my gateway [{:s}] with uplink state [{:s}] and downlink state [{:s}], {:s}".format(lizt[0][0:16], lizt[0][17:25], lizt[0][26:35], lizt[0][36:] ) )
				found = True

		if found == False:
			if verbose:
				print("Could not locate [{:s}]. Is the packet forwarder running?".format(myGateway) )
			else:
				print('0')
		else:
			if not verbose:
				print('1')


"""
"""
if __name__ == '__main__':
	main()
