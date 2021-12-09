import sys
import os
from parser import *
from socket import *

er500 = '500 Syntax error: command unrecognized'
er501 = '501 Syntax error in parameters or arguments'
er503 = '503 Bad sequence of commands'

def startServer():
    if len(sys.argv) != 2:
        sys.stdout.write('Error, expected two arguments\n')
        return
    
    serv_port = int(sys.argv[1])

    #socket setup:
    serv_socket = socket(AF_INET, SOCK_STREAM) 
    serv_socket.bind(('', serv_port))
    serv_socket.listen(1) #not sure if this should be 1 or 5
    # print("Server is ready to receive data...")

    while True:
        # print("here")
        connectionSocket, addr = serv_socket.accept()
        # print("The socket has succesfully connected...")
        #220 server greeting
        # greeting = '220 comp431fa21.cs.unc.edu'
        greeting = '220 ' + gethostname()
        # print(greeting)
        connectionSocket.send(greeting.encode())
        # print("Greeting sent to client")

        #await for HELO from client
        awaitHELO = False


        # DO A WHILE TRUE (big outer one), INSIDE DO A WHILE NOT QUIT. 
        while not awaitHELO:
            # print(awaitHELO)
            rcvHELO = connectionSocket.recv(1024).decode()
            # print("Helo recevied..." + rcvHELO) 
            validHELO = parseHELO(rcvHELO)
            # print("____valid helo: " + str(validHELO))

            if validHELO == True:
                # print("____await helo: " + str(awaitHELO))
                # print("____valid helo: " + str(validHELO))
                awaitHELO = True
                ackmsg = '250 Hello ' + getDomain(rcvHELO)+ ' pleased to meet you' #check
                connectionSocket.send(ackmsg.encode())
                # print("Ack sent to client...")
        
        #process emails
        state = 0
        sender = ''
        receivers = []
        msgs = []
        
        receivedQuit = False
        # print('Server is ready to receive...')
        mademsg = False

        while not receivedQuit:
            inputstr = connectionSocket.recv(1024).decode()
            #print(inputstr)
            # print(state)
            if inputstr == 'QUIT\n':
                receivedQuit = True
            else:
                if state == 0:
                    fromstr = responseCodes(parseMailFromCmd(inputstr))
                    # print("fromstr: " + fromstr)
                    if fromstr == '250 OK':
                        state = 1
                        sender = getAddy(inputstr)
                        rsp = fromstr + '\n'
                        connectionSocket.send(rsp.encode())
                    else:
                        tostr = responseCodes(parseRCPTtoCmd(inputstr))
                        datastr = responseCodes(parseDataCmd(inputstr))
                        state = 0
                        sender = ''
                        receivers = []
                        msgs = []
                        if (tostr == er500 or fromstr == er500 or datastr == er500):
                            rsp = er500
                            connectionSocket.send(rsp.encode())
                        elif (fromstr == er501):
                            rsp = er501
                            connectionSocket.send(rsp.encode())
                        else:
                            rsp = er503
                            connectionSocket.send(rsp.encode())
                        
                elif state == 1:
                    tostr = responseCodes(parseRCPTtoCmd(inputstr))
                    # print("tostr: " + tostr)
                    if tostr == '250 OK':
                        state = 2
                        receivers.append(getAddy(inputstr))
                        rsp = tostr + '\n'
                        connectionSocket.send(rsp.encode())
                    else:
                        fromstr = responseCodes(parseMailFromCmd(inputstr))
                        datastr = responseCodes(parseDataCmd(inputstr))
                        state = 0
                        sender = ''
                        receivers = []
                        msgs = []
                        if (tostr == er500 or fromstr == er500 or datastr == er500):
                            rsp = er500
                            connectionSocket.send(rsp.encode())
                        elif (tostr == er501):
                            rsp = er501
                            connectionSocket.send(rsp.encode())
                        else:
                            rsp = er503
                            connectionSocket.send(rsp.encode())

                elif state == 2:
                    tostr = responseCodes(parseRCPTtoCmd(inputstr))
                    # print("tostr: " + tostr)
                    if tostr == '250 OK':
                        receivers.append(getAddy(inputstr))
                        rsp = tostr + '\n'
                        connectionSocket.send(rsp.encode())
                    else:
                        datastr = responseCodes(parseDataCmd(inputstr))
                        # print("datastr: " + datastr)
                        if datastr == '250 OK':
                            state = 3
                            rsp = '354 Start mail input; end with <CRLF>.<CRLF>\n'
                            connectionSocket.send(rsp.encode())
                        else:
                            state = 0
                            sender = ''
                            receivers = []
                            msgs = []
                            rsp = responseCodes(parseMailFromCmd(inputstr))
                            # print(rsp)
                            connectionSocket.send(rsp.encode())

                elif state == 3:
                    enddatastr = responseCodes(isEndData(inputstr))
                    # print("enddatastr: " + enddatastr)
                    # print("end data func: ", isEndData(inputstr))
                    # print("data msgs: ", inputstr)
                    if enddatastr == '250 OK':
                        if len(inputstr) > 2:
                            if (inputstr[-1] == '\n' and inputstr[-2] == '.' and inputstr[-3] == '\n'):
                                msgs.append(inputstr[:-2])
                                # print("msgs: " + str(msgs))
                       
                        makeMsgFile(sender, receivers, msgs)
                        rsp = enddatastr + '\n'
                        connectionSocket.send(rsp.encode())
                        state = 0
                        sender = ''
                        receivers = []
                        msgs = [] 
                    else:
                        msgs.append(inputstr)
                else:
                    sys.stderr.write("this is broken" + '\n')
               

        closingMessage = '221 ' + gethostname() + ' closing connection'
        connectionSocket.send(closingMessage.encode())
        



#=============================  HELPER FUNCTIONS 
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
    m = 'From: <' + send + '>\n'

    m += 'To: '

    subA = []
    for r in rcptA:
        subA.append('<' + r + '>')
    st = ",".join(subA)
    m += st + '\n'  
    
    for ms in msg:
        m += ms
    domains = set(())
    for email in rcptA:
        domains.add(email.split("@")[1])
    for r in domains:
        with open('./forward/' + r, 'a+') as f:
            f.write(m)

def getafterAt(s):
    index = s.index('@')
    newstr = s[(index+1):]
    return newstr

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

def getAddy(cmd):
	L_index = cmd.find('<')
	R_index = cmd.find('>')

	return cmd[L_index+1:R_index]

#=============================  FUNCTION CALL 
startServer()
