'''Contains definition of Server_Response class.
'''
import cards

class Server_Response:
    '''
    '''
    def __init__(self, status = True, message = ''):
        '''
        '''
        self._status = status
        self._message = message
        self._uid = 0
        self._game_name = ''
        self._game_options = []
        self._trump_card = None
        self._out = None
        self._table = None
        self._cards_in_deck = 0
        self._games_list = []
        self._other_players_info = []
        self._me = None
        self._error = None
    def add_server_game_info(self, game):
        '''Saves info about a single server game.
        '''
        self._games_list.append(game)
    def get_list_of_games(self):
        '''Returns list of games' info.
        '''
        return self._games_list
    def set_status(self, status = True):
        '''Sets response's status.
        '''
        self._status = status
    def get_status(self):
        '''Returns response's status.
        '''
        return self._status
    def set_message(self, message):
        '''Sets response's message.
        '''
        self._message = message
    def get_message(self):
        '''Returns response's message.
        '''
        return self._message
    def set_uid(self, uid):
        '''Sets response's uid.
        '''
        self._uid = uid
    def get_uid(self):
        '''Returns response's uid.
        '''
        return self._uid
    def set_game_name(self, name):
        '''Sets game's name.
        '''
        self._game_name = name
    def get_game_name(self):
        '''Returns game's name.
        '''
        return self._game_name
    def set_game_options(self, attack6, first_attack5, retransfer):
        '''Sets game's options.
        '''
        self._game_options = [attack6, first_attack5, retransfer]
    def set_options_list(self, options):
        '''Sets game's options given as a list.
        '''
        self._game_options = options
    def get_game_options(self):
        '''Returns game's options.
        '''
        return self._game_options
    def retransfer_allowed(self):
        '''Retuns True if retransfer is allowed.
        Returns False otherwise.
        '''
        return self._game_options[2]
    def first_attack5_restrict(self):
        '''Retuns True if first attack 5 cards restriction is on.
        Returns False otherwise.
        '''
        return self._game_options[1]
    def attack6_restrict(self):
        '''Retuns True if attack 6 cards restriction is on.
        Returns False otherwise.
        '''
        return self._game_options[0]
    def set_trump_card(self, card):
        '''Sets the current trump card.
        '''
        self._trump_card = card
    def get_trump_card(self):
        '''Returns the trump card.
        '''
        return self._trump_card
    def set_out(self, cards):
        '''Sets out cards.
        '''
        self._out = cards
    def get_out(self):
        '''Returns out cards.
        '''
        return self._out
    def set_table(self, table):
        '''Sets cards from table.
        '''
        self._table = table
    def get_table(self):
        '''Returns cards in table.
        '''
        return self._table
    def set_cards_in_deck(self, number):
        '''Sets cards in deck.
        '''
        self._cards_in_deck = number
    def get_cards_in_deck(self):
        '''Returns cards in deck.
        '''
        return self._cards_in_deck
    def add_other_player_info(self, player):
        '''Adds another player's info to the response.
        '''
        self._other_players_info.append(player)
    def add_other_players_info(self, players):
        '''Adds other players' info to the response.
        '''
        self._other_players_info.extend(players)
    def get_other_players_info(self):
        '''Returns other players' info.
        '''
        return self._other_players_info
    def get_all_players_info(self):
        '''Returns another player's info.
        '''
        concat = []
        concat.extend(self._other_players_info)
        concat.append(self._me)
        return concat
    def get_my_info(self):
        '''Returns player info of the recipient of this response.
        '''
        return self._me
    def set_my_info(self, player):
        '''Sets player info of the recipient of this response.
        '''
        self._me = player
    def save_error(self, error):
        '''Saves error info.
        '''
        self._error = error
    def get_error(self):
        '''Returns error info.
        '''
        return self._error
    def is_valid(self):
        '''Returns True if no errors occured during parsing.
        Otherwise returns False.
        '''
        return self.get_error() == None
    def attacker_is_active(self):
        '''Returns True if current attacker is
        an active player. False otherwise.
        '''
        for player in self.get_all_players_info():
            if player.get_status() == "_attacker_":
                return player.is_active()
    def game_continues(self):
        counter = 0
        for player in self.get_all_players_info():
            if player.is_playing():
                counter = counter + 1
        return counter > 1
    def defender_is_active(self):
        '''Returns True if current defender is
        an active player. False otherwise.
        '''
        for player in self.get_all_players_info():
            if player.get_status() == "_defender_":
                return player.is_active()
    def get_defender(self):
        for player in self.get_all_players_info():
            if player.get_status() == "_defender_":
                return player
    def get_attacker(self):
        for player in self.get_all_players_info():
            if player.get_status() == "_attacker_":
                return player
    def __str__(self):
        '''Returns string representation of the response.
        '''
        return '\n'.join([
                         'status:' + str(self._status),
                         'message:' + str(self._message),
                         'uid:' + str(self._uid),
                         'game_name:' + str(self._game_name),
                         'game_options:' + str(self._game_options),
                         'trump_card:' + str(self._trump_card),
                         'out:' + str(self._out),
                         'table:' + str(self._table),
                         'cards_in_deck:' + str(self._cards_in_deck),
                         'games_list:' + str(self._games_list),
                         'other_players_info:' + str(self._other_players_info),
                         'me:' + str(self._me),
                         'error:' + str(self._error)
                         ])
    def __repr__(self):
        '''String representation.
        '''
        return self.__str__()


