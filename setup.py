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

# To include documentation in the build, create a MANIFEST.in file with these lines:
# recursive-exclude doc *
# recursive-include doc/html *

# reference URLs:
# http://docs.python.org/2/distutils/setupscript.html
# http://packages.python.org/distribute/setuptools.html
# http://docs.python.org/2/distutils/sourcedist.html
setup(
    name = "py.OS",
    version = "0.5.0",
    description = "Attempts to provide common operating system functions that are platform independent",
    author = "Jesse Cowles",
    author_email = "jcowles@indigital.net",
	url = "http://projects.indigitaldev.net/py.OS",
	
	package_dir = {"":"src"},
	packages = find_packages("src"),
#	namespace_packages = ["Common"],
	install_requires = dependencies,
    zip_safe = False,
#    dependency_links = ["http://projects.indigitaldev.net/master#egg=gearman-2.0.0beta"],
	
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
