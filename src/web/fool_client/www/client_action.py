from spyceModule import spyceModulePlus
import requestor
import client_generator
import client_parser
import ai



class client_action(spyceModulePlus):
    def initialize(self):
        self._requestor = requestor.Requestor()
        self._parser = client_parser.Client_Parser()
        self._generator = client_generator.Client_Generator()
	self._ai = ai.Ai()
        all_fields = ['uid', 'name', 'host', 'status', 'reg', 'registration_status',
                'join_status', 'create_game_status', 'server_error', 'message', 'join',
                'action_status', 'action_message', 'using_ai']
        for x in all_fields:
            self.modules.session[x] = ''
    def register(self, name):
        resp = self._parser.parse_response(
            self._requestor.make_request(self._generator.register(name)))
        self._ai.set_uid(resp.get_uid())
        return resp

    def init_requestor(self, host, script):
        self._requestor.set_host(host)
        self._requestor.set_script(script)
        self._ai.set_requestor(self._requestor)

    def join_game(self, uid, name):
        response = self._requestor.make_request(self._generator.join_game(uid, name))
        return self._parser.parse_response(response)
        
    def skip(self, uid):
        return self._parser.parse_response(
            self._requestor.make_request(self._generator.skip(uid)))
        
    def quit(self, uid):
        return self._parser.parse_response(
            self._requestor.make_request(self._generator.quit(uid)))

    def take(self, uid):
        return self._parser.parse_response(
            self._requestor.make_request(self._generator.take(uid)))

    def get_list_of_games(self):
        return self._parser.parse_response(
            self._requestor.make_request(self._generator.get_games_list()))

    def cover(self, uid, cards):
        return self._parser.parse_response(
                self._requestor.make_request(self._generator.cover(uid, cards)))

    def attack(self, uid, cards):
        return self._parser.parse_response(
                self._requestor.make_request(self._generator.attack(uid, cards)))
    
    def retransfer(self, uid, cards):
        return self._parser.parse_response(
                self._requestor.make_request(self._generator.retransfer(uid, cards)))

    def create_game(self, uid, name, players_num,
                    retransfer, first_attack5, attack6):
        return self._parser.parse_response(self._requestor.make_request(
                    self._generator.create_game(uid, name, players_num,
                                            retransfer, first_attack5, attack6)))
    
    def get_game_status(self, uid, using_ai):
        resp = self._parser.parse_response(
            self._requestor.make_request(self._generator.get_game_status(uid)))
        if using_ai and resp.get_status() and resp.game_continues():
            self._ai.think(resp)
            if resp.get_my_info().is_active() and resp.game_continues():
               self._ai.generate_strategy() 
               resp = self._parser.parse_response(
                    self._requestor.make_request(self._generator.get_game_status(uid)))
               if resp.get_status() and resp.game_continues():
                   self._ai.think(resp)
        return resp

    def set_host(self, host):
        self.modules.session['host'] = host
    
    def set_script(self, script):
        self.modules.session['script'] = script
    
    def set_name(self, name):
        self.modules.session['name'] = name
    
    def set_server_error(self, error):
        self.modules.session['server_error'] = error
    
    def set_server_message(self, message):
        self.modules.session['server_message'] = message
    
    def set_create_game_status(self, status):
        self.modules.session['create_game_status'] = status
    
    def set_registration_status(self, status):
        self.modules.session['registration_status'] = status

