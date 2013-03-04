from _base import PackageManager
from .. import _OS
from Lang import DescribeOS

class MacPortInstaller(PackageManager):
	def __init__(self):
		super(MacPortInstaller, self).__init__()
	@classmethod
	def isSupported(cls):
		return DescribeOS.flavor == "darwin" and _OS.runCMD("port version", assertSuccess=False).returnCode == 0
	@property
	def _terminalPkgManagerName(self):
		return "macports"
	def _updatePackageIndex(self):
		_OS.runCMD("port selfupdate")
	
	def _install(self, packageNames):
		_OS.runCMD("port install" + (" %s" * len(packageNames)), packageNames)
	
	def _update(self, packageNames=None):
		if packageNames == None:
			_OS.runCMD("port upgrade outdated")
		else:
			_OS.runCMD("port upgrade" + (" %s" * len(packageNames)), packageNames)
	
	def _remove(self, packageNames):
		for pkgName in packageNames:
			_OS.runCMD("port uninstall --follow-dependencies %s", pkgName)
	
	def isInstalled(self, packageName):
		for line in _OS.runCMD("port installed").stdout.split("\n"):
			if line.strip().split(" ")[0] == packageName:
				return True
		return False
	
	def isAvailable(self, packageName):
		self.updatePackageIndex(exitOnNoRootPerm=False)
		return _OS.runCMD("port search --exact --case-sensitive --name %s", packageName, assertSuccess=False) == -1
