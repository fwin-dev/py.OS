from Lang.DescribeOS import *

import shlex, subprocess, os, sys

class CMD_Proc(object):
	def __init__(self, cmd):
		self.cmd = cmd

class CMD_ProcOutput(CMD_Proc):
	def __init__(self, cmd, returnCode, stdout, stderr):
		super(CMD_ProcOutput, self).__init__(cmd)
		self.returnCode = returnCode
		self.stdout = stdout
		self.stderr = stderr

class CMD_ProcException(Exception, object):
	def __init__(self, proc, message=None):
		self.proc = proc
		if message == None:
			message = "Command: '" + self.proc.cmd + "' could not be executed"
		super(CMD_ProcException, self).__init__(message)

class CMD_ProcOutputException(CMD_ProcException):
	def __init__(self, cmdProcOutput):
		message = "Command: '" + cmdProcOutput.cmd + "' returned " + str(cmdProcOutput.returnCode)
		super(CMD_ProcOutputException, self).__init__(cmdProcOutput, message=message)

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
			if not shouldExit:
				raise Exception("You must run this script with sudo or as root")
			else:
				sys.exit("You must run this script with sudo or as root")
		return os.geteuid() == 0
	
	@classmethod
	def runCMD_getFullCMD(cls, command, params=None):
		"""
		@return str:	The terminal command with command line parameters, escaped if needed
		"""
		if params != None:
			if not hasattr(params, "__iter__"):
				params = (params,)
			params = [str(param).replace(" ", "\\ ") for param in params]
			command = command % tuple(params)
		return command
	
	@classmethod
	def runCMD(cls, command, params=None, assertSuccess=True, useBash=True, variables=None, printOutput=False, inputStr=None):
		"""
		Runs a command on the terminal.
		
		@param params			iterable(str):	Parameters to substitute into command. If given, command must contain a %s for each parameter.
		@param assertSuccess	bool:			If True, will throw an Exception if the command returns a non-zero exit code.
		@param useBash			bool:			Use the bash environment to execute the command.
		@param variables		dict{str:str}:	Environment variables to set before the command executes. The keys are environment variable names.
		@param printOutput		bool:			If True, prints the stdout of the command to the screen.
		@param inputStr			str:			A string to write to the process's stdin.
		
		@return CMD_ProcOutput: An instance through which stdout, stderr, and return code of the process can be accessed.
		"""
		command = cls.runCMD_getFullCMD(command, params)
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
		
		cmdProcOutput = CMD_ProcOutput(command, resultCode, stdout, stderr)
		if resultCode != 0 and assertSuccess:
			print(stderr)
			raise CMD_ProcOutputException(cmdProcOutput)
		if printOutput:
			print(stdout)
		return cmdProcOutput


import inspect
_thisModule = sys.modules[__name__]
_class = _OS()
for name, func in inspect.getmembers(_class):
	if inspect.ismethod(func) and name[0] != "_":
		setattr(_thisModule, name, func)

