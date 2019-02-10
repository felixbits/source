#!/usr/bin/python

### ensure firmware will have correct version info

import json
import re
import os
import argparse


# find the directory of the script
dirName = os.path.dirname(os.path.abspath(__file__))

buildInfoFile = "build_info.json"

# get build info
def getBuildInfo():
	filePath = ('../%s'%buildInfoFile) 	# path relative to this directory
	filePath = '/'.join([dirName, filePath])
	with open(filePath, "r") as f:
		data = json.load(f);
		return data

# update the buildroot's version info
def updateFwInfo(build, version):
	filePath = "../files/etc/uci-defaults/12_onion_version" 	# path relative to this directory
	filePath = '/'.join([dirName, filePath])
	with open(filePath, "r+") as f:
		data = f.read()

		data = re.sub(r"set\ onion\.@onion\[0\]\.version='(.*)'", "set onion.@onion[0].version='%s'"%version, data )
		data = re.sub(r"set\ onion\.@onion\[0\]\.build='(.*)'", "set onion.@onion[0].build='%s'"%build, data )

		f.seek(0)
		f.write(data)
	
# increment build number
def incrementBuildNumber():
	buildNumber = 0
	filePath = ("../%s"%buildInfoFile) 	# path relative to this directory
	filePath = '/'.join([dirName, filePath])

	with open(filePath, "r+") as f:
		data = json.load(f)
		buildNumber = data['build'] + 1
		data['build'] = buildNumber

		f.seek(0)
		json.dump(data, f)

	return buildNumber

# setup the build
def setupBuild():
	info = getBuildInfo()

	print '*'*20
	print "   Version: %s"%info["version"]
	print "   Build: %s"%info["build"]
	print '*'*20
	
	updateFwInfo(info["build"], info["version"])


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Prepare build system with version info.')
	parser.add_argument('-i', '--increment', action='store_true', help='increment build number')
	args = parser.parse_args()
	
	if args.increment:
		incrementBuildNumber()
		
	setupBuild()
	
	

	