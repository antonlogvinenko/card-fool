class Client_Command:
    '''Represents the client's command.
    '''
    def __init__(self):
        self._set_defaults()
    def _set_defaults(self):
        '''Initializes members with None value.
        Initializes the map (names_of_fields_in_command, name_of_class_member)
        '''
        self._FIELDS_TO_MEMBERS = {'command':'_command', 'uid':'_uid',
                                   'numberOfPlayers':'_number_of_players',
                                   'name':'_name', 'gameName':'_game_name',
                                   'cards':'_cards', 'attack6Cards':'_attack_6cards',
                                   'firstAttack5Cards':'_first_attack_5cards',
                                   'retransfer':'_retransfer','test':'_test'}
        self._members = ('_command', '_uid', '_number_of_players', '_name',
                         '_game_name', '_cards', '_first_attack_5cards',
                         '_attack_6cards', '_retransfer', '_error', '_test')
        for member in self._members:
            self.__dict__[member] = None
        #_covering_cards:   [[covered,covering], [covered,covering],...]
        #_retatt_cards:   [[card,user],[card,user],...]
    def map_field(self, field):
        return self._FIELDS_TO_MEMBERS[field]
    def _save_error(self, e):
        '''Saves the InvalidCommandException class' instance for server's needs.
        '''
        self._error = e
    def is_valid(self):
        '''The command is valid if no exception was saved during parsing.
        '''
        return self._error == None
    def get_type(self):
        '''Get the type of the command.
        '''
        return self._command
    def get_uid(self):
        '''Get the UID used in the command.
        '''
        return self._uid
    def get_name(self):
        '''Get the name used in the command.
        '''
        return self._name
    def get_game_name(self):
        '''Get the name of the game used in the command.
        '''
        return self._game_name
    def get_number_of_players(self):
        '''Get the number of players from the command.
        '''
        return self._number_of_players
    def get_cards(self):
        '''Get the list of cards used in the command.
        '''
        return self._cards
    def get_first5(self):
        '''If first attack may include 5 cards
        '''
        return self._first_attack_5cards
    def get_attack6(self):
        '''If an attack may include 6 cards
        '''
        return self._attack_6cards
    def get_retransfer(self):
        '''If retransfer is allowed
        '''
        return self._retransfer
    def whose_card(self, card):
        '''Returns the owner of the card. None if owner is unknown
        or no such card.
        '''
        owner = ''
        if self.get_type() == 'cover':
            for pair in self.get_cards():
                if pair[0] == card:
                    owner = pair[0].get_owner()
                    break
                if pair[1] == card:
                    owner = pair[1].get_owner()
                    break
        else:
            for x in self.get_cards():
                if x == card:
                    owner = x.get_owner()
                    break
        if owner == None:
            return ''
        return owner
    def how_covered(self, card):
        '''What card coveres (is over) this 'card'?
        Returns None if it is not covered.
        '''
        for pair in self._cards:
            if pair[0] == card: return pair[1]
        return None
    def what_covers(self, card):
        '''What card is covered by the 'card'?
        Returns None if no cards are.
        '''
        for pair in self._cards:
            if pair[1] == card: return pair[0]
        return None
    def __str__(self):
        '''Converts the command to a string.
        '''
        out = 'The client command object='
        for member in self._members:
            if self.__dict__[member] != None:
                out += '\n' + member + ' = \n' + str(self.__dict__[member])
        return out
    def __repr__(self):
        '''Returns full string reprsentation of the command
        '''
        return self.__str__()
    def to_string(self):
        '''Only returns the result of private __str__()
        '''
        return self.__str__()