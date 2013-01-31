import sys, os.path, shutil

def remove():
	# centos based machines don't usually have /usr/local/lib/python
	localLibPath = "python" + str(sys.version_info[0]) + "." + str(sys.version_info[1])
	localLibPath = os.path.join("/usr/local/lib", localLibPath, "dist-packages/LinuxCommon")
	if os.path.exists(localLibPath):
		print("Found legacy LinuxCommon package installed. Removing...")
		shutil.rmtree(localLibPath)
		print("\tDone")
