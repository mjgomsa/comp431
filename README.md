# comp431
My repo for Comp431: Internet Services &amp; Protocols

## HW1
First Steps of the Construction of a Mail Server — Parsing in Python.
This program takes input strings from a "client" and evaluates if they're part of the SMTP grammar:
```
<mail-from-cmd> ::= “MAIL” <SP> “FROM:” <reverse-path> <CRLF>
<reverse-path> ::= <path>
 <path> ::= "<" <mailbox> ">"
 <mailbox> ::= <local-part> "@" <domain>
 <local-part> ::= <string>
 <string> ::= <char> | <char> <string>
 <char> ::= any one of the printable ASCII characters, but not any
 <special> or <SP>
 <domain> ::= <element> | <element> "." <domain>
 <element> ::= <letter> | <name>
 <name> ::= <letter> <let-dig-str>
 <letter> ::= any one of the 52 alphabetic characters A through Z
 in upper case and a through z in lower case
 <let-dig-str> ::= <let-dig> | <let-dig> <let-dig-str>
 <let-dig> ::= <letter> | <digit>
 <digit> ::= any one of the ten digits 0 through 9
 <CRLF> ::= the newline character
 <SP> ::= the space or tab character
 <special> ::= "<" | ">" | "(" | ")" | "[" | "]" | "\" | "."
 | "," | ";" | ":" | "@" | """
```
## HW2
Extension of the program in Homework 1 to parse more SMTP commands. Now includes “RCPT TO” and “DATA” commands. Additionally, the program processes the DATA command to receive and store the contents of a mail message in a file. Possible responses:
```
500 Syntax error: command unrecognized
501 Syntax error in parameters or arguments
503 Bad sequence of commands
354 Start mail input; end with <CRLF>.<CRLF>
250 OK
```

## HW3
This is the Server-side processing. The program reads a forward-file (from that of HW2) and generates and writes to standard output the SMTP messages necessary to send the contents of the mail messages in the forward-file to a destination SMTP server. It both generates SMTP server messages and listens for the SMTP response messages that a real server would emit. For example:
```
MAIL FROM: <mjgomsa@cs.unc.edu>
250 OK
250 OK
RCPT TO: <mj@gmail.com>
250 OK
250 OK
DATA
354 Some random response message…
354 Some random response message…
Hey! This is some random text signifying an email's body :)
.
250 OK
250 OK
```

## HW4
This program is the glue to all the previously made programs. It is made up of two programs: the SMTP “server” and the SMTP “client". As real clients and servers, these programs interoperate over a network by using a TCP socket (https://docs.python.org/3/howto/sockets.html).
In order to run these programs they need to be ran in different hosts (for instance local host '127.0.0.1' and port number 8625):
```
MacBook-Pro ~ %  python3 Client.py 127.0.0.1 8625  
MacBook-Pro ~ % python3 Server.py 8625

```
