# MJ Gomez-Saavedra (PID:730270625)
# Honor Pledge: I herby pledge that no disallowed help was received in my complition of this assignment.

import sys

# <mail-from-cmd> :== "MAIL" <whitespace> "FROM:" <nullspace> <reversepath> <nullspace> <CRLF>
def parseFunc(code):
    # "MAIL"
    checkMail = parseMail(code[0:4])
    if (checkMail != 0):
        return checkMail

    # <whitespace>
    code = code[4:]
    endWS = getEndWS(code)
    if (endWS < 0):
        if (endWS == -3): #if next char isnt 'F'
            return 1
        else:
            return 2
    else: 
        checkWhiteSpace = parseWhitespace(code[0:endWS])
        if (checkWhiteSpace != 0):
            return checkWhiteSpace
    
    # "FROM"
    code = code[endWS:]
    checkFrom = parseFrom(code[0:5])
    if (checkFrom != 0):
        return checkFrom

    # <nullspace>
    code = code[5:]
    endNS1 = getEndNS(code)
    if (endNS1 < 0):
        return 4
    else:
        if (endNS1 > 0):
            checkNullSpace = parseNullspace(code[0:endNS1])
            if (checkNullSpace != 0):
                return checkNullSpace
    
    # <reverse-path>
    code = code[endNS1:]
    endRP = getEndRP(code)
    checkRP = parseReversePath(code[0:endRP+1])
    if (checkRP != 0):
        return checkRP

    # <nullspace> <CRLF>
    code = code[endRP+1:]
    for i in code:
        if (parseCRLF(i) == False):
            if (parseNullspace(i) != 0):
                return 1
            else:
                continue
        else:
            continue
    
    # sender ok
    return 0


# Helper Function to get the end of the reverse-path. Returns index if succesful, or a negative number otherwise
def getEndRP(st):
    for char in st:
        if (char == '>'):
            return st.index(char)
    return -7

# Helper Function to get the end of the nullspace. Returns index if succesful, or a negative number otherwise
def getEndNS(st):
    for char in st:
        if (char == '<'):
            return st.index(char)
        elif ((parseNull(char) == True) or (parseSpace(char) == 0)):
            continue
        else:
            return -6
            
# Helper Function to get the end of the whitespace. Returns index if succesful, or a negative number otherwise
def getEndWS(st):
    for char in st:
        if (parseSpace(char)!= 0) and (st.index(char) == 0):
            return -5
        
        if (parseSpace(char)!= 0) and (char == 'F'):
            return st.index(char)
        elif (parseSpace(char) != 0) and (char != 'F'):
            return -3
        else:
            continue


# Helper function to get the response codes.
def responseCodes(n):
    if n == 0:
        return 'Sender ok'
    if n == 1:
        return 'ERROR -- mail-from-cmd'
    if n == 2:
        return 'ERROR -- whitespace'
    if n == 3:
        return 'ERROR -- SP'
    if n == 4:
        return 'ERROR -- nullspace'
    if n == 5:
        return 'ERROR -- null'
    if n == 6:
        return 'ERROR -- reverse-path'
    if n == 7:
        return 'ERROR -- path'
    if n == 8:
        return 'ERROR -- mailbox'
    if n == 9:
        return 'ERROR -- local-part'
    if n == 10:
        return 'ERROR -- string'
    if n == 11:
        return 'ERROR -- char'
    if n == 12:
        return 'ERROR -- domain'
    if n == 13:
        return 'ERROR -- element'
    if n == 14:
        return 'ERROR -- name'
    if n == 15:
        return 'ERROR -- letter'
    if n == 16:
        return 'ERROR -- let-dig-str'
    if n == 17:
        return 'ERROR -- let-dig'
    if n == 18:
        return 'ERROR -- digit'
    if n == 19:
        return 'ERROR -- CRLF'
    if n == 20:
        return 'ERROR -- special'
        
# "MAIL" 
def parseMail(x):
    if ((x[0] == 'M') and (x[1] == 'A') and (x[2] == 'I') and (x[3] == 'L')):
        return 0
    else:
        return 1

# "FROM"  
def parseFrom(x):
    if ((x[0] == 'F') and (x[1] == 'R') and (x[2] == 'O') and (x[3] == 'M') and (x[4] == ':')):
        return 0
    else:
        return 1

# <whitespace> ::= <SP> | <SP> <whitespace>  
def parseWhitespace(strng):
    count = 0 
    for i in range(len(strng)):
        count = parseSpace(strng[i])
    
    if count != 0:
        return 2
    else:
        return 0


