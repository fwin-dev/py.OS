import sys, fileinput, re

class ParseException(Exception):
    def __init__(self, message=""):
        self.message = message
    def __str__(self):
        return self.message

class ConfigLine:
    def __init__(self, line, commentChar='#', assignChar=' '):
        self.commentChar = commentChar
        self.assignChar = assignChar
        
        if len(line.split(commentChar, 1)) == 2:
            line = line[1:]
            self.isCommentedOut = True
        else:
            self.isCommentedOut = False
        
        temp = line.split(assignChar, 3)
        self.endLineComment = ""
        self.endLineCommentWhitespace = ""
        if len(temp) == 3 and temp[2].strip().find(commentChar) == 0:
            self.endLineCommentWhitespace = temp[2][:temp[2].find(commentChar)]
            self.endLineComment = temp[2].strip()
        elif len(temp) != 2:
            raise ParseException()
        
        self.optionName = temp[0]
        self.optionValue = temp[1]
    
    def __str__(self, commentOut=None):
        _str = ""
        if self.isCommentedOut:
            _str += self.commentChar
        _str += self.optionName + self.assignChar + self.optionValue + self.endLineCommentWhitespace + self.endLineComment
        return _str


def changeConfig(_file, newData, commentChar='#', assignChar=' ', sectionStart=None, sectionEnd=None):
    """ Changes a config file line in the format '#OptionName foo' (format can be changed with parameters) under specified section.
        
        newData:        New config file string to write to file, between sectionStart and sectionEnd.
                        It can end or begin with a new line to write an entire line to file.
        sectionStart:   ex. "\n[logging]"
                        A new line may be present at the beginning of the string only
        sectionEnd:     ex. "\n[" (end of section may also be indicated by reaching end of file)
                        A new line may be present at the beginning of the string only
        
        Returns a list of all the following that apply:
            0    If setting name was encountered in the file and it was uncommented
            1    If setting name was encountered in the file and it was commented out
            2    If setting name and value were added by this function
            3    If setting value was changed by this function """
    newData = ConfigLine(newData, commentChar, assignChar)
    sectionStartRe = re.compile(re.escape(sectionStart))
    sectionEndRe = re.compile(re.escape(sectionEnd))
    commentCharRe = re.compile(re.escape(commentChar))
    
    returnCode = []
    sectionPos = [None, None]   # [begin, end] ,  -1 in index 0 if startPos was on a previous line
    inSection = False
    for line in fileinput.input(_file, inplace=1):
        reMatch = commentCharRe.search(line)
        commentPos = reMatch.start()
        reMatch = sectionStartRe.search("\n" + line, endpos=commentPos)
        sectionPos[0] = reMatch.start()
        reMatch = sectionEndRe.search("\n" + line, endpos=commentPos)
        sectionPos[1] = reMatch.start()
        
        if newData[0] == "\n":
            # look for 
        if sectionStartPos != None sectionEndPos != None
            if "\n" + line:
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
            continue    # don't write line
        
        if newLine.endLineComment == "" and parsedOldLine.endLineComment != "":
            newLine.endLineComment = parsedOldLine.endLineComment
            newLine.endLineCommentWhitespace = parsedOldLine.endLineCommentWhitespace
        
        sys.stdout.write(str(newLine))    # writes new line in place of old line
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


