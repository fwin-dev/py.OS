import _OS

import sys, os, platform

"""
@package OS.PyVersion
@see checkSuitablePyExe

This module can also be invoked as a script from the terminal, with 2 purposes.
If no arguments are passed, it will print the name or path of the current python executable being invoked.
If a major.minor version is passed, it will try to locate the name/path of that installed python version.
	If no such version exists, 'None' will be printed out.
"""

def checkSuitablePyExe(ver=platform.python_version_tuple[:2], assertExists=True):
	"""
	Returns the executable name or path of the wanted python version which can be executed from the terminal.
	
	This function can be used to ensure compatibility between different versions.
	
	@param ver			tuple:	The wanted version, ex. (2,6)
	@param assertExists	bool:	If True, raises an exception if a suitable version isn't installed
	@return				string:	A compatible python executable name or path, or None
	"""
	currentVer = platform.python_version_tuple[:2]
	if currentVer < ver or currentVer[0] > ver[0]:
		# incompatible, so check for a differently installed python version
		exe = "python" + str(ver[0]) + "." + str(ver[1])
		if _OS.runCMD(exe + " -V", assertSuccess=False).returnCode != 0:
			if assertExists:
				raise Exception("Your python version is incompatible. Please install python " + ".".join(ver) + " and run this application using that version.")
			return None
		else:
			return exe
	else:
		return sys.executable

PY_EXE = checkSuitablePyExe()
"""Value returned by checkSuitablePyExe()"""

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print(PY_EXE)
	else:
		os.system(PY_EXE + " " + " ".join(sys.argv[1:]))
