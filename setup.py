from setuptools import setup, find_packages
from setuptools.command.install import install as _install

import sys

requirements = [
	"py.Lang",
	"py.Net",
]
import setuptools
setuptools.dist.Distribution(dict(setup_requires="py.Lang"))
class InstallHook(_install):
	def run(self):
		self.preInstall()
		_install.run(self)
		self.postInstall()
	
	def preInstall(self):
		if sys.version_info[0] >= 3 or sys.version_info <= (2,5):
			raise Exception("This module only supports Python 2.6 or 2.7")
		
		from Lang import DescribeOS
		if DescribeOS.isDebianBased():
			global requirements
			requirements.append("python-apt")
		elif DescribeOS.isRedHatBased():
			# red hat based OSs come with a python yum module already installed
			try:
				import yum
			except ImportError:
				raise Exception("Error: Could not find the python yum module. If you installed py.OS in a virtualenv, use --system-site-packages to give access to python yum. You will need to re-create the virtualenv to do this.")
		# macport CLI is used on OSX, so no modules are needed for it
	
	def postInstall(self):
		pass

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
	version = "1.0.2",
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
		"Development Status :: 5 - Production/Stable",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
		"Operating System :: POSIX :: Linux",
		"Operating System :: MacOS :: MacOS X",
		"Environment :: Console",
	],
#	keywords = "networking",
#	license = "",
)
