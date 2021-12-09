# This file contains all the functions to recognize or not STMP codes like "MAIL FROM", "RCPT TO", "DATA"

# returns true if grammar is in correct format
# <From> ::= "From: " <reverse-path> <CRLF>
def isFrom(code):
    if (len(code) < 6):
        return -1
    
    if (code[0:6] != 'From: '):
        return -1
    
    code = code[6:]
    endRP = getEndRP(code)
    checkRP = parseReversePath(code[0:endRP+1])
    if (checkRP != 0):
        return -1
    
    code = code[endRP+1:]
    if (parseCRLF(code) == False):
        return -1
    
    # "Sender ok"
    return 2

# returns true if grammar is in correct format
# <rcpt-to-cmd> ::= "To: "<forward-path> <CRLF>
def isTo(code):
    if (len(code) < 4):
        return -1
    
    if (code[0:4] != 'To: '):
        return -1
    
    code = code[4:]
    endRP = getEndRP(code)
    checkRP = parseReversePath(code[0:endRP+1])
    if (checkRP != 0):
        return -1
    
    code = code[endRP+1:]
    if (parseCRLF(code) == False):
        return -1
    
    # "Sender ok"
    return 2



# <data-cmd> ::= “DATA” <nullspace> <CRLF>
def parseDataCmd(code):
    # "DATA"
    checkData = parseData(code[0:4])
    if (checkData != 0):
        return checkData
    
    # <nullspace> <CRLF>
    code = code[4:]
    for i in code:
        if (parseCRLF(i) == False):
            if (parseNullspace(i) != 0):
                return 4
            else:
                continue
        else:
            continue
    
    # sender ok
    return 0

# <mail-from-cmd> :== "MAIL" <whitespace> "FROM:" <nullspace> <reversepath> <nullspace> <CRLF>
def parseMailFromCmd(code):
    # "MAIL"
    checkMail = parseMail(code[0:4])
    if (checkMail != 0):
        return checkMail

    # <whitespace>
    code = code[4:]
    endWS = getEndWS(code, 'F')
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

# <rcpt-to-cmd> ::= “RCPT” <whitespace> “TO:” <nullspace> <forward-path> <nullspace> <CRLF>
def parseRCPTtoCmd(code):
    # "RCPT"
    checkRCPT = parseRCPT(code[0:4])
    if (checkRCPT != 0):
        return checkRCPT

    # <whitespace>
    code = code[4:]
    endWS = getEndWS(code, 'T')
    if (endWS < 0):
        if (endWS == -3): 
            return 1
        else:
            return 2
    else: 
        checkWhiteSpace = parseWhitespace(code[0:endWS])
        if (checkWhiteSpace != 0):
            return checkWhiteSpace

    # "TO:"
    code = code[endWS:]
    checkTO = parseTO(code[0:5])
    if (checkTO != 0):
        return checkTO
    
    # <nullspace>
    code = code[3:] #check this number
    endNS1 = getEndNS(code)
    if (endNS1 < 0):
        return 4
    else:
        if (endNS1 > 0):
            checkNullSpace = parseNullspace(code[0:endNS1])
            if (checkNullSpace != 0):
                 return checkNullSpace
    
    # <forward-path>
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

def getEndRP(st):
    for char in st:
        if (char == '>'):
            return st.index(char)
    return -7

def getEndNS(st):
    for char in st:
        if (char == '<'):
            return st.index(char)
        elif ((parseNull(char) == True) or (parseSpace(char) == 0)):
            continue
        else:
            return -6
            
def getEndWS(st, x):
    for char in st:
        if (parseSpace(char)!= 0) and (st.index(char) == 0):
            return -5
        
        if (parseSpace(char)!= 0) and (char == x):
            return st.index(char)
        elif (parseSpace(char) != 0) and (char != x):
            return -3
        else:
            continue

# "DATA"
def parseData(x):
    if ((x[0] == 'D') and (x[1] == 'A') and (x[2] == 'T') and (x[3] == 'A')):
        return 0
    else:
        return 1

# "MAIL" 
def parseMail(x):
    if ((x[0] == 'M') and (x[1] == 'A') and (x[2] == 'I') and (x[3] == 'L')):
        return 0
    else:
        return 1

# "FROM:"  
def parseFrom(x):
    if ((x[0] == 'F') and (x[1] == 'R') and (x[2] == 'O') and (x[3] == 'M') and (x[4] == ':')):
        return 0
    else:
        return 1

# "RCPT"
def parseRCPT(x):
    if ((x[0] == 'R') and (x[1] == 'C') and (x[2] == 'P') and (x[3] == 'T')):
        return 0
    else:
        return 1

# "TO:"
def parseTO(x):
    if ((x[0] == 'T') and (x[1] == 'O') and (x[2] == ':')):
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

# used in get sender and get recipient-- returns direct path
def getEmail(s):
    s = s[s.index('<') + 1 :]
    s = s[0:s.index('>')]
    return s
