'''Contains definition of class Server_Generator.
'''
import string


class Server_Generator:
    '''Used for creating server's responses.
    '''
    def __init__(self):
        self.IN_DELIM = ':'
        self.OUT_DELIM = '\n'
    def _status_message(self, status, message):
        '''Common function for responses that require only
        2 fields: status and message.
        '''
        return self.OUT_DELIM.join([
                                    self.IN_DELIM.join(['status',  self._bool_to_str(status)]),
                                    self.IN_DELIM.join(['message', message])
                                    ])
    def _bool_to_str(self, bool):
        '''Convert boolean data according to responses' specification.
        '''
        if bool:
            return 'ok'
        return 'fail'
    def _param_encl(self, param):
        return '{' + param + '}'
    '''Creating responses methods follow.
    '''
    def _game_name_encl(self, name):
        '''Returns 'game:name'.
        '''
        return 'game:\"' + name + '\"'
    def _name_encl(self, name):
        '''Returns '(name)'
        '''
        return '('  + name + ')'
    def _game_info(self, game_name, game):
        '''Compiles a string with game's description.
        '''
        info = [self._game_name_encl(game_name)]
        names = []
        for player in game.get_players():
            names.append(player.get_name())
        names.sort()
        info.extend([self._name_encl(name) for name in names])
        info.append(game.get_options())
        return ''.join(info)
    def _players_info(self, players, recipient_uid):
        '''Compiles a string with information about players.
        Recipient_uid is uid of the player to whome the
        response is sent.
        '''
        info = []
        for order in range(1, players.get_number_of_players() + 1):
            pl_info = ''
            player = players.get_by_order(order)
            pl_info += 'player:' + str(order)
            pl_info += self._name_encl(player.get_name())
            pl_info += player.get_status()
            uid = players.get_player_uid(player)
            if recipient_uid == uid:
                pl_info += player.get_cards_str()
            else:
                pl_info += player.get_number_of_cards_str()
            info.append(pl_info)
        info.append('active:' + str(players.get_active_player()))
        return '\n'.join(info)
    def list_of_games_response(self, games):
        '''Compiles a string with games' description.
        '''
        names = games.get_game_names()
        return '\n'.join([
                   self._game_info(name, games[name]) for name in names
                   ])
    def register_response(self, status, message, uid):
        '''Creates response on registration request.
        '''
        return self.OUT_DELIM.join([
                                    self._status_message(status, message),
                                    self.IN_DELIM.join(['uid', str(uid)])
                                    ])
    def create_game_response(self, status, message):
        '''Creates response on registration request.
        '''
        return self._status_message(status, message)
    def join_game_response(self, status, message):
        '''Creates response on registration request.
        '''
        return self._status_message(status, message)
    def get_game_status_response(self, status, message,
                                 game_name, game, recipient_uid):
        '''Creates response on registration request.
        '''
        if status:
            return '\n'.join([
                       self._status_message(status, message),
                       'game:' + game_name,
                       'table:' + game.get_table_str(),
                       'deck:' + game.get_deck_str(),
                       'trump:' + game.get_trump_str(),
                       'out:' + game.get_out_str(),
                       'options:' + game.get_options(),
                       self._players_info(game.get_players_hash(), recipient_uid)
                       ])
        return self._status_message(status, message)
    def attack_response(self, status, message):
        '''Creates response on attack request.
        '''
        return self._status_message(status, message)
    def cover_response(self, status, message):
        '''Creates response on cover request.
        '''
        return self._status_message(status, message)
    def take_response(self, status, message):
        '''Creates response on take request.
        '''
        return self._status_message(status, message)
    def retransfer_response(self, status, message):
        '''Creates response on retransfer request.
        '''
        return self._status_message(status, message)
    def quit_response(self, status, message):
        '''Creates response on quit request.
        '''
        return self._status_message(status, message)
    def skip_response(self, status, message):
        '''Creates response on skip request.
        '''
        return self._status_message(status, message)
    def restart_response(self, status, message):
        '''Creates response on restart request.
        '''
        return self._status_message(status, message)