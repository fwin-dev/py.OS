import pkg
import _OS

import sys

"""
@package OS.svc
Service module can change the state of a service.

Supported operating systems include Debian based and Red Hat based.
"""

def changeCurrentState(serviceName, action):
    assert action in ["start", "stop", "restart"]
    _OS.runCMD("sudo /etc/init.d/%s %s", (serviceName, action))

def changeBootState(serviceName, shouldStartAtBoot):
    if pkg.isAptOS():   # debian
        cmd = "sudo update-rc.d %s"
        if shouldStartAtBoot:   cmd += " defaults"
        else:                   cmd += " remove"
    elif pkg.isYumOS():
        cmd = "sudo chkconfig %s"
        if shouldStartAtBoot:   cmd += " on"
        else:                   cmd += " off"
    else:
        raise NotImplemented
    
    _OS.runCMD(cmd, serviceName)

def remove(serviceName):
    if pkg.isAptOS():
        _OS.runCMD("sudo update-rc.d -f %s remove", serviceName)
    elif pkg.isYumOS():
        raise NotImplemented	# TODO
