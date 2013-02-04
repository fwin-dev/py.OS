import OS

import os, os.path

class GPG(object):
	"""Quick GNUPG implementation with common functions, using the command line interface."""
	def import_(self, keyFile):
		keyFile = str(keyFile)
		OS.runCMD("gpg --batch --import %s", keyFile)
		id_ = self.getKeyID(keyFile)
		# LIMITATION: if key is already signed, gnupg prints out key information to terminal even if stdout is connected to pipe
		# OS.runCMD("gpg --lsign-key " + id_)
		# LIMITATION: owner trust of key can't be set non-interactively for it due to limitations in the gnupg interface
	
	def isKeyImported(self, id):
		"""
		Checks if a key is imported into the local keyring.
		
		@param id	str:	An 8 or 16 character hex string
		"""
		return id + ":" in OS.runCMD("gpg --list-secret-keys --with-colons").stdout
	
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
	
	def decrypt(self, inputFilePath, password):
		"""
		Decrypts a file.
		
		Note that the necessary keys must already be imported, signed, and trusted in the local keyring
		in order for decryption to work.
		
		@param inputFilePath	str:	File to decrypt. Must have .pgp extension. Will not be modified.
		@param password			str:	Password of private key in keyring
		@return					str:	Path of the decrypted file
		"""
		inputFilePath = str(inputFilePath)
		assert inputFilePath.endswith(".pgp")
		outputFilePath = os.path.splitext(inputFilePath)[0]
		if os.path.exists(outputFilePath):
			os.remove(outputFilePath)
		OS.runCMD("gpg --batch --passphrase %s --output %s --decrypt %s", (password, outputFilePath, inputFilePath))
		return outputFilePath
		

GPG = GPG()
