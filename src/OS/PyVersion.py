import _OS

import sys, os

def checkSuitablePyExe(ver=(2,6), assertExists=True):
	currentVer = [int(i) for i in _OS.runCMD("python -V").stderr.split("\n")[0].replace("Python ", "").split(".")]
	if currentVer < ver:
		exe = "python" + str(ver[0]) + "." + str(ver[1])
		if _OS.runCMD(exe + " -V", assertSuccess=False).returnCode != 0:
			if assertExists:
				raise Exception("Your python version is too old. Please install python " + ".".join(ver) + " and run this application using that version.")
		else:
			return exe
	else:
		return "python"

PY_EXE = checkSuitablePyExe()

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("\n=== Found py exe '" + PY_EXE + "'")
	else:
		os.system(PY_EXE + " " + " ".join(sys.argv[1:]))
