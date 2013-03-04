from setuptools import setup, find_packages
from setuptools.command.install import install as _install

import sys
if sys.version_info[0] >= 3 or sys.version_info <= (2,5):
	raise Exception("This module only supports Python 2.6 or 2.7")

requirements = [
	"py.Lang",
]
import setuptools
setuptools.dist.Distribution(dict(setup_requires="py.Lang"))
class InstallHook(_install):
	def run(self):
		self.preInstall()
		_install.run(self)
		self.postInstall()
	
	def preInstall(self):
		from Lang import DescribeOS
		if DescribeOS.isDebianBased():
			global requirements
			requirements.append("python-apt")
		# red hat based OSs come with a python yum module already installed
		# macport CLI is used on OSX, so no modules are needed for it
	
	def postInstall(self):
		from Lang import DescribeOS
		if DescribeOS.isRedHatBased():
			try:
				import yum
			except ImportError:
				raise Exception("Error: Could not find the python yum module. If you installed py.OS in a virtualenv, use the --system-site-packages to give access to python yum.")


# To include documentation in the build, create a MANIFEST.in file with these lines:
# recursive-exclude doc *
# recursive-include doc/html *

# reference URLs:
# http://docs.python.org/2/distutils/setupscript.html
# http://packages.python.org/distribute/setuptools.html
# http://docs.python.org/2/distutils/sourcedist.html
setup(
	cmdclass = {"install": InstallHook},
	name = "py.OS",
	version = "0.5.1-dev7",
	description = "Attempts to provide common operating system functions that are platform independent",
	author = "Jesse Cowles",
	author_email = "jcowles@indigital.net",
	url = "http://projects.indigitaldev.net/py.OS",
	
	package_dir = {"":"src"},
	packages = find_packages("src"),
	install_requires = requirements,
	zip_safe = False,
	classifiers = [
		# http://pypi.python.org/pypi?%3Aaction=list_classifiers
		"Development Status :: 4 - Beta",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Operating System :: POSIX :: Linux",
		"Operating System :: MacOS :: MacOS X",
		"Environment :: Console",
	],
#	keywords = "networking",
#	license = "",
)
