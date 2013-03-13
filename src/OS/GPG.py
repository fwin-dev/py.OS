import OS

import os, os.path

class GPG(object):
	"""Quick GNUPG implementation with common functions, using the command line interface."""
	def importPublicKey(self, keyFile):
		keyFile = str(keyFile)
		OS.runCMD("gpg --batch --import %s", keyFile)
	
	def importPrivateKey(self, keyFile):
		keyFile = str(keyFile)
		OS.runCMD("gpg --batch --allow-secret-key-import --import %s", keyFile)
	
	def signKey(self, id_):
		"""
		LIMITATION: If key is already signed, gnupg prints out key information to terminal even if stdout is connected to pipe
		"""
		OS.runCMD("gpg --batch --lsign-key %s", id_)
	
	def markKeyTrusted(self, id_):
		"""
		LIMITATION: Owner trust of key can't be set non-interactively for it due to limitations in the gnupg interface
		"""
		OS.runCMD("gpg --edit-key %s trust quit", id_)
	
	def importPublicKey_signTrust(self, keyFile):
		"""
		LIMITATION: This requires manual user input
		"""
		keyFile = str(keyFile)
		self.importPublicKey(keyFile)
		id_ = self.getKeyID(keyFile)
		self.signKey(id_)
		self.markKeyTrusted(id_)
	
	def isKeyImported(self, id_):
		"""
		Checks if a public or private key is imported into the local keyring.
		
		@param id_	str:	An 8 or 16 character hex string
		"""
		return id_ + ":" in OS.runCMD("gpg --list-secret-keys --with-colons").stdout or \
			   id_ + ":" in OS.runCMD("gpg --list-public-keys --with-colons").stdout
	
	def getKeyID(self, filename):
		"""
		Gets first key ID of the key in filename.
		
		@return str:	8 character hex string
		"""
		filename = str(filename)
		
		id_ = None
		for line in OS.runCMD("gpg --with-colons %s", filename).stdout.split("\n"):
			line = line.split(":")
			if line[0] == "pub":
				if id_ != None:
					raise Exception("More than 1 key found in " + filename)
				id_ = line[4][8:]
		return id_
	
	def encrypt(self, inputFilePath, keyID):
		"""
		Encrypts a file.
		
		Note that the necessary keys must already be imported, signed, and trusted in the local keyring
		in order for encryption to work.
		
		@param inputFilePath	str:	File to encrypt. Will not be modified.
		@param keyID			str:	An 8 or 16 character hex string
		@return					str:	Path of the encrypted file
		"""
		inputFilePath = str(inputFilePath)
		outputFilePath = inputFilePath + ".pgp"
		if os.path.exists(outputFilePath):
			os.remove(outputFilePath)
		OS.runCMD("gpg --batch -r %s --output %s --encrypt %s", (keyID, outputFilePath, inputFilePath))
		return outputFilePath
	
	def decrypt(self, inputFilePath, password=None):
		"""
		Decrypts a file.
		
		Note that the necessary keys must already be imported, signed, and trusted in the local keyring
		in order for decryption to work.
		
		@param inputFilePath	str:	File to decrypt. Must have .pgp extension. Will not be modified.
		@param password			str:	Password of private key in keyring, or None if no password.
		@return					str:	Path of the decrypted file
		"""
		inputFilePath = str(inputFilePath)
		assert inputFilePath.endswith(".pgp")
		outputFilePath = os.path.splitext(inputFilePath)[0]
		if os.path.exists(outputFilePath):
			os.remove(outputFilePath)
		if password != None:
			OS.runCMD("gpg --batch --passphrase %s --output %s --decrypt %s", (password, outputFilePath, inputFilePath))
		else:
			OS.runCMD("gpg --batch --output %s --decrypt %s", (outputFilePath, inputFilePath))
		return outputFilePath
		

GPG = GPG()
