from DescribeOS import *

import shlex, subprocess, os, sys
import random, string

class CMDProcOutput:
	def __init__(self, cmd, returnCode, stdout, stderr):
		self.cmd = cmd
		self.returnCode = returnCode
		self.stdout = stdout
		self.stderr = stderr

class _OS:
	def __init__(self):
		pass
	
	@classmethod
	def hasRootPermissions(cls, assertTrue=False, shouldExit=True):
		if assertTrue and os.geteuid() != 0:
			raise Exception()
			if not shouldExit:
				raise Exception("You must run this script with sudo or as root")
			else:
				sys.exit("You must run this script with sudo or as root")
		return os.geteuid()==0
	
	@classmethod
	def getPyExe(cls):
		from py_version import PY_EXE
		return PY_EXE
	@classmethod
	def changeConfig(cls, _file, newLine, commentChar='#', assignChar=' ', sectionName=None, sectionMatch='['):
		import ConfigParser_m1
		return ConfigParser_m1.changeConfig(_file, newLine, commentChar, assignChar, sectionName, sectionMatch)
	@classmethod
	def getRandomDir(cls):
		LENGTH = 6
		_dir = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(LENGTH))
		_dir = "/tmp/py_" + _dir
		return _dir
	@classmethod
	def askYesNo(cls, question):
		return raw_input(question + " [y/n]: ").lower() in ["y", "yes"]
	
	@classmethod
	def runCMD(cls, command, params=None, assertSuccess=True, useBash=False, variables=None, printOutput=False, inputStr=None):
		if params != None:
			if not hasattr(params, "__iter__"):
				params = (params,)
			params = [str(param).replace(" ", "\\ ") for param in params]
			command = command % tuple(params)
		
		popenKwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE}
		if useBash or variables != None:
			if variables != None:
				useBash = True
				temp = os.environ.copy()
				temp.update(variables)
				variables = temp
			popenKwargs.update({"shell":True, "executable":"/bin/bash", "env":variables})
		
		comKwargs = {}
		if inputStr != None:
			popenKwargs["stdin"] = subprocess.PIPE
			comKwargs["input"] = inputStr
		
		try:
			proc = subprocess.Popen(shlex.split(command), **popenKwargs)
		except OSError:
			stdout = stderr = ""
			resultCode = -1
		else:
			stdout, stderr = proc.communicate(**comKwargs)
			resultCode = proc.wait()
		
		if resultCode != 0 and assertSuccess:
			print(stderr)
			raise Exception("Command: '" + command + "' returned " + str(resultCode))
		if printOutput:
			print(stdout)
		return CMDProcOutput(command, resultCode, stdout, stderr)


import inspect
_thisModule = sys.modules[__name__]
_class = _OS()
for name, func in inspect.getmembers(_class):
	if inspect.ismethod(func) and name[0] != "_":
		setattr(_thisModule, name, func)

