'''Contains definitions of Server_Parser and InvalidCommandException classes.
'''
import re
import cgi
import cards
import client_command
import table


CLIENT_COMMANDS = ('register', 'createGame', 'joinGame', 'getListOfGames', 'getGameStatus',
                   'attack', 'cover', 'take', 'retransfer', 'quit', 'skip', 'restart')
SUITS = ('h', 'd', 's', 'c')
VALUES = ('6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A')
FIELDS_DELIMITER = '&'
INNER_DELIMITER = '='
ERROR_CODES = {
               0:'Unknown field name',
               1:'Unknown command',
               2:'Identificator is missed',
               3:'Illegal identificator',
               4:'Non boolean value',
               5:'Not a number',
               6:'Wrong covering set syntax',
               7:'Wrong attack or retransfer set syntax',
               8:'Command can not be splitted on pairs',
               9:'Not all required for the command fields are filled',
               10:"More than one inner delimiter " + INNER_DELIMITER,
               11:'Illegal command syntax: command field goes first',
               12:'Command must be set once'
               }


class Server_Parser:
    '''Parses an incoming string command. Contains a Command object.
    While parsing checks the data. Fills Command object's fields then returns it
    to the server. If an error occurs, stops parsing, saves the error info
    in the object, returns it to the server.
    '''
    def __init__(self):
        self._init_tester()
    def parse_cgi_input(self):
        '''Takes arguments from command line. Must be used in a cgi script.
        See similar function parse_command().
        '''
        self.com = client_command.Client_Command()
        self.storage = cgi.FieldStorage()
        try:
            for key in self.storage.keys():
                self._check_and_assign([key, self.storage.getvalue(key)])
            self._check_empty_fields()
        except InvalidCommandException, e:
            self.com._save_error(e)
        return self.com
    def parse_command(self, input_string):
        self.com = client_command.Client_Command()
        '''Parses an incoming command 'input_string'. Used for testing.
        See similar function parse_cgi_command().
        '''
        try:
            for field in input_string.split(FIELDS_DELIMITER):
                self._check_and_assign(self._split_string(field, INNER_DELIMITER))
            self._check_empty_fields()
        except InvalidCommandException, e:
            self.com._save_error(e)
        return self.com
    def _init_tester(self):
        '''Initializes values of a hash used for testing different fields.
        Has a structure: (key, value) == (field_name, name_of _testing_function)
        '''
        self._FIELDS_TESTERS = {'command':'_testif_is_command', 'name':'_testif_is_legal_ident',
                               'gameName':'_testif_is_legal_ident', 'retransfer':'_testif_is_bool',
                               'firstAttack5Cards':'_testif_is_bool', 'test':'_testif_is_test_on',
                               'uid':'_testif_is_legal_ident', 'numberOfPlayers':'_testif_is_number',
                               'attack6Cards':'_testif_is_bool', 'cards':'_testif_proper_set'}
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
    def _check_empty_fields(self):
        '''Cheks if all required fields were filled.
        '''
        unfilled = []
        for x in self._REQUIRED_FIELDS[self.get_com_type()]:
            if self.com.__dict__[self.com.map_field(x)] == None:
                unfilled.append(x)
        if unfilled != []:
            raise InvalidCommandException(9, unfilled)
    def _check_and_assign(self, pair):
        '''Checks if the field with pair[0] name exists.
        If it is, checks the value using self._tester()
        '''
        self._testif_is_pair(pair)
        (field, value) = pair
        self._testif_field_exists(field)
        self._testif_command_redef(field)
        if not self._field_is_required(field): return
        self._tester(field, value, self._FIELDS_TESTERS[field])
    def _field_is_required(self, field):
        return field == 'command' or field in self._REQUIRED_FIELDS[self.get_com_type()]
    def _tester(self, f, v, tester):
        '''Calls the specified test function for the value v.
        If that function does not raise an exception, it returns
        the value to assign to the f field.
        '''
        r = self.__class__.__dict__[tester].__call__(self, v)
        self.com.__dict__[self.com.map_field(f)] = r
    def _testif_command_redef(self, field):
        '''Checks if 'command' field is defined twice.
        Raises an exception if so.
        '''
        if field == 'command' and self.com.get_type():
            raise InvalidCommandException(12)
    def _testif_is_pair(self, pair):
        '''Checks if a list has two elements.
        '''
        if len(pair) != 2:
            raise InvalidCommandException(10, pair)
    def _testif_is_test_on(self, str):
        '''Checks if restart command sets test mode on.
        '''
        if str != 'true':
            raise InvalidCommandException(3, str)
        return True
    def _testif_field_exists(self, field):
        '''Checks if a field which value we are going to test exists.
        '''
        if field not in self._FIELDS_TESTERS.keys():
            raise InvalidCommandException(0, field)
    #"TEST IF" functions follows. They check the value of a field given by
    #the client. If it has wrong syntax an exeption is raised.
    #Otherwise the value to assign to the command's field is returned.
    #The value is based on one given by the client.
    def _testif_proper_set(self, value):
        '''Determines if the 'value' is a set of attacking/retransfered
        or covering cards and calls appropriate functions to perform
        further checks. See these appropriate functions' comments.
        '''
        cmd = self.com._command
        if cmd == 'cover':
            return self._testif_is_cover_set(value)
        elif cmd == 'attack' or cmd == 'retransfer':
            return self._testif_is_retatt_cards(value)
    def _testif_is_number(self, value):
        '''Checks if 'value' is a number.
        '''
        if not value.isdigit():
            raise InvalidCommandException(5, value)
        return int(value)
    def _testif_is_command(self, cmd):
        '''Checks if 'cmd' is an existing command.
        '''
        if cmd not in CLIENT_COMMANDS:
            raise InvalidCommandException(1, cmd)
        return cmd
    def _testif_is_retatt_cards(self, set):
        '''Checks if the string 'set' is a legal string representation
        of a set of retransfered or attacking cards.
        It must look like "[h0][c9]".
        Returns a list (Card('h0'), Card('c9'))
        '''
        split_set = self._split_cards_string(set)
        retatt_set = cards.Cards()
        for card in split_set:
            if not self._is_card(card):
                raise InvalidCommandException(7, set)
            retatt_set.add_card(cards.Card(card))
        return retatt_set
    def _testif_is_cover_set(self, set):
        '''Checks if the string 'set' is a legal string representation
        of a set of coverng cards. It must look like "[h0(Alice)<hK][c9<cQ]".
        Returns a list ( (Card('h0','Alice'),Card('hK')),  (Card('c9'),Card('cQ'))).
        '''
        split_set = self._split_cards_string(set)
        cover_set = table.Table()
        for pair in split_set:
            spl = pair.split('<')
            if (len(spl) !=2 or
            not self._is_card(spl[0]) or not self._is_card(spl[1]) ):
                raise InvalidCommandException(6, set)
            cover_set.append([cards.Card(spl[0]), cards.Card(spl[1])])
        return cover_set
    def _testif_is_bool(self, var):
        '''Checks if var is 'true' or 'false'
        '''
        if var !='true' and var != 'false':
            raise InvalidCommandException(4, var)
        return self._str_to_bool(var)
    def _testif_is_legal_ident(self, name):
        '''Checks if 'smth' is one or another.
        (name) is user name and "name" is a game name.
        '''
        if name == '':
            raise InvalidCommandException(2, name)
        if not self._is_valid_ident(name):
            raise InvalidCommandException(3, name)
        return name
    def get_com_type(self):
        '''Returns a command type if it exists.
        Raises an exception otherwise.
        '''
        if self.com.get_type() == None:
            raise InvalidCommandException(11)
        return self.com.get_type()
    def _split_string(self, str, delimiter):
        '''Split the str by delimiter and check if splitted
        '''
        splitted = str.split(delimiter)
        if len(splitted) == 1:
            raise InvalidCommandException(8, str)
        return splitted
    def _split_cards_string(self, str):
        '''Makes a list ['h0', 'd5', 'cK'] from string '[h0][d5][cK]'
        '''
        return str[1:-1].split('][')
    def _str_to_bool(self, str):
        '''Maps 'true' to True, False otherwise
        '''
        if str == 'true':
            return True
        return False
    def _is_valid_ident(self, name):
        '''Checks if 'name' cosists only of digits, letters and underscores
        '''
        exp = re.compile(r'[_\d\w]*')
        if exp.search(name).end() == len(name):
            return True
        return False
    def _is_card(self, str):
        '''Checks if 'str' represents a card
        '''
        if len(str)<2 or str[0] not in SUITS or str[1] not in VALUES:
            return False
        return True


class InvalidCommandException:
    '''Is raised if the syntax of the client's request is wrong.
    Contains full error description.
    '''
    def __init__(self, code = 0, info = 'No info'):
        '''Creates an exception object.
        '''
        self._err_info = info
        self._errdescr = ERROR_CODES[code]
    def __str__(self):
        '''Conversion to string.
        '''
        return "Error type= " + self._errdescr + "\nDetails= " + str(self._err_info)
    def __repr__(self):
        '''String representation.
        '''
        return self.__str__()