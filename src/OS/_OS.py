from Lang.DescribeOS import *

import shlex, subprocess, os, sys

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
		"""
		Determines if your python script was invoked by a user with root permissions (run as root or using sudo).
		
		@param assertTrue	bool:	Will throw an Exception if no root permissions.
		@param shouldExit	bool:	If True, your program will exit if there are no root permissions.
		@return				bool:	True if script has root permissions, False otherwise.
		"""
		
		if assertTrue and os.geteuid() != 0:
			raise Exception()
			if not shouldExit:
				raise Exception("You must run this script with sudo or as root")
			else:
				sys.exit("You must run this script with sudo or as root")
		return os.geteuid() == 0
	
	@classmethod
	def runCMD(cls, command, params=None, assertSuccess=True, useBash=False, variables=None, printOutput=False, inputStr=None):
		"""
		Runs a command on the terminal.
		
		@param params			iterable(str):	Parameters to substitute into command. If given, command must contain a %s for each parameter.
		@param assertSuccess	bool:			If True, will throw an Exception if the command returns a non-zero exit code.
		@param useBash			bool:			Use the bash environment to execute the command.
		@param variables		dict{str:str}:	Environment variables to set before the command executes. The keys are environment variable names.
		@param printOutput		bool:			If True, prints the stdout of the command to the screen.
		@param inputStr			str:			A string to write to the process's stdin.
		
		@return CMDProcOutput: An instance through which stdout, stderr, and return code of the process can be accessed.
		"""
		
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

