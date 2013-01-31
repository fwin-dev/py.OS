from setuptools import setup, find_packages

import sys
if sys.version_info[0] >= 3 or sys.version_info <= (2,5):
	raise Exception("This module only supports Python 2.6 or 2.7")

def isAptOS():
	import platform
	try:
		platform.linux_distribution
	except AttributeError:
		DIST_FUNC = platform.dist
	else:
		DIST_FUNC = platform.linux_distribution
	flavor = DIST_FUNC()[0].lower()
	if DIST_FUNC() == ("debian", "lenny/sid", ""):  # fix for ubuntu 10.04
		flavor = "ubuntu"
	return flavor in ["ubuntu", "debian", "linuxmint"]

dependencies = []
if isAptOS():
	dependencies.append("python-apt")
# red hat based OSs come with a python yum module already installed
# macport CLI is used on OSX, so no modules for it

setup(
    name = "py.OS",
    version = "0.5.0",
    description = "Attempts to provide common operating system functions that are platform independent",
	long_description = """\
		Attempts to provide common operating system functions that are platform independent, including:
			- Interacting with the OS package manager (apt, yum, macports) - installing, removing, upgrading, etc.
			- Interacting with operating system services - start, stop, restart, set boot state, etc.
		""",
    author = "Jesse Cowles",
    author_email = "jcowles@indigital.net",
	url = "http://projects.indigitaldev.net/py.OS",
	
	package_dir = {"":"src"},
	packages = find_packages("src"),
	package_data = {
#		"": [
#			"doc"
#		]
	},
#	namespace_packages = ["Common"],
	install_requires = dependencies,
#    include_package_data = True,
	exclude_package_data = {"": ["*.pyc", ".DS_Store"]},
    zip_safe = False,
	
#	classifiers = [
#		# http://pypi.python.org/pypi?%3Aaction=list_classifiers
#	    "Classifier: Development Status :: 4 - Beta",
#	    "Classifier: Operating System :: POSIX :: Linux",
#	    "Classifier: Operating System :: MacOS :: MacOS X",
#	    "Classifier: Programming Language :: Python :: 2.6",
#	    "Classifier: Programming Language :: Python :: 2.7",
#	    "Classifier: Environment :: Console",
#	],
#	keywords = "networking",
#	license = "",
)
