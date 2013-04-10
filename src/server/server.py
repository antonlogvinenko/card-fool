import BaseHTTPServer
import cgi_http_server
import game_server
import sys

#Global variable game_server
game_server = game_server.Game_Server()


class ClientsRequestHandler(cgi_http_server.CGIHTTPRequestHandler):
    '''Inheriting from modified class CGIHTTPRequestHandler.
    Output of all cgi scripts are handled by handle_cgi_output.
    Returning value of this function is sent to the client
    as the response.
    '''
    def handle_cgi_output(self, command):
        '''Takes instance of class Client_Command representing parsed
        command received from the client
        '''
        print '\n', command
        response = game_server.handle_command(command)
        print '\n', response
        return response


def run(server_class, handler_class):
    '''Runs a server of 'server_class' class
    with a HTTP handler of 'handler_class' class.
    '''
    if "test" in sys.argv:
        game_server.set_test_mode()
    server_address = ('localhost', 80)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


#Running server
run(BaseHTTPServer.HTTPServer, ClientsRequestHandler)