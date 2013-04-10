'''
This script takes clients commands, parses them.
Resulting command object is packed and returned to the server.
'''

import server_parser
import pickle
import cgi

parser = server_parser.Server_Parser()
#parse a command from client:
parsed_command = parser.parse_cgi_input()
#pack parsed command and output it:
print pickle.dumps(parsed_command)