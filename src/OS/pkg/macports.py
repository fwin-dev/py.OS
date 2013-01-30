from .. import _OS

def isMacPortOS():
	return _OS.flavor == "darwin" and _OS.runCMD("port version", assertSuccess=False).returnCode == 0

class MacPortInstaller:
	def __init__(self):
		assert isMacPortOS()
		self.needsRepoUpdate = True
	def _updatePackageIndex(self):
		assert _OS.hasRootPermissions(assertTrue=True)
		if self.needsRepoUpdate:
			_OS.runCMD("port selfupdate")
			self.needsRepoUpdate = False
	
	def install(self, packageNames):
		if isinstance(packageNames, str):
			packageNames = [packageNames]
		packageNames = filter(lambda x: not self.isInstalled(x), packageNames)
		
		if len(packageNames) > 0:
			self._updatePackageIndex()
			_OS.runCMD("port install" + (" %s" * len(packageNames)), packageNames)
	
	def update(self, packageNames=None):
		""" Updates/upgrades all packages """
		if isinstance(packageNames, str):
			packageNames = [packageNames]
		
		self._updatePackageIndex()
		if packageNames == None:
			_OS.runCMD("port upgrade outdated")
		elif hasattr(packageNames, "__iter__") and len(packageNames) > 0:
			_OS.runCMD("port upgrade" + (" %s" * len(packageNames)))
	
	def remove(self, packageNames, purgeConfigFiles=False):
		if isinstance(packageNames, str):
			packageNames = [packageNames]
		packageNames = filter(lambda x: self.isInstalled(x), packageNames)
		
		if len(packageNames) > 0:
			_OS.hasRootPermissions(assertTrue=True, shouldExit=True)
			for pkgName in packageNames:
				self._apt[pkgName].mark_delete(purge = purgeConfigFiles)
			self._apt.commit()
	
	def isInstalled(self, packageName):
		for line in _OS.runCMD("port installed").stdout.split("\n"):
			if line.strip().split(" ")[0] == packageName:
				return True
		return False
	
	def isAvailable(self, packageName):
		self._updatePackageIndex()
		return _OS.runCMD("port search --exact --case-sensitive --name %s", packageName, assertSuccess=False) == -1