# <SP> ::= the space or tab character
def parseSpace(char):
    if (char == ' ' or char == '\t'):
        return 0 
    else:
        return 3

# <null> :== no character
def parseNull(char):
    if (char == ''):
        return True
    else:
        return False


# <nullspace> :== <null> | <whitespace>
def parseNullspace(st):
    for char in st:
        if ((parseNull(char) is True) or (parseSpace(char) == 0)):
            return 0
        else:
            return 4

# <reverse-path> :== <path>
def parseReversePath(st):
    return parsePath(st)

# <path> :== "<" <mailbox> ">"
def parsePath(st):
    if (st.startswith('<')) and (st.endswith('>')):
        n = st[1:-1]
        if (parseMailbox(n) == 0):
            return 0
        else:
            return parseMailbox(n)
    else:
        return 7


# <mailbox> :== <local-part> "@" <domain>
def parseMailbox(st):
    if '@' not in st:
        return 8
    else:
        count = findOccurances(st, '@')
        if (len(count) > 1):
            return 8
    
        new = st.split('@')
        if (parseLocalPart(new[0]) is True):
            if (parseDomain(new[1]) is True):
                return 0
            else:
                return parseDomain(new[1])
        else:
            return 9
 

# <local-part> :== <string>
def parseLocalPart(st):
    if (st == ''):
        return 9
    else:
        return parseString(st)

# <string> :== <char> | <char> <string>
def parseString(st):
    return parseChar(st)

# <char> :== any printable ASCII except <special> or <SP>
def parseChar(st):
    for char in st:
        if ((parseSpace(char) == 0) or (parseSpecial(char) is (True))):
            return False
    return all(ord(c) < 128 for c in st)

# <domain> :== <element> | <element> "." <domain>
def parseDomain(s):
    if (s == ''):
        return 12


    if '.' not in s:
        if (parseElement(s) == 0):
            return 0
        else:
            return 12
    else:
        dotArr = findOccurances(s, '.')

        if ((s.startswith('.')) or (s.endswith('.'))): # starts or ends with dot
            return 12
        else: #somewhere in the middle
            if (checkAdjDots(s) > 0):
                return 12
            
            newArr = []
            newArr = s.split('.')
            for i in newArr:
                if (parseElement(i) != 0):
                    return 12
                else:
                    continue
            return 0

            
# Helpers for domain
def checkAdjDots(s):
    n = len(s)
    count = 0
    for i in range(1, n-1):
        if (s[i] == s[i+1]) and (s[i] == '.'):
            count += 1
    return count
        
def findOccurances(s, char):
    iPosList = []
    iPos = 0
    while True:
        try:
            iPos = s.index(char, iPos)
            iPosList.append(iPos)
            iPos += 1
        except ValueError as e:
            break
    return iPosList

# <element> :== <letter> | <name>
def parseElement(s):
    if (parseDigit(s[0]) is True):
        return 13

    if (parseName(s) == 0):
        return 0 
    else: 
        for char in s:
            if (parseLetter(char) is True):
                continue
            else:
                return 13
        return 0

# <name> :== <letter> <let-dig-str>
def parseName(s):
    if (parseLetDigStr(s) == 0):
        return 0
    else:
        for char in s:
            if (parseLetter(char) is True):
                continue
            else:
                return 14
        return 0

# <let-dig-str> :== <let-dig> | <let-dig> <let-dig-str>
def parseLetDigStr(s):
    if (parseLetDig(s) == 0):
        return 0
    else: 
        return 16

# <let-dig> :== <letter> | <digit>
def parseLetDig(s):
    for i in s:
        if ((parseLetter(i) is True) or (parseDigit(i) is True)):
            continue
        else:
            return 17
    return 0


# <digit> :== [0-9] (true or false)
def parseDigit(char):
    new = char.isdigit()
    return new

# <letter> :== A-Z and a-z (true or false)
def parseLetter(char):
    new = char.isalpha()
    return new

# <CRLF> :== newline (true or false)
def parseCRLF(char):
    if (char == '\n'):
        return True
    else:
        return False

# <special> :== "<"|">"|"("|")"|"["|"]"|"\"|"."|","|";"|":"|"@"|"""
def parseSpecial(char):
    if ((char == "<") or (char == ">") or (char == "(") or (char == ")") or (char == "[") or (char == "]") or (char == "\\") or (char == ".") or (char == ",") or (char == ";") or (char == ":") or (char == "@") or (char == "\"")):
        return True
    else:
        return False

for cmd in sys.stdin:
    sys.stdout.write(cmd)
    sys.stdout.write(responseCodes(parseFunc(cmd)) + '\n')
