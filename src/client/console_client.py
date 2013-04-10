'''Includes definition of Console_Client class allowing to play, test game and
create .log files for testing game logic.
'''

import msvcrt
import os
import client_generator
import client_parser
import requestor
import time
import sys
import logger
import cards
import re
import table
import ai

class Console_Client:
    def __init__(self, use_ai = False):
        self._generator = client_generator.Client_Generator()
        self._parser = client_parser.Client_Parser()
        self._requestor = requestor.Requestor()
        self._uid = 0
        self._name = ''
        self._game_name = ''
        self.UPDATE_DELAY = 0
        self._logger = logger.Logger()
        self._response_old = ''
        self._response_new = ''
        self._options = []
        self._ai = ai.Ai(self._requestor, self._uid)
        self._use_ai = use_ai
    def _make_and_parse(self, request):
        '''Makes request, gets a response. Parses and returns
        the result.'''
        self._make(request)
        return self._parse()
    def _make(self, request):
        '''Logs a request, sends it.
        Logs received response.
        '''
        #log = False
        #if request.find('getGameStatus') == -1 and request.find('getListOfGames') == -1:
        #    log = True
        self._response_new = self._requestor.make_request(request)
        self._logger.sent(request)
        self._logger.received(self._response_new)
    def new_response(self):
        '''Checks if the response received by _make()
        differs form the previous one.
        '''
        return self._response_old != self._response_new
    def _parse(self):
        '''Saves received response as an old one,
        parses it and returns the result.
        '''
        self._response_old = self._response_new
        return self._parser.parse_response(self._response_new)
    def _read_choice(self):
        '''Returns what user has entered.
        '''
        c = raw_input('$')
        if c == 'bye':
            sys.exit()
        return c
    def _read_int_choice(self, a=1, b=0):
        '''Reads user input and coverts it to int.
        '''
        d = self._read_choice()
        while re.compile(r'\d*').findall(d)[0] != d and (d<a or d>b):
            d = self._read_choice()
        return int(d)
    def _convert_to_cards(self, str):
        '''If str can be converted to cards.Cards returns
        its conversion. Otherwise returns None.
        '''
        read_cards = cards.Cards()
        for card in str.split(" "):
            if cards.is_card(card):
                read_cards.add_card(cards.Card(card))
            else:
                return None
        return read_cards
    def _read_cards_choice(self):
        '''Reads user input and converts it to class cards.Cards.
        '''
        self._print_info("Enter set of cards: cA c6 sK ...")
        converted = None
        while converted == None:
            read = self._read_choice()
            converted = self._convert_to_cards(read)
            if converted != None:
                return converted
    def _convert_to_cover_set(self, str):
        '''If str can be converted to table.Table returns
        its conversion. Otherwise returns None.
        '''
        user_table = table.Table()
        for pair in str.split(" "):
            set = pair.split('<')
            if not isinstance(set, list):
                return None
            if len(set) < 2:
                return None
            if cards.is_card(set[0]) and cards.is_card(set[1]):
                bottom = cards.Card(set[0])
                top = cards.Card(set[1])
                user_table.put_on_card(bottom)
                user_table.cover_card(bottom, top)
            else:
                return None
        return user_table
    def _read_cover_cards_choice(self):
        '''Reads user input and converts it to class table.Table.
        '''
        self._print_info("Enter set of covered cards: c6<cA s9<s0 ...")
        convert = None
        while convert == None:
            read = self._read_choice()
            converted = self._convert_to_cover_set(read)
            if converted != None:
                return converted
    def _print_wait(self):
        '''Pints a "Wait ..." string.
        '''
        print 'Please wait...'
    def _print_success(self, name, succeeded, message):
        '''Prints the successfulness of 'name' operation and
        server's message.
        '''
        if succeeded:
            print name + " succeeded"
        else:
            print name + " failed. Server reason: " + message
    def _read_bool_choice(self):
        '''Reads user input and converts it to a boolean value.
        '''
        d = self._read_choice()
        if d == 'y':
            return True
        return False
    def _welcome_text(self):
        '''Prints welcome text.
        '''
        print "Card game Durak. Join us!"
        print "Type 'bye' to quit the game.\n"
    def _select_game_source(self):
        '''Asks user about the way he wants to
        enter the game.
        '''
        while True:
            self._prepare_screen()
            self._print_info('Join to a game or create it?')
            self._print_hash({1:'See list of existing games', 2:'Create game'})
            choice = self._read_int_choice(1, 2)
            if choice == 1:
                self._select_existing_game()
            else:
                self._create_game()
    def _select_existing_game(self):
        '''Makes user to choose an existing game.
        '''
        response = self._do_select()
        while not (response == None or response.get_status()):
            response = self._do_select(response.get_message())
        if response != None:
            self._main_menu()
    def _do_select(self, msg=''):
        '''Shows a menu with a list representing all existing games.
        '''
        self._prepare_screen()
        if msg != '':
            self._print_info('Joining game failed. Server reason: ' + msg)
        response = self._make_and_parse(self._generator.get_games_list())
        description_list = {}
        i = 1
        for game in response.get_list_of_games():
            opts = game.get_options()
            options = ''
            if opts[0]: options = "attack 6 cards restriction"
            if opts[1]: options += "first attack 5 cards restriction"
            if opts[2]: options += "retransfer" 
            description_list[i] = "; ".join([
                                             "Game name: " + game.get_name(),
                                             "Players: " + ", ".join(game.get_list_of_players()),
                                             "Required: " + str(game.get_required_number()),
                                             "Options: " + options
                                             ])
            i = i + 1
        self._print_item(0, "Back")
        self._print_hash(description_list)
        choice = self._read_int_choice()
        while not (choice in description_list.keys() or choice == 0):
            choice = self._read_int_choice()
        if choice == 0:
            return None
        game_name = response.get_list_of_games()[choice - 1].get_name()
        self._game_name = game_name
        self._print_wait()
        return self._make_and_parse(
                            self._generator.join_game(self._uid, self._game_name))
    def _register_menu(self):
        '''Makes a user to register himself.
        '''
        response = self._do_register()
        while not response.get_status():
            response = self._do_register(response.get_message())
        self._uid = response.get_uid()
        self._ai.set_uid(self._uid)
        while True:
            self._select_game_source()
    def _do_register(self, msg=''):
        '''Shows a menu for registering.
        '''
        self._prepare_screen()
        if msg != '':
            self._print_info('Registration failed. Server reason: ' + msg)
            self._print_info('Please try again')
        self._print_info('Please enter host name')
        host = self._read_choice()
        if host == '': host = 'localhost'
        self._print_info('Please enter script name')
        script = self._read_choice()
        if script == '': script = '/cgi-bin/commands.py'
        self._print_info('Please enter your name')
        self._name = self._read_choice()
        self._print_wait()
        self._requestor.set_host(host)
        self._requestor.set_script(script)
        self._ai.set_requestor(self._requestor)
        return self._make_and_parse(self._generator.register(self._name))
    def _create_game(self):
        '''Makes a user to create a game.
        '''
        response = self._do_create()
        while not response.get_status():
            response = self._do_create(response.get_message())
        self._main_menu()
    def _do_create(self, msg=''):
        '''Shows a menu for creating game.
        '''
        self._prepare_screen()
        if msg != '':
            self._print_info('Creating game failed. Server reason: ' + msg)
        self._print_info('Please enter game name:')
        game_name = self._read_choice()
        self._print_info('Please enter number of players:')
        players = self._read_int_choice()
        while (players < 2) or (players > 6):
            self._print_info('Please enter number of players: (2..)')
            players = self._read_int_choice()
        self._print_info('Do you allow to retransfer cards? (y/n)')
        retransfer = self._read_bool_choice()
        self._print_info('Do you allow six cards attack? (y/n)')
        attack6 = self._read_bool_choice()
        self._print_info('Do you allow first five cards attack? (y/n)')
        first_attack5 = self._read_bool_choice()
        self._print_wait()
        return self._make_and_parse(self._generator.create_game(self._uid, game_name, players,
                                                            retransfer, first_attack5, attack6))
    def _main_menu(self):
        '''Controls the screen content during the game.
        '''
        self._prepare_screen()
        while True:
            self._make(self._generator.get_game_status(self._uid))
            if self.new_response():
                response = self._parse()
                if not response.get_status():
                    self._print_info(response.get_message())
                else:
                    self._prepare_screen()
                    self._print_info('Game status Ok')
                    if self._draw_control(response):
                        return
            time.sleep(self.UPDATE_DELAY)
    def ai_enabled(self):
        return self._use_ai
    def _draw_control(self, response):
        '''Shows a player's 'control' menu.
        Returns True if user finishes playing.
        '''
        #print response
        if response.get_message() != '':
            self._print_info('Message: ' + response.get_message())
        self._options = response.get_game_options()
        options = ''
        if self._options[0]: options += "attack 6 cards "
        if self._options[1]: options += "attack 5 cards "
        if self._options[2]: options += "retransfer"


    
        print 'Game options: ', options
        print 'Deck:', response.get_cards_in_deck()
        print 'Table:', response.get_table()
        print 'Out:', response.get_out()
        print 'Trump:', response.get_trump_card()
        players_info = ''
        for player in response.get_other_players_info():
            players_info += ", ".join(['Player ' + player.get_name(),
                                        'Order ' + str(player.get_order()),
                                        'Status ' + player.get_status(),
                                        'Is active:' + str(player.is_active())]) + "\n"
        my_info = response.get_my_info()
        self._print_other_players_info(response.get_other_players_info())
        self._print_my_info(my_info)


        if my_info.get_status() == '_winner_':
            self._print_info("You win!")
        if my_info.get_status() == '_fool_':
            self._print_info("You loose. Haha.")


        if (my_info.get_status() not in ['_winner_', '_fool_']):
            #extracts data
            self._ai.think(response)
            #self._ai._probs.output("current_game" + self._uid)

            if my_info.is_active():
                if self.ai_enabled():
                    self._print_info("Ai is trying to do something")
                    self._ai.generate_strategy()
                    self._print_info("Succeeded")
                else:
                    self._print_info("Your available actions:")
                    self._print_item(0, "Quit")
                    if my_info.get_status() == '_attacker_':
                        self._print_hash({1:'Attack card[, card[, card[, ...]]]', 2:'Skip'})
                        choice = self._read_int_choice(0, 2)
                        if choice == 0:
                            response = self._make_and_parse(self._generator.quit(self._uid))
                            self._print_success("Quit", response.get_status(), response.get_message())
                            time.sleep(self.UPDATE_DELAY)
                            if response.get_status():
                                return True
                        elif choice == 1:
                            attack_cards = self._read_cards_choice()
                            response = self._make_and_parse(self._generator.attack(self._uid, attack_cards))
                            self._print_success("Attack", response.get_status(), response.get_message())
                        elif choice == 2:
                            response = self._make_and_parse(self._generator.skip(self._uid))
                            self._print_success("Skip", response.get_status(), response.get_message())
                    if my_info.get_status() == '_defender_':
                        actions = {1:'Cover card<card[, card<card[, ...]]', 2:'Take cards'}
                        if self._options[2]:
                            actions[3] = 'Retransfer'
                        self._print_hash(actions)
                        if self._options[2]:
                            choice = self._read_int_choice(0, 2)
                        else:
                            choice = self._read_int_choice(0, 3)
                        if choice == 0:
                            response = self._make_and_parse(self._generator.quit(self._uid))
                            self._print_success("Quit", response.get_status(), response.get_message())
                            time.sleep(self.UPDATE_DELAY)
                            if response.get_status():
                                return True
                        elif choice == 1:
                            covered = self._read_cover_cards_choice()
                            response = self._make_and_parse(self._generator.cover(self._uid, covered))
                            self._print_success("Cover", response.get_status(), response.get_message())
                        elif choice == 2:
                            response = self._make_and_parse(self._generator.take(self._uid))
                            self._print_success("Take", response.get_status(), response.get_message())
                        elif choice == 3:
                            retransfer_cards = self._read_cards_choice()
                            response = self._make_and_parse(self._generator.retransfer(self._uid, retransfer_cards))
                            self._print_success("Retransfer", response.get_status(), response.get_message())
            else:
                self._print_info("Wait until YOU become an active player.")

        if my_info.get_status() in ['_winner_', '_fool_']:
            self._print_info("Press enter to leave the game.")
            self._read_choice()
            response = self._make_and_parse(self._generator.quit(self._uid))
            self._print_success("Quit", response.get_status(), response.get_message())
            time.sleep(self.UPDATE_DELAY)
            if response.get_status():
                return True
        return False
    def _print_my_info(self, me):
        '''Prints information about the player.
        '''
        print " || ".join([
                             "\nYou are " + me.get_name(),
                             "order " + str(me.get_order()),
                             "status " + str(me.get_status()),
                             "active player?" + str(me.is_active()),
                             "\nCards: " + str(me.get_cards()),
                             ])
    def _print_player_info(self, player):
        '''Prints another player's info.
        '''
        print " || ".join([
                             "\nPlayer " + player.get_name(),
                             "order " + str(player.get_order()),
                             "status " + str(player.get_status()),
                             "active player?" + str(player.is_active()),
                             "number of cards: " + str(player.get_number_of_cards()),
                             ])
    def _print_other_players_info(self, players):
        '''Prints other players' info.
        '''
        for player in players:
            self._print_player_info(player)
    def _prepare_screen(self):
        '''Prepares screen to output following info.
        '''
        os.system('cls')
        self._welcome_text()
    def _print_item(self, n, txt):
        '''Prints an item from the hash representing possible user actions.
        '''
        print '[' + str(n) + ']', txt
    def _print_hash(self, hash):
        '''Prins the hash representing possible user actions.
        '''
        for n in hash:
            self._print_item(n, hash[n])
    def _print_info(self, info=''):
        '''Prins a message to a user.
        '''
        if info == '':
            print 'Type a digit to make a choice.'
        else:
            print '\n> > >', info
    def run(self):
        '''Starts console-client application.
        '''
        self._register_menu()

#starting console client
use_ai = False
if "ai" in sys.argv:
    use_ai = True
Console_Client(use_ai).run()