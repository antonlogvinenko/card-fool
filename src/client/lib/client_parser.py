'''Contains definitions of Client_Parser ans InvalidResponseException classes.
'''

import server_response
import re
import table
import cards

ERROR_CODES = {
               0:'Unknown error',
               1:'Missed field',
               2:'Illegal field value',
               }

class Client_Parser:
    def __init__(self):
        '''Initialization of constant values used for parsing response.
        '''
        self.INNER_DELIMITER = ':'
        self.OUTER_DELIMITER = '\n'
        self.GAME = 'game'; self.STATUS = 'status';    self.MESSAGE = 'message'
        self.UID = 'uid'; self.TABLE = 'table'; self.PLAYER = 'player'; self.TRUMP = 'trump'
        self.OPTIONS = 'options'; self.ACTIVE = 'active'; self.OUT = 'out'; self.DECK = 'deck'
        self.NUMBER_OF_PLAYERS = 'numberOfPlayers'; self.FIRST_ATTACK5 = 'firstAttack5Cards'
        self.ATTACK6 = 'attack6Cards'; self.CAN_RETRANSER = 'canRetransfer'
        self._restart()
    def _restart(self):
        '''Resets some attributes used for parsing.
        '''
        self._server_response = server_response.Server_Response()
        self._splitted = ''
        self._games_fields = 0
        self._has_games_list = False
        self._has_game_data = False
    def parse_response(self, response):
        '''Takes a response from server, splits it, calls other
        methods to extract from it all possible data.
        '''
        self._restart()
        try:
            self._split_response(response)
            self._get_status_from_response()
            self._get_message_from_response()
            self._get_uid_from_response()
            if self._response_has_games_list():
                self._get_games_list_from_response()
            if self._response_has_game_data():
                self._get_game_data_from_response()
        except InvalidResponseException, e:
            self._server_response.save_error(e)
        return self._server_response
    def _cut_field(self, name):
        '''Finds a field 'name' in splitted response, cuts 
        and returns it. Returns None if field 'name' is not found.
        '''
        for x in self._splitted:
            if x[0] == name:
                self._splitted.remove(x)
                return x[1]
        return None
    def _cut_and_check_field(self, name):
        '''Finds a field 'name' in splitted response, cuts 
        and returns it. Raises an exception if field 'name' is not found.
        '''
        value = self._cut_field(name)
        if value == None:
            raise InvalidResponseException(1, name)
        return value
    def _response_has_games_list(self):
        '''Returns True if the response contains list of games.
        Returns False otherwise.
        '''
        return self._has_games_list
    def _response_has_game_data(self):
        '''Returns True if the response contains game status.
        Returns False otherwise.
        '''
        return self._has_game_data
    def _split_response(self, response):
        '''Splits response. Provides a short analysis of its
        contents.
        '''
        self._splitted = [str.split(self.INNER_DELIMITER)
                          for str in response.split(self.OUTER_DELIMITER)]
        games_fields = 0
        has_games_list = False
        for x in self._splitted:
            if x[0] == self.GAME:
                games_fields = games_fields + 1
                if x[1].count("\"") != 0:
                    has_games_list = True
        if games_fields != 0:
            if has_games_list:
                self._has_games_list = True
            else:
                self._has_game_data = True
    def _get_status_from_response(self):
        '''Gets the valuse of 'status' field from the response.
        Set an according field in response's object.
        '''
        status = self._cut_field(self.STATUS)
        if status != None:
            self._server_response.set_status(self._to_bool(status))
    def _get_message_from_response(self):
        '''Gets the values of 'message' field from server's
        response, adds it to the response object.
        '''
        message = self._cut_field(self.MESSAGE)
        if message != None:
            self._server_response.set_message(message)
    def _get_uid_from_response(self):
        '''Gets the values of 'uid' field from server's
        response, adds it to the response object.
        '''
        uid = self._cut_field(self.UID)
        if uid != None:
            self._server_response.set_uid(uid)
    def _get_games_list_from_response(self):
        '''Gets description of games in the server's response.
        '''
        next_game = self._cut_field(self.GAME)
        while next_game != None:
            self._get_game_description(next_game)
            next_game = self._cut_field(self.GAME)
    def _get_game_description(self, str):
        '''Gets description of a single game in the response,
        adds this info to the response object.
        '''
        name = re.compile(r"\".*\"").findall(str)[0].replace("\"", '')
        players = [player[1:-1] for player in re.compile(r"\(.*?\)").findall(str)]
        other_data = [option[1:-1] for option in re.compile(r"{.*?}").findall(str)]
        required_n = self._to_number(other_data[0].replace(self.NUMBER_OF_PLAYERS, ''))
        options = [self.ATTACK6 in other_data,
                   self.FIRST_ATTACK5 in other_data,
                   self.CAN_RETRANSER in other_data]
        self._server_response.add_server_game_info(
                                   server_response.Game_Info(name, players, required_n, options))


    def _get_game_data_from_response(self):
        '''Get info about the playing game.
        '''
        self._server_response.set_game_name(self._get_game_name())
        self._server_response.set_out(self._get_out())
        self._server_response.set_cards_in_deck(self._get_deck())
        self._server_response.set_table(self._get_table())
        self._server_response.set_trump_card(self._get_trump())
        active = self._get_active()
        [players, me] = self._get_players_description(active)
        self._server_response.add_other_players_info(players)
        self._server_response.set_my_info(me)
        self._server_response.set_options_list(self._get_options())
    def _get_deck(self):
        '''Returns the number of cards in deck.
        '''
        deck = self._cut_and_check_field(self.DECK)
        deck = deck[1:-1]
        return self._to_number(deck)
    def _get_game_name(self):
        '''Returns game name.
        '''
        return self._cut_and_check_field(self.GAME)
    def _get_active(self):
        '''Returns the number of active player.
        '''
        return self._to_number(self._cut_and_check_field(self.ACTIVE))
    def _get_options(self):
        '''Returns a list [attack6, attack5, retrnasfer]
        with boolean values representing game options.
        '''
        opts = [x[1:-1]
                for x in re.compile(r"{.*?}").findall(self._cut_and_check_field(self.OPTIONS))]
        options = [self.ATTACK6 in opts, self.FIRST_ATTACK5 in opts, self.CAN_RETRANSER in opts]
        return options
    def _get_out(self):
        '''Retutns cards that were sent to out.
        '''
        out_cards = self._cut_and_check_field(self.OUT)
        out = cards.Cards()
        if out_cards != '[]':
            for card in re.compile(r"\[.*?\]").findall(out_cards):
                card = card[1:-1]
                out.add_card(cards.Card(card))
        return out
    def _get_trump(self):
        '''Returns the trump card.
        '''
        trump = self._cut_and_check_field(self.TRUMP)
        return cards.Card(trump[1:-1])
    def _get_table(self):
        '''Returns cards on the table.
        '''
        t = table.Table()
        for card in re.compile(r"\[.*?\]").findall(self._cut_and_check_field(self.TABLE)):
            card = card[1:-1]
            set = card.split('<')
            t.put_on_card(cards.Card(set[0]))
            if len(set) == 2:
                t.cover_card(cards.Card(set[0]), cards.Card(set[1]))
        return t
    def _get_players_description(self, active):
        '''Get the description of players in the response.
        '''
        players = []
        me = None
        next_player = self._cut_field(self.PLAYER)
        while next_player:
            player = self._get_player_info(active, next_player)
            if player.is_me():
                me = player
            else:
                players.append(player)
            next_player = self._cut_field(self.PLAYER)
        return [players, me]
    def _get_player_info(self, active, str):
        '''Gets info about a single player and adds
        this info to the response object.
        '''
        order = re.compile(r'.*\(').findall(str)
        order = self._to_number(order[0][:-1])
        name = re.compile(r'\(.*?\)').findall(str)
        name = name[0][1:-1]
        status = re.compile(r'\).*?\[').findall(str)
        if len(status) != 0:
            status = status[0][1:-1]
        else:
            status = re.compile(r'\).*').findall(str)
            status = status[0][1:]
        other = re.compile(r'\[.*?\]').findall(str)
        player_info = server_response.Player_Info(order, name, status, active == order)
        if len(other) == 0:
            player_info.set_is_me()
        elif other[0][1:-1].isdigit():
            number_of_cards = other[0][1:-1]
            player_info.set_number_of_cards(number_of_cards)
        else:
            players_cards = cards.Cards()
            for card in other:
                players_cards.add_card(cards.Card(card[1:-1]))
            player_info.set_cards(players_cards)
            player_info.set_is_me()
        return player_info
    def _to_bool(self, b):
        '''Converts string message to a boolean value.
        Raises an exception if string is incorrect.
        '''
        if b == 'ok':
            return True
        if b == 'fail':
            return False
        raise InvalidResponseException(2, b)
    def _to_number(self, n):
        '''Converts string message to an int value.
        Raises an exception if string is incorrect.
        '''
        if not n.isdigit():
            raise InvalidResponseException(2, n)
        return int(n)


class InvalidResponseException:
    def __init__(self, code = 0, info = 'No info'):
        '''Creates an exception.
        '''
        self._err_info = info
        self._errdescr = ERROR_CODES[code]
    def __str__(self):
        '''Conversion to a string.
        '''
        return "Error type= " + self._errdescr + " Details= " + str(self._err_info)
    def __repr__(self):
        '''String representation.
        '''
        return self.__str__()