# Package description

The OS module provides common operating system functions that are platform independent.

Note that for most of the functions/methods on this page, arguments are not listed. You should look at the source code to determine the arguments needed.

# Summary of functionality

* Finding a suitable version of python installed in the OS for compatibility reasons
* Retrieving general operating system information
* Interacting with operating system services - start, stop, restart, set boot state, etc.
* Interacting with the OS package manager (apt, yum, macports) - installing, removing, upgrading, etc.
* Miscellaneous APIs and scripts that do not yet have a home may also be included in this python OS package for various reasons. Currently, this includes:
  * Removal of legacy LinuxCommon package, which used to be a master package containing py.OS, py.Net, py.Lang, and py.Disk
  * GPG encryption/decryption library, which is not yet fully featured and is small enough to be included in the py.OS package

# Detailed functionality

## Python version information
The following is accessible by using the [PyVersion](@ref OS.PyVersion) module:

	import PyVersion

### Determining the executable path or name of the currently running python interpreter
	PyVersion.PY_EXE
### Finding a suitable installed version of python to run your code
	PyVersion.checkSuitablePyExe()

---

## Retrieving information about the OS and performing common OS-related functions
The following is accessible by using the OS module:

	import OS

### Determining what OS is running
	OS.flavor

### Determining the OS version
	OS.version

### Determining if an OS is unix/unix-like (Linux, Darwin, etc.)
	OS.isUnix()

### Determine if your python script has root permissions (ran as root or using sudo)
	OS.hasRootPermissions()

### Run a command in the terminal
There are lots of arguments here. Refer to the code!

	OS.runCMD()

---

## System services
The following is accessible by using the services module:

	import OS.svc

These features are self-explanatory with a quick glance at the code.

### Start, stop, or restart a service right now
### Change whether a service starts on boot
### Remove a service	

---

## System software packages
The following is accessible by using the packages module:

	import OS.pkg

OS.pkg is more complex than some modules. Most of this is due to differences between the underlying package managers supported by OS.pkg, including:
- `yum` for CentOS and Red Hat is supported natively through python, since yum itself is written in python
- `apt` for Debian, Ubuntu, etc. is supported by using the `python-apt` module which will be installed along with the `py.OS` package if your OS is apt-based
- `macports` for Mac OSX is supported (sadly) only by parsing command line output using the `port` command

The good news is that one similar API can be used to work with packages for all 3 package managers across different platforms.

The bad news is that sometimes a package will have a different name across different package managers, even though they effectively install the same thing. To work around this, you can do for example:

	if OS.pkg.isYumOS():
		OS.pkg.install("yum package name here")
	elif OS.pkg.isAptOS():
		OS.pkg.install("apt-get package name here")
	elif OS.pkg.isPortOS():
		OS.pkg.install("macports package name here")

Also, when using install, update, isAvailable, and similar functions, there is no need to manually update the list of available packages from the internet. This is done automatically when OS.pkg is imported.

### Checking if the pkg module supports your OS
	OS.pkg.isSupported()

### Checking if a package is installed
	OS.pkg.isInstalled()

### Checking if a package is available for install
	OS.pkg.isAvailable()

### Installing a package
See above. You can also install an iterable of packages like:

	OS.pkg.install(("nano", "vim", "emacs"))

### Upgrading/updating existing packages
	OS.pkg.update()

### Removing/uninstalling a package
	OS.pkg.remove()
- On apt, an additional argument `purgeConfigFiles` can be specified which, when `True`, is identical to `apt-get purge`

### Platform-specific functions
#### Updating the kernel on apt
	OS.pkg.updateKernel()

#### Installing a 3rd party repository on yum
	OS.pkg.installRepo_RPM()
	OS.pkg.installRepo_allKeys()

##### Installing EPEL on yum
This is a convenience method for installing EPEL. The latest EPEL RPM will be fetched.

	OS.pkg.installRepo_EPEL()

---

## GPG
The following is accessible by using the GPG module:

	from OS import GPG

These features are self-explanatory with a quick glance at the code in OS.GPG

### Import a key to the local keyring

### Get a key's ID

### Check if a key is imported

### Encrypt a file

### Decrypt a file

