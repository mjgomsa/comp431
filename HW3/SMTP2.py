# MJ Gomez-Saavedra (PID:730270625)
# Honor Pledge: I herby pledge that no disallowed help was received in my complition of this assignment.

import sys
import os, os.path
from parser import isFrom, isTo, getEndWS, parseChar, parseWhitespace, findOccurances, parseSpace


def parseFwdFile():
    forwardPath = sys.argv[1]
    Lines = None
    stateMachine = 1

    # check existance of file
    if (os.path.exists(forwardPath)):
        f = open(forwardPath, "r")
        Lines = f.readlines()
    else:
        print("The file " + forwardPath + " does not exist.")
        sys.exit()


    for line in Lines:
        # print("--------State: " + str(stateMachine))
        if (stateMachine == 1):
            if (isFrom(line) > 0):
                sys.stdout.write("MAIL FROM: " + line[6:])
                stateMachine = 2
            else:
                sys.exit()
        elif (stateMachine == 2):
            if (isTo(line) > 0):
                sys.stdout.write("RCPT TO: " + line[4:])
                stateMachine = 3
            else:
                sys.exit()
        elif (stateMachine == 3):
            if (isTo(line) > 0):
                sys.stdout.write("RCPT TO: " + line[4:])
            else:
                sys.stdout.write("DATA\n")
                # expects: 354 code
                response = sys.stdin.readline()
                sys.stderr.write(response)
                validate(response, 354)
                stateMachine = 4
                
        if (stateMachine == 4):
            if (isFrom(line) > 0):
                sys.stdout.write(".\n")
                # expects: '.'
                response = sys.stdin.readline()
                sys.stderr.write(response)
                validate(response, 250)
                sys.stdout.write("MAIL FROM: " + line[6:])
                stateMachine = 2
            else:
                # print("fail, stateMachine 4")
                sys.stdout.write(line)

        if (stateMachine != 4):
            # expects: 250 code
            response = sys.stdin.readline()
            sys.stderr.write(response)
            validate(response, 250)
    # END OF FOR LOOP-------

    # ending responses
    if (stateMachine == 3):
        sys.stdout.write("DATA\n")
        #expects: 354 code
        response = sys.stdin.readline()
        sys.stderr.write(response)
        validate(response, 354)
        stateMachine = 4

    # ending with no body
    if (stateMachine == 4):
        sys.stdout.write(".\n")
        #expects: 250 code
        response = sys.stdin.readline()
        sys.stderr.write(response)
        validate(response, 250)

    # quit code
    sys.stdout.write("QUIT\n")
    sys.exit()


# helper function to compare the expected and actual results 
def validate(current, expected):
    # check response codes
    if (current[:3] != str(expected)) or (len(current) < 4):
        sys.stdout.write("QUIT\n")
        sys.exit()


    current = current[3:]

    # must have a white space rightafter response code
    if ((current[0] != ' ') and (current[0] != '\t')):
        sys.stdout.write("QUIT\n")
        sys.exit()

    #case: repcode whitespace \n
    if ((current[0] == ' ' or current[0] == '\t') and (current[1] == '\n')):
        sys.stdout.write("QUIT\n")
        sys.exit()
    
    #if current contains just white space, QUIT
    if (current.isspace()):
        sys.stdout.write("QUIT\n")
        sys.exit()


    #if current contains at least 1 printable char, OK
    current = current[1:]
    for char in current:
        if isChar(char) is False:
            sys.stdout.write("QUIT\n")
            sys.exit()
        else:
            continue
    
    if (current[-1] != '\n'):
        sys.stdout.write("QUIT\n")
        sys.exit()

    return True


def isChar(st):
    return all(ord(c) < 128 for c in st)


#main call
parseFwdFile()
