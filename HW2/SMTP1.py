# MJ Gomez-Saavedra (PID:730270625)
# Honor Pledge: I herby pledge that no disallowed help was received in my complition of this assignment.
import sys
import os
from parser import parseMail, parseRCPT, parseData, parseDataCmd, parseMailFromCmd, parseRCPTtoCmd, getEmail


# gets the actual message to be created in txt.file
def getMessageCmd(cmd):
    message = []   
    while True:
        line = sys.stdin.readline()
        if line != ".\n":
            message.append(line)
            sys.stdout.write(line) 
        else:
            sys.stdout.write(".\n")
            return message

# makes msg file within the ./forward/ folder
def makeMsgFile(send, rcptA, msg):
    if not os.path.exists('forward'):
        os.makedirs('forward')
    for r in rcptA:
        m = open('./forward/' + r, 'a+')
        m.write('From: <' + send + '>' + '\n')
        for r1 in rcptA:
            m.write('To: <' + r1 + '>' + '\n')
        for line in msg: #list
            m.write(line)
    m.close

    # if not os.path.exists('forward'):
    #     os.makedirs('forward')
    # for r in rcptA:
    #     m = open('./forward/' + r, 'a+')
    #     m.write('From: <' + send + '>' + '\n')
    #     for r1 in rcptA:
    #         m.write('To: <' + r1 + '>' + '\n')
    #     for line in msg:
    #         m.write(line)
    # m.close

    # # check if forward exists
    # if not os.path.exists('forward'):
    #     os.makedirs('forward')
    
    # # if <rp> file doesn't
    
    
# response codes for main function
def responseCodes(n):
    if n == 0:
        return '250 OK'

    if (n == 1) or (n == 2) or (n == 3):
        return '500 Syntax error: command unrecognized'

    if (n == 4) or (n == 5) or (n == 6) or (n == 7) or (n == 8) or (n == 9) or (n == 10) or (n == 11) or (n == 12) or (n == 13) or (n == 14) or (n == 15) or (n == 16) or (n == 17) or (n == 18) or (n == 19) or (n == 20):
        return '501 Syntax error in parameters or arguments'

    if n == 21:
        return '354 Start mail input; end with <CRLF>.<CRLF>'

    if n == 22:
        return '503 Bad sequence of commands'



# -------- MAIN CALL -----------------
hasMail = False
hasRcpt = False
rcptArray = []
while True:
    cmd = sys.stdin.readline()
    sys.stdout.write(cmd) #echo
    # sys.stdout.write(responseCodes(parseMailFromCmd(cmd)) + '\n') #works
    # sys.stdout.write(str(parseMailFromCmd(cmd))+ '\n')
    # sys.stdout.write(str(parseRCPTtoCmd(cmd))+ '\n')
    # sys.stdout.write(str(parseDataCmd(cmd))+ '\n')

    #initial check for syntax errors:
    # if ((parseMailFromCmd(cmd) == 1 or 2 or 3) or (parseRCPTtoCmd(cmd) == 1 or 2 or 3) or (parseDataCmd(cmd) == 1 or 2 or 3)):
    #     sys.stdout.write(responseCodes(1) + '\n')
    
    if (parseMail(cmd[0:4]) == 0): #"MAIL"
        if ((parseMailFromCmd(cmd) == 1) or (parseMailFromCmd(cmd) == 2) or (parseMailFromCmd(cmd) == 3)): #500
            sys.stdout.write(responseCodes(1) + '\n')
        else:
            if hasMail:
                sys.stdout.write(responseCodes(22) + '\n') #503: out of order  
            else:
                if (parseMailFromCmd(cmd) != 0):
                    sys.stdout.write(responseCodes(parseMailFromCmd(cmd)) + '\n')
                else:
                    sender = getEmail(cmd)
                    hasMail = True
                    sys.stdout.write(responseCodes(parseMailFromCmd(cmd)) + '\n')
    elif (parseRCPT(cmd[0:4]) == 0): #"RCPT"
        if ((parseRCPTtoCmd(cmd) == 1) or (parseRCPTtoCmd(cmd) == 2) or (parseRCPTtoCmd(cmd) == 3)):#500
            sys.stdout.write(responseCodes(1) + '\n')
        else:
            if not hasMail:
                sys.stdout.write(responseCodes(22) + '\n') #503: out of order
            else:
                if (parseRCPTtoCmd(cmd) != 0):
                    sys.stdout.write(responseCodes(parseRCPTtoCmd(cmd)) + '\n')
                else:
                    rcptArray.append(getEmail(cmd))
                    hasRcpt = True
                    sys.stdout.write(responseCodes(parseRCPTtoCmd(cmd)) + '\n')
    elif (parseData(cmd[0:4]) == 0): #"DATA"
        if not hasRcpt:
            sys.stdout.write(responseCodes(22) + '\n') #503: out of order
        else:
            if (parseDataCmd(cmd) != 0):
                sys.stdout.write(responseCodes(parseDataCmd(cmd)) + '\n')
            else:
                sys.stdout.write(responseCodes(21) + '\n') #data input
                message = getMessageCmd(cmd)
                #print("sender: " + sender)
                #print("message: " + str(message))
                #print("rcptArray: "+ str(rcptArray))
                # print("made msg file")
                makeMsgFile(sender, rcptArray, message)
                hasMail = False
                hasRcpt = False
                sender = ""
                rcptArray = []
                message = []
                sys.stdout.write(responseCodes(parseDataCmd(cmd)) + '\n')
    else: #500: syntax
        sys.stdout.write(responseCodes(1) + '\n')
