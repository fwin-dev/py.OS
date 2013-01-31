from .. import _OS

def isYumOS():
	return _OS.flavor in ["fedora", "redhat", "centos", "mandrake", "yellowdog"]

class _YumDummyCallback(object):
	def event(self, state, data=None):
		return True

class _EPEL:
	def _findBestEPEL(self):
		from Net.HTTPIndex_FindLatestFile import findLatestFile
		epelURL = "http://dl.fedoraproject.org/pub/epel/" + _OS.version[0] + "/i386/"
		return findLatestFile(epelURL, "epel-release-")
	
	def isInstalled(self):
		return not (_OS.flavor in ["centos", "rhel"] and not pkg.isInstalled("epel-release"))
	
	def install(self):
		if not self.hasEPEL():
			print("===Installing EPEL repository...\n")
			_OS.pkg.installRepo_RPM(self._findBestEPEL(), "epel")
			_OS.pkg.installRepo_allKeys()

class YumInstaller:
	def __init__(self):
		assert isYumOS()
		self.needsRepoUpdate = True
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
	
	def installRepo_RPM(self, rpmURL, commonRepoName):
		_OS.hasRootPermissions(assertTrue=True, shouldExit=True)
		_OS.runCMD("rpm -Uvh %s", rpmURL)
		self._yum = self._init()	# needed to recognize new repo
		repos = self._yum.repos.findRepos(commonRepoName)
		assert len(repos) == 1 and len(repos[0].gpgkey) == 1
		_OS.runCMD("rpm --import %s", repos[0].gpgkey[0])
		self.needsRepoUpdate = True
	
	def installRepo_allKeys(self):
		""" Installs all keys for repo rpms already present on the system """
		_OS.hasRootPermissions(assertTrue=True, shouldExit=True)
		
		for repoName in self._yum.repos.repos:
			for key in self._yum.repos.repos[repoName].gpgkey:
				_OS.runCMD("rpm --import %s", key)
	
	def installRepo_EPEL(self):
		_EPEL().install()
	
	def _updatePackageIndex(self):
		assert _OS.hasRootPermissions(assertTrue=True)
		if self.needsRepoUpdate:
			# self._yum.update()
			self._yum.doSetup()
			self.needsRepoUpdate = False
	
	def install(self, packageNames):
		self._updatePackageIndex()
		if isinstance(packageNames, str):
			packageNames = [packageNames]
		packageNames = filter(lambda x: not self.isInstalled(x), packageNames)
		
		_OS.hasRootPermissions(assertTrue=True, shouldExit=True)
		for pkgName in packageNames:
			self._yum.install(name=pkgName)
		self._yum.buildTransaction()
		self._yum.processTransaction(_YumDummyCallback())
	
	def update(self, packageNames=None):
		if isinstance(packageNames, str):
			packageNames = [packageNames]
		
		self._updatePackageIndex()
		if packageNames == None:
			_OS.runCMD("sudo yum update")
		elif hasattr(packageNames, "__iter__") and len(packageNames) > 0:
			_OS.runCMD("sudo yum update" + (" %s" * len(packageNames)), packageNames)
	
	def remove(self, packageNames):
		if isinstance(packageNames, str):
			packageNames = [packageNames]
		packageNames = filter(lambda x: self.isInstalled(x), packageNames)
		
		_OS.hasRootPermissions(assertTrue=True, shouldExit=True)
		for pkgName in packageNames:
			self._yum.remove(name=pkgName)
		self._yum.resolveDeps()
		self._yum.processTransaction()
	
	def isInstalled(self, packageName):
		return self._yum.rpmdb.installed(packageName)
	
	# ignores x86/x64 availability
	def isAvailable(self, packageName):
		self._yum.doConfigSetup()
		self._yum.doRepoSetup()
		self._yum.doSackSetup()
		self._yum.doTsSetup()
		self._yum.doRpmDBSetup()
		self._updatePackageIndex()
		
		fields = ["name"]
		matches = self._yum.searchPackages(fields, [packageName])
		for match in matches:
			if match.name == packageName:
				return True
		return False
