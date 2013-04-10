import re
import sys
import os
import server_parser
import client_parser
import server_response
import client_command
import requestor
import client_generator


class Logic_Tester:
    def __init__(self):
        self.s_parser = server_parser.Server_Parser()
        self.c_parser = client_parser.Client_Parser()
        self.requestor = requestor.Requestor("localhost", "/cgi-bin/commands.py")
        self.c_generator = client_generator.Client_Generator()
        self.test_name = ""
        self.uid_map = {}
        self.players = {}
        self.game_uid = 0
        self.game_record = []
    def end_working(self):
        for file in self.players.values():
            file.close()
        self.test_name = ""
        self.uid_map = {}
        self.players = {}
        self.game_record = []
    def get_command_response(self, file):
        command = file.readline()
        if not 'command' in command:
            return None
        line = ""
        response = "\n"
        while line != "\n":
            line = file.readline()
            response += line
        return (command[:-1], response[1:-2])
    def next_command_response(self, name):
        command_response = self.get_command_response(self.players[name])
        if command_response == None:
            return None
        cmd = self.s_parser.parse_command(command_response[0])
        while cmd.get_type() in ['getGameStatus', 'getListOfGames']:
            command_response = self.get_command_response(self.players[name])
            cmd = self.s_parser.parse_command(command_response[0])
        return command_response
    def get_files(self):
        for file in os.listdir(os.getcwd()):
            if file.endswith(".log"):
                self.game_record.append(open(file, 'r'))
    def register(self):
        mem = {}
        for log in self.game_record:
            command, response = self.get_command_response(log)
            reg = int(self.c_parser.parse_response(response).get_uid())
            mem[reg] = (command, response, log)
        for uid in mem.keys():
            name = self.s_parser.parse_command(mem[uid][0]).get_name()
            got_response = self.requestor.make_request(mem[uid][0])
            response = self.c_parser.parse_response(got_response)
            if response.get_status():
                new_uid = response.get_uid()
                old_uid = self.c_parser.parse_response(mem[uid][1]).get_uid()
                self.uid_map[uid] = int(new_uid)
                self.players[name] = mem[uid][2]
            else:
                raise Error("Registration", name, mem[uid][0], mem[uid][1], got_response)
        self.game_uid = self.uid_map.keys()[0]
    def create_join(self):
        mem = {}
        for name in self.players.keys():
            command, response = self.next_command_response(name)
            if self.s_parser.parse_command(command).get_type() == "createGame":
                got_response = self.requestor.make_request(command)
                if got_response != response:
                    raise Error("create", name, command, response, got_response)
            else:
                mem[name] = (command, response)
        for name in mem.keys():
            got_response = self.requestor.make_request(mem[name][0])
            if got_response != mem[name][1]:
                raise Error("join", name, mem[name][0], mem[name][1], got_response)
    def run_other_commands(self):
        response = self.c_parser.parse_response(self.requestor.make_request(
                                self.c_generator.get_game_status(self.game_uid)))
        end_game = False
        while response.get_status() and not end_game:
            for player in response.get_all_players_info():
                if player.get_status() == '_fool_':
                    end_game = True
                    break
            if not end_game:
                for player in response.get_all_players_info():
                    if player.is_active():
                        self.run_next_player_command(player.get_name())
                response = self.c_parser.parse_response(self.requestor.make_request(
                            self.c_generator.get_game_status(self.game_uid)))
        #Here: for each player, execute quit
        response = self.c_parser.parse_response(self.requestor.make_request(
                            self.c_generator.get_game_status(self.game_uid)))
        for player in response.get_all_players_info():
            if player != None:
                self.run_all_next_player_commands(player.get_name())
    def run_next_player_command(self, name):
        command_response = self.next_command_response(name)
        if command_response == None:
            return False
        got_response = self.requestor.make_request(command_response[0])
        if command_response[1] != got_response:
            raise Error("Commands", name, command_response[0], command_response[1], got_response)
        return True
    def run_all_next_player_commands(self, name):
        success = self.run_next_player_command(name)
        while success:
            success = self.run_next_player_command(name)
    def run_test(self):
        self.get_files()
        self.register()
        self.create_join()
        self.run_other_commands()
        while len(self.players.keys()) != 0:
            self.players.popitem()[1].close()
        self.game_record = []
        self.players = {}
    def run_tests(self):
        for dir in os.listdir(os.getcwd()):
            if os.path.isdir(dir):
                os.chdir(dir)
                try:
                    print "Starting in", os.getcwd()
                    self.run_test()
                    print "\t... OK\n",
                except Error, e:
                    print os.getcwd()
                    print e
                os.chdir('..')

class Error:
    def __init__(self, when, name, command, response='', got_response=''):
        self._when = when
        self._name = name
        self._response = response
        self._command = command
        self._got_response = got_response
    def __str__(self):
        str = "Error in " + self._when + " with player " + self._name
        str += "\nCommand:\n"
        str += self._command
        str += "\nExpected response:\n"
        str += self._response
        str += "\nGot response:\n"
        str += self._got_response
        return str
    def __repr__(self):
        return self.__str__()

Logic_Tester().run_tests()