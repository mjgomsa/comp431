# comp431
My repo for Comp431: Internet Services &amp; Protocols

## HW1
First Steps of the Construction of a Mail Server — Parsing in Python.
This program takes input strings from a "client" and evaluates if they're part of the SMTP grammar:
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
