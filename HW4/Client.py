import sys
import os, os.path
from parser import *
from socket import *

#takes in a host name, port number
def startClient():
    if len(sys.argv) != 3:
        sys.stdout.write('Expected 3 arguments\n')
        return
    
    servName = sys.argv[1]
    servPort = int(sys.argv[2])

    # Get from line
    sys.stdout.write("From:\n")
    from_line = sys.stdin.readline()
    while not isValidEmail(from_line):
        sys.stdout.write("Invalid email in From, try again.\n")
        sys.stdout.write("From:\n")
        from_line = sys.stdin.readline()
    
    from_line = from_line.strip(' \n\t')

    # Get to line
    sys.stdout.write("To:\n")
    to_line = sys.stdin.readline()
    while not areValidEmails(to_line):
        sys.stdout.write("Invalid email(s) in To, try again.\n") 
        sys.stdout.write("To:\n")
        to_line = sys.stdin.readline()
    
    to_line = [x.strip(' \n\t') for x in to_line.split(',')] #check this!
    # print(to_line)

    # Get subject line
    sys.stdout.write("Subject:\n")
    subj_line = sys.stdin.readline()

    # Get Message-Body line
    sys.stdout.write("Message:\n")
    msg_body = ""

    isEnd = False
    while not isEnd:
        msg = sys.stdin.readline()
        if (msg != ".\n" and msg != "."):
            msg_body += msg
        else:
            isEnd = True
    # print("<<<" + msg_body + ">>>")
    # print(isEnd)

    # SOCKET:
    cli_socket = socket(AF_INET, SOCK_STREAM)
    # print(servName)
    # print(servPort)
    try:
        cli_socket.connect((servName, servPort))
    except:
        sys.stdout.write('Failed server connection...\n')
    
    greeting = cli_socket.recv(1024).decode()
    # print("Greeting received.... " + greeting)

    helo_msg = 'HELO ' + gethostname() + '\n'
    cli_socket.send(helo_msg.encode())
    # print("Helo sent.... ")

    ack_msg = cli_socket.recv(1024).decode()
    # print("Ack received...." + ack_msg)

    ### TRANSMISSION ###
    # From
    from_msg = 'MAIL FROM: <' + from_line + '>'
    # print("from msg: " + from_msg)

    cli_socket.send(from_msg.encode())
    from_rsp = cli_socket.recv(1024).decode()
    # print("from rsp: " + from_rsp)

    # To
    to_msg_array = getToMsgArray(to_line)

    for to_msg in to_msg_array:
        # print("to msg: " + to_msg)
        cli_socket.send(to_msg.encode())
        to_rsp = cli_socket.recv(1024).decode()
        # print("to rsp: " + to_rsp)
    
    # Data 
    ### HEAD
    data_head = 'DATA \n'
    # print("data header: " + data_head)
    cli_socket.send(data_head.encode())
    data_head_rsp = cli_socket.recv(1024).decode()
    # print("data header rsp: " + data_head_rsp)

    data_msg_array = getDataMsgs(from_line, to_line, subj_line, msg_body)
    for data_msg in data_msg_array:
        cli_socket.send(data_msg.encode())
        # print("data msg sent.")
    
    ### FOOT
    data_foot = '.\n'
    # print("data footer: " + data_foot)
    cli_socket.send(data_foot.encode())
    data_rsp = cli_socket.recv(1024).decode()
    # print("data rsp: " + data_rsp)

    # Quit
    quit_msg = 'QUIT\n'
    # print("Quit msg: " + quit_msg)
    cli_socket.send(quit_msg.encode())
    quit_ack = cli_socket.recv(1024).decode()
    # print("Quit Ack: " + quit_ack)

    cli_socket.close()

def getDataMsgs(from_line, to_line, subj_line, msg_body):
    msg_array = []

    msg_array.append('Subject: ' + subj_line)
    msg_array.append('\n') #check

    msg_array.append(msg_body)

    # print(msg_array)
    return msg_array

def getToMsgArray(st):
    m = []

    for r in st:
        m.append('RCPT TO: <' + r + '>')
    
    return m

def isValidEmail(st):
    st = st.strip(' \n\t')
    return parseMailbox(st) == 0

def areValidEmails(st):
    addys = st.split(',')
    for addy in addys:
        if not isValidEmail(addy):
            return False
    return True



startClient()
