from macports import isMacPortOS, MacPortInstaller
from apt import isAptOS, AptInstaller
from yum import isYumOS, YumInstaller

import sys, inspect

def isSupported():
	return isAptOS() or isYumOS() or isMacPortOS()

if isAptOS():
	_class = AptInstaller()
elif isYumOS():
	_class = YumInstaller()
elif isMacPortOS():
	_class = MacPortInstaller()
else:
	_class = None

if _class != None:
	_thisModule = sys.modules[__name__]
	for name, func in inspect.getmembers(_class):
		if inspect.ismethod(func) and name[0] != "_":
			setattr(_thisModule, name, func)
