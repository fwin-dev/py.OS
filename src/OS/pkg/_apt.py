from _base import PackageManager, CMD_ProcException
from .. import _OS
from Lang import DescribeOS

"""
This apt module supports the standard package methods in addition to an updateKernel(...) method
which will perform a distupgrade.
"""

class AptInstaller(PackageManager):
	def __init__(self):
		super(AptInstaller, self).__init__()
		try:
			self._apt = self._init()
		except ImportError:
			self._execAsRoot_withPkgs("install", ("python-apt",), self._installPyAptModule)
			self._apt = self._init()
			self._needsIndexUpdate = False
	
	def _installPyAptModule(self):
		try:
			_OS.runCMD("apt-get update")
			_OS.runCMD("apt-get -y install python-apt")
		except Exception as err:
			raise CMD_ProcException("apt-get install python-apt", err)
	def _init(self):
		import apt
		return apt.cache.Cache()
	@classmethod
	def isSupported(cls):
		return DescribeOS.isDebianBased()
	@property
	def _terminalPkgManagerName(self):
		return "apt-get"
	def _updatePackageIndex(self):
		try:
			self._apt.update()
		except Exception as err:
			raise CMD_ProcException("apt-get update", err)
	
	def _install(self, packageNames):
		try:
			for pkgName in packageNames:
				self._apt[pkgName].mark_install()
				self._apt.commit()
		except Exception as err:
			raise CMD_ProcException("apt-get install " + " ".join(packageNames), err)
	
	def _update(self, packageNames=None):
		if packageNames == None:
			_OS.runCMD("apt-get upgrade")
		else:
			self.install(packageNames)
	def updateKernel(self):
		return self._execAsRoot_pkgManagerCommand("dist-upgrade", self._updateKernel)
	def _updateKernel(self):
		_OS.runCMD("apt-get dist-upgrade")
	
	def _remove(self, packageNames, purgeConfigFiles=False):
		"""
		@param purgeConfigFiles	bool:	When `True`, does the equivalent of an `apt-get purge`
		"""
		try:
			for pkgName in packageNames:
				self._apt[pkgName].mark_delete(purge = purgeConfigFiles)
			self._apt.commit()
		except Exception as err:
			raise CMD_ProcException("apt-get purge " + " ".join(packageNames), err)
	
	def isInstalled(self, packageName):
		return self._apt[packageName].installed != None
	
	def isAvailable(self, packageName):
		self.updatePackageIndex(exitOnNoRootPerm=False)		# if no root, use existing index without updating
		return packageName in self._apt