class Player_Info:
    '''Contains single player's information.
    '''
    def __init__(self, order, name, status, is_active):
        self._order = order
        self._name = name
        self._status = status
        self._number_of_cards = 0
        self._cards = cards.Cards()
        self._is_active = is_active
        self._is_me = False
    def set_number_of_cards(self, number):
        '''Sets player's number of cards.
        '''
        self._number_of_cards = number
    def set_cards(self, cards):
        '''Set player's cards.
        '''
        self._cards = cards
    def get_order(self):
        '''Returns player's order.
        '''
        return self._order
    def get_name(self):
        '''Return player's name.
        '''
        return self._name
    def is_active(self):
        '''Return True if player is active.
        Return False otherwise.
        '''
        return self._is_active
    def set_is_me(self):
        '''Sets the flag meaning that this object represents
        the recipient.
        '''
        self._is_me = True
    def is_me(self):
        '''Returns if this object represents the recipient
        of the response.
        '''
        return self._is_me
    def is_attacker(self):
        '''Checks if player is attacker.
        '''
        return self.get_status() == "_attacker_"
    def is_defender(self):
        '''Checks if player is defender.
        '''
        return self.get_status() == "_defender_"
    def is_playing(self):
        '''Checks if player is not winner or looser.
        '''
        return not self.get_status() in ["_winner_", "_fool_"]
    def make_active(self):
        '''Sets the player active.
        '''
        self._is_active = True
    def get_status(self):
        '''Returns the player's status.
        '''
        return self._status
    def get_number_of_cards(self):
        '''Returns player's number of cards.
        '''
        return self._number_of_cards
    def get_cards(self):
        '''Returns player's cards.
        '''
        return self._cards
    def __str__(self):
        '''String representation.
        '''
        return '\n'.join([
                         '\nPlayer_info',
                         'name:' + str(self._name),
                         'order:' + str(self._order),
                         'status:' + str(self._status),
                         'active:' + str(self._is_active),
                         'number of cards:' + str(self._number_of_cards),
                         'cards:' + str(self._cards)
                         ])
    def __repr__(self):
        '''String representation.
        '''
        return self.__str__()

class Game_Info:
    '''Stores information about a single game.
    '''
    def __init__(self, name, players, required_n, options):
        self._name = name
        self._players = players
        self._required_n = required_n
        self._options = options
    def get_name(self):
        '''Returns game's name.
        '''
        return self._name
    def get_list_of_players(self):
        '''Returns list of players in the game.
        '''
        return self._players
    def get_required_number(self):
        '''Returns number of players required to start the game.
        '''
        return self._required_n
    def get_options(self):
        '''Returns game's options.
        '''
        return self._options
    def retransfer_allowed(self):
        '''Returns True if retransfer is allowed.
        Returns False otherwise.
        '''
        return self._options[2]
    def first_attack5_restrict(self):
        '''Returns True if first attack 5 cards option is on.
        Returns False otherwise.
        '''
        return self._options[1]
    def attack6_restrict(self):
        '''Returns True if attack 6 cards option is on.
        Returns False otherwise.
        '''
        return self._options[0]
    def __str__(self):
        '''Returns string representation of the object.
        '''
        return '\n'.join([
                         '\nGame_info',
                         'name:' + str(self._name),
                         'players:' + str(self._players),
                         'required numbers:' + str(self._required_n),
                         'options:' + str(self._options)
                         ])
    def __repr__(self):
        '''String representation.
        '''
        return self.__str__()