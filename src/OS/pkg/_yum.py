from _base import PackageManager, CMD_ProcException
from .. import _OS
from Lang import DescribeOS

class _YumDummyCallback(object):
	def event(self, state, data=None):
		return True

class _EPEL:
	def _findBestEPEL(self):
		from Net.HTTPIndex_FindLatestFile import findLatestFile
		epelURL = "http://dl.fedoraproject.org/pub/epel/" + _OS.version[0] + "/i386/"
		return findLatestFile(epelURL, "epel-release-")
	
	def isInstalled(self):
		return not (_OS.flavor in ["centos", "rhel"] and not _OS.pkg.isInstalled("epel-release"))
	
	def install(self):
		if not self.hasEPEL():
			print("===Installing EPEL repository...\n")
			_OS.pkg.installRepo_RPM(self._findBestEPEL(), "epel")
			_OS.pkg.installRepo_allKeys()

class YumInstaller(PackageManager):
	def __init__(self):
		super(YumInstaller, self).__init__()
		self._yum = self._init()
	
	def _init(self):
		from yum import YumBase
		yum = YumBase()
		yum.setCacheDir()
		
		# urlgrabber is a 3rd party module
#		try:
#			if sys.stdout.isatty():
#				import imp
#				from urlgrabber.progress import TextMeter
#				output = imp.load_source("output", "/usr/share/yum=cli")
#				yum.repos.setProgressBar(TextMeter(fo=sys.stdout))
#				yum.repos.callback = output.CacheProgressCallback()
#				yumout = output.YumOutput()
#				freport = ( yumout.failureReport, (), {} )
#				yum.repos.setFailureCallback( freport )
#		except:
#			print("Warning: Unable to set progress indicator")
		
		return yum
	
	@classmethod
	def isSupported(cls):
		return DescribeOS.isRedHatBased()
	@property
	def _terminalPkgManagerName(self):
		return "yum"
	def _updatePackageIndex(self):
		try:
			self._yum.repos.doSetup()
		except Exception as err:
			raise CMD_ProcException("yum check-update", err)
	def installRepo_RPM(self, rpmURL, commonRepoName):
		"""
		Installs a new repository from an RPM.
		
		commonRepoName	--- The name used by yum for the repository; for example, "epel"
		"""
		return self._execAsRoot_terminalCommand(self._installRepo_RPM, args=(rpmURL, commonRepoName))
	def _installRepo_RPM(self, rpmURL, commonRepoName):
		_OS.hasRootPermissions(asserTrue=True)
		_OS.runCMD("rpm -Uvh %s", rpmURL)
		self._yum = self._init()	# needed to recognize new repo
		repos = self._yum.repos.findRepos(commonRepoName)
		assert len(repos) == 1 and len(repos[0].gpgkey) == 1
		_OS.runCMD("rpm --import %s", repos[0].gpgkey[0])
		self._needsIndexUpdate = True
	
	def installRepo_allKeys(self):
		"""Installs all keys for repo rpms already present on the system"""
		_OS.hasRootPermissions(assertTrue=True)
		
		for repoName in self._yum.repos.repos:
			for key in self._yum.repos.repos[repoName].gpgkey:
				_OS.runCMD("rpm --import %s", key)
	
	def installRepo_EPEL(self):
		_EPEL().install()
	
	def _install(self, packageNames):
		if not _OS.hasRootPermissions():
			raise CMD_ProcException("yum install " + " ".join(packageNames))
		for pkgName in packageNames:
			self._yum.install(name=pkgName)
		self._yum.buildTransaction()
		self._yum.processTransaction(_YumDummyCallback())
	
	def _update(self, packageNames=None):
		if packageNames == None:
			self._yum.update()
#			_OS.runCMD("sudo yum update")
		else:
			for packageName in packageNames:
				pkg_ = self._findPkgByName(packageName, assertExists=True)
				self._yum.update(po=pkg_)
			self._yum.resolveDeps()
			self._yum.processTransaction()
#			_OS.runCMD("sudo yum update " + " ".join(packageNames))
	
	def _remove(self, packageNames):
		if not _OS.hasRootPermissions():
			raise CMD_ProcException("yum remove " + " ".join(packageNames))
		for pkgName in packageNames:
			self._yum.remove(name=pkgName)
		self._yum.resolveDeps()
		self._yum.processTransaction()
	
	def isInstalled(self, packageName):
		return self._yum.rpmdb.installed(packageName)
	
	def _findPkgByName(self, packageName, assertExists=False):
		"""Note: ignores x86/x64 availability"""
		self._yum.doConfigSetup()
		self._yum.doRepoSetup()
		self._yum.doSackSetup()
		self._yum.doTsSetup()
		self._yum.doRpmDBSetup()
		self.updatePackageIndex(exitOnNoRootPerm=False)
		
		fields = ["name"]
		matches = self._yum.searchPackages(fields, [packageName])
		for match in matches:
			if match.name == packageName:
				return match
		
		if assertExists:
			raise Exception(str(packageName) + " not found in package database")
		else:
			return False
	
	def isAvailable(self, packageName):
		return self._findPkgByName(packageName) != False

