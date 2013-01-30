from .. import _OS

def isAptOS():
	return _OS.flavor in ["ubuntu", "debian", "linuxmint"]

"""
This apt module supports the standard package methods in addition to an updateKernel(...) method
which will perform a distupgrade.
"""

class AptInstaller:
	def __init__(self):
		assert isAptOS()
		self.needsRepoUpdate = True
		
		try:
			import apt
			self._apt = self._init()
		except ImportError:
			_OS.runCMD("apt-get update")
			_OS.runCMD("apt-get -y install python-apt")
			import apt
			self._apt = self._init()
	
	def _init(self):
		import apt
		return apt.cache.Cache()
	
	def _updatePackageIndex(self):
		assert _OS.hasRootPermissions(assertTrue=True)
		if self.needsRepoUpdate:
			self._apt.update()
			self.needsRepoUpdate = False
	
	def install(self, packageNames):
		if isinstance(packageNames, str):
			packageNames = [packageNames]
		packageNames = filter(lambda x: not self.isInstalled(x), packageNames)
		
		if len(packageNames) > 0:
			self._updatePackageIndex()
			for pkgName in packageNames:
				self._apt[pkgName].mark_install()
			self._apt.commit()
	
	def update(self, packageNames=None):
		""" Updates/upgrades the specified list of packages, or all packages if packageNames == None """
		if packageNames == None:
			self._updatePackageIndex()
			_OS.runCMD("sudo apt-get upgrade")
		elif hasattr(packageNames, "__iter__"):
			self.install(packageNames)
	
	def updateKernel(self):
		_OS.runCMD("sudo apt-get dist-upgrade")
	
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
		return self._apt[packageName].installed != None
	
	def isAvailable(self, packageName):
		self._updatePackageIndex()
		return packageName in self._apt
