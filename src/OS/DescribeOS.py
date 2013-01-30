import platform as __platform

try:
	__platform.linux_distribution
except AttributeError:
	__DIST_FUNC = __platform.dist
else:
	__DIST_FUNC = __platform.linux_distribution

flavor = __DIST_FUNC()[0].lower()
version = __DIST_FUNC()[1]
if __DIST_FUNC()[0] == "redhat" and __DIST_FUNC()[2] == "Final":   # fix for centos 5
	flavor = "centos"
elif __platform.system() == "Darwin":
	flavor = "darwin"
	version = __platform.mac_ver()
if __DIST_FUNC() == ("debian", "lenny/sid", ""):  # fix for ubuntu 10.04
	flavor = "ubuntu"

def isUnix(assertTrue=True):
	isUnix = __platform.system() in ["Linux", "Darwin"]
	if assertTrue:
		assert isUnix
	return isUnix
