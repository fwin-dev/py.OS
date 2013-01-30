from LinuxCommon import LC
import Common
from Common.Disk.Tempfile import NamedSecureTempFile

import sys, fileinput, re

class ParseException(Exception):
	def __init__(self, message=""):
		self.message = message
	def __str__(self):
		return self.message

class ConfigLine:
	def __init__(self, line, commentChar='#', assignChar='='):
		""" assignChar:	can be None """
		self.line = line
		self.commentChar = commentChar
		self.assignChar = assignChar
		
		temp = self.line.strip()
		if len(temp) > 0 and temp[0] == self.commentChar:
			temp = temp[1:]
			self.isCommentedOut = True
		else:
			self.isCommentedOut = False
		
		if assignChar != None:
			temp = temp.split(self.assignChar, 1)
			self.optionName = temp[0]
			temp = temp[1]
		else:
			self.optionName = None
		
		temp = re.split("(\s*" + re.escape(self.commentChar) + ".*)$", temp, 1)
		if self.optionName != None:
			self.optionValue = temp[0].strip()
		else:
			self.optionName = temp[0].strip()
			self.optionValue = None
		
		if len(temp) > 1:
			self.endLine = temp[1]
			if self.endLine == "":
				self.endLine = None
		else:
			self.endLine = None
	
	def __str__(self):
		return self.line

def changeConfig(_file, newLine, commentChar='#', assignChar=' ', sectionName=None, sectionMatch='['):
	with NamedSecureTempFile(delete=False) as backupFile:
		Common.shutil.copyFile(_file, backupFile, closeSrcFile=False, closeDestFile=False, copyDates=True)
		try:
			return _changeConfig(_file, newLine, commentChar, assignChar, sectionName, sectionMatch)
		except:
			Common.shutil.moveFile(backupFile, _file, closeSrcFile=False, closeDestFile=False, copyDates=True)
			raise

def _changeConfig(_file, newLine, commentChar='#', assignChar=' ', sectionName=None, sectionMatch='['):
	""" Changes a config file line in the format '#OptionName foo' (format can be changed with parameters) under specified section.
		Returns a list of all the following that apply:
			0	If setting name was encountered in the file and it was uncommented
			1	If setting name was encountered in the file and it was commented out
			2	If setting name and value were added by this function
			3	If setting value was changed by this function """
	newLine = ConfigLine(newLine + "\n", commentChar, assignChar)
	
	returnCode = []
	inSection = False
	for line in fileinput.input(_file, inplace=1):
		if sectionName != None:
			if line.startswith(sectionMatch):
				if line.startswith(sectionMatch + sectionName):
					inSection = True
				else:
					inSection = False
				sys.stdout.write(line)
				continue
			if not inSection:
				sys.stdout.write(line)
				continue
		
		try:
			parsedOldLine = ConfigLine(line, commentChar, assignChar)
		except ParseException:
			sys.stdout.write(line)
			continue
		if parsedOldLine.optionName != newLine.optionName:
			sys.stdout.write(line)
			continue
		if len(returnCode) != 0:
			continue	# don't write line
		
		if newLine.endLine == None and parsedOldLine.endLine != None:
			newLine.endLine = parsedOldLine.endLine
		
		sys.stdout.write(str(newLine))	# writes new line in place of old line
		if parsedOldLine.isCommentedOut:
			returnCode.append(1)
		else:
			returnCode.append(0)
		if parsedOldLine.optionValue != newLine.optionValue:
			returnCode.append(3)
	
	if len(returnCode) == 0:
		with open(_file, 'a') as f:
			f.write(str(newLine))
		returnCode = [2]
	
	return returnCode
