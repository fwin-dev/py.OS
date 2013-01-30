import OS
from LinuxCommon.Common import Disk

class GPG(object):
	def import_(self, keyFile):
		keyFile = str(keyFile)
		OS.runCMD("gpg --batch --import %s", keyFile)
		id = self.getKeyID(keyFile)
		# LIMITATION: if key is already signed, gnupg prints out key information to terminal even if stdout is connected to pipe
		# OS.runCMD("gpg --lsign-key " + id)
		# LIMITATION: owner trust of key can't be set non-interactively for it due to limitations in the gnupg interface
	
	def isKeyImported(self, id):
		""" id: an 8 or 16 character hex string """
		return id + ":" in OS.runCMD("gpg --list-secret-keys --with-colons").stdout
	
	def getKeyID(self, filename):
		if isinstance(filename, Disk.base.PathAbstract):
			assert isinstance(filename, Disk.Local.FilePath)
			filename = str(filename)
		
		id = None
		for line in OS.runCMD("gpg --with-colons %s", filename).stdout.split("\n"):
			line = line.split(":")
			if line[0] == "pub":
				if id != None:
					raise Exception("More than 1 key found in " + filename)
				id = line[4][8:]
		return id
	
	def encrypt(self, inputFilePath, keyID):
		if isinstance(inputFilePath, str) or isinstance(inputFilePath, unicode):
			inputFilePath = Disk.Local.FilePath(inputFilePath)
		outputFilePath = inputFilePath + ".pgp"
		if outputFilePath.exists():
			outputFilePath.remove()
		OS.runCMD("gpg --batch -r %s --output %s --encrypt %s", (keyID, outputFilePath, inputFilePath))
		return outputFilePath
	
	def decrypt(self, inputFilePath, password):
		if isinstance(inputFilePath, str) or isinstance(inputFilePath, unicode):
			inputFilePath = Disk.Local.FilePath(inputFilePath)
		assert str(inputFilePath).endswith(".pgp")
		outputFilePath = inputFilePath.splitext()[0]
		if outputFilePath.exists():
			outputFilePath.remove()
		OS.runCMD("gpg --batch --passphrase %s --output %s --decrypt %s", (password, outputFilePath, inputFilePath))
		return outputFilePath
		

GPG = GPG()
