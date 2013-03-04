from OS import _OS
from Lang.FuncTools.Abstraction import abstractmethod
from abc import ABCMeta, abstractproperty

class PrivilegeException(Exception):
	"""Instances of this and of CMD_ProcOutputException both have `proc` attributes containing a terminal command that was ran,
	or that the user will need to run in order to do the same functionality of something."""
	def __init__(self, procException):
		self.proc = procException.proc
		super(PrivilegeException, self).__init__(str(procException))

class CMD_ProcException(_OS.CMD_ProcException):
	def __init__(self, cmd, originalException=None):
		self.originalException = originalException
		kwargs = {}
		if originalException != None:
			kwargs["message"] = str(originalException)
		proc = _OS.CMD_Proc(cmd)
		super(CMD_ProcException, self).__init__(proc, **kwargs)

class PackageManager(object):
	__metaclass__ = ABCMeta
	def __init__(self):
		self._needsIndexUpdate = True
		assert self.isSupported()
#		self.setCanSudoPrompt(False)
	@classmethod
	@abstractmethod
	def isSupported(cls):
		pass
	@abstractproperty
	def _terminalPkgManagerName(self):
		pass
	
	def updatePackageIndex(self, force=False, exitOnNoRootPerm=True):
		"""
		Updates the package manager's package index using the network.
		
		@return bool:	True if root permissions are available; False if they aren't available and exitOnNoRootPerm is False.
		"""
		if force or self._needsIndexUpdate:
			rootPermKwargs = {}
			if exitOnNoRootPerm:
				rootPermKwargs["shouldExit"] = True
			
			if _OS.hasRootPermissions(rootPermKwargs):
				self._updatePackageIndex()
				self._needsIndexUpdate = False
				return True
			return False	# only possibly returned if exitOnNoRootPerm == False
	
	@abstractmethod
	def _updatePackageIndex(self):
		pass
	
#	def setCanSudoPrompt(self, canSudo=False):
#		"""
#		@param canSudo	bool:	If `True` and root permissions aren't available, prompt the user to enter their password for sudo. If `False`, exit the script with a message telling the user to perform package operations manually.
#		"""
#		self._canSudo = canSudo
	
	def _execAsRoot_withPkgs(self, actionName, packages, method, args=tuple(), kwargs={}):
		try:
			return self._execAsRoot(method, args, kwargs)
		except PrivilegeException as err:
			errorMsg = "Could not " + actionName + " the following system packages because of lack of root permissions: \n" + \
					   "\t" + " ".join(packages) + "\n" + \
					   "If possible, re-run this script under root or sudo, or if not possible, " + actionName + \
					   " these packages manually with " + self._terminalPkgManagerName + " and then re-run this script."
			raise Exception(errorMsg)
	def _execAsRoot_pkgManagerCommand(self, actionName, method, args=tuple(), kwargs={}):
		action = actionName + " with " + self._terminalPkgManagerName
		return self._execAsRoot_terminalCommand(method, args, kwargs, action)
	def _execAsRoot_terminalCommand(self, method, args=tuple(), kwargs={}, fakeTermCommand=None):
		try:
			return self._execAsRoot(method, args, kwargs)
		except PrivilegeException as err:
			errorMsg = "Could not perform:\n\t" + err.proc.cmd + "\n because of lack of root permissions.\n" + \
					   "If possible, re-run this script under root or sudo, or if not possible, run the previous " + \
					   "command manually and then re-run this script."
			raise Exception(errorMsg)
	def _execAsRoot(self, method, args=tuple(), kwargs=dict()):
		try:
			self.updatePackageIndex(exitOnNoRootPerm=False)
			return method(*args, **kwargs)
		except _OS.CMD_ProcException as err:
			if not _OS.hasRootPermissions():
				raise PrivilegeException(err)
			else:
				raise err
	
	def install(self, packageNames):
		if isinstance(packageNames, str):
			packageNames = [packageNames]
		packageNames = filter(lambda x: not self.isInstalled(x), packageNames)
		if len(packageNames) > 0:
			return self._execAsRoot_withPkgs("install", packageNames, self._install, args=(packageNames,))
	@abstractmethod
	def _install(self, packageNames):
		pass
	
	def update(self, packageNames=None):
		"""
		Updates/upgrades packages
		
		@param packageNames		iterable of str or None:	If None, all packages will be updated
		"""
		if isinstance(packageNames, str):
			packageNames = [packageNames]
		assert packageNames == None or hasattr(packageNames, "__iter__")
		if packageNames == None:
			return self._execAsRoot_pkgManagerCommand("update", self._update, args=(packageNames,))
		else:
			return self._execAsRoot_withPkgs("update", packageNames, self._update, args=(packageNames,))
	@abstractmethod
	def _update(self, packageNames=None):
		pass
	
	def remove(self, packageNames, *args, **kwargs):
		if isinstance(packageNames, str):
			packageNames = [packageNames]
		packageNames = filter(lambda x: self.isInstalled(x), packageNames)
		if len(packageNames) > 0:
			args = (packageNames,) + args
			return self._execAsRoot_withPkgs("remove", packageNames, self._remove, args, kwargs)
	@abstractmethod
	def _remove(self, packageNames, *args, **kwargs):
		pass
	
	@abstractmethod
	def isInstalled(self, packageName):
		"""Must be executable without requiring root privileges"""
		pass
	@abstractmethod
	def isAvailable(self, packageName):
		"""Must be executable without requiring root privileges"""
		pass

