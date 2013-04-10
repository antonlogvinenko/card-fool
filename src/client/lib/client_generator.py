'''
This module contains tools for generating client's requests
(commands) to the server.
'''
import cards

class Client_Generator:
    def __init__(self):
        self.OUTER_DELIM = '&'
        self.INNER_DELIM = '='
        self._REQUIRED_FIELDS = {'register':['name'],
                                 'createGame':['uid', 'gameName', 'numberOfPlayers', 'retransfer',
                                               'firstAttack5Cards','attack6Cards'],
                                 'joinGame':['uid','gameName'],
                                 'getListOfGames':[],
                                 'getGameStatus':['uid'],
                                 'attack':['uid', 'cards'],
                                 'cover':['uid','cards'],
                                 'take':['uid'],
                                 'retransfer':['uid', 'cards'],
                                 'quit':['uid'],
                                 'skip':['uid'],
                                 'restart':['test']}
    def _create_command(self, cmd, *kwargs):
        fields = self._REQUIRED_FIELDS[cmd]
        result =  self.OUTER_DELIM.join(
                                     [self.INNER_DELIM.join(['command', cmd])] + [
                                      self.INNER_DELIM.join([fields[i], str(kwargs[i])])
                                      for i in range(len(fields)) ]
                                      )
        return result
    def _bool_to_str(self, boolean):
        if boolean:
            return 'true'
        return 'false'
    def register(self, name):
        return self._create_command('register', name)
    def create_game(self, uid, name, players_num,
                    retransfer, first_attack5, attack6):
        return self._create_command(
                                    'createGame',
                                    str(uid), str(name),
                                    str(players_num),
                                    self._bool_to_str(retransfer),
                                    self._bool_to_str(first_attack5),
                                    self._bool_to_str(attack6)
                                    )
    def join_game(self, uid, name):
        '''Creates a 'join game' command.
        '''
        return self._create_command('joinGame', uid, name)
    def get_games_list(self):
        '''Creates a 'get games list' command.
        '''
        return self._create_command('getListOfGames')
    def get_game_status(self, uid):
        '''Creates a 'get game status' command.
        '''
        return self._create_command('getGameStatus', uid)
    def attack(self, uid, send_cards):
        '''Creates an 'attack' command.
        '''
        if isinstance(send_cards, cards.Cards):
            return self._create_command('attack', uid, send_cards.get_str_repr())
        else:
            return self._create_command('attack', uid, send_cards)
    def cover(self, uid, table):
        '''Creates a 'cover' command.
        '''
        return self._create_command('cover', uid, str(table))
    def take(self, uid):
        '''Creates a 'take' command.
        '''
        return self._create_command('take', uid)
    def retransfer(self, uid, send_cards):
        '''Creates a 'retransfer' command.
        '''
        if isinstance(send_cards, cards.Cards):
            return self._create_command('retransfer', uid, send_cards.get_str_repr())
        else:
            return self._create_command('retransfer', uid, send_cards)
    def quit(self, uid):
        '''Creates a 'quit' command.
        '''
        return self._create_command('quit', uid)
    def skip(self, uid):
        '''Creates a 'skip' command.
        '''
        return self._create_command('skip', uid)