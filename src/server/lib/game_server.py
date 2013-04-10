'''Contains definition of game_server class.
'''

import games
import players
import server_generator
import logger
import cards
import table

class Game_Server:
    '''Contains information about all games and registered players.
    Handles parsed client commands and return responses to them.
    '''
    def _generate_id(self, name):
        '''Generates and returns a uid.
        '''
        if self._in_compatibility_test_mode():
            return name
        elif self._in_test_mode():
            id = self._temp_id
            self._temp_id = id + 1
            return str(id)
        else:
            id = self._temp_id
            self._temp_id = id + 1
            return str(id)
    def _reset_id(self):
        '''Resets uid counter as if no uid were generated.
        '''
        self._temp_id = 0
    def __init__(self):
        '''
        '''
        self.MESSAGES = {
                         0:'',
                         1:'The user with such name is already registered',
                         2:'The game is already started',
                         3:'There is no game with such name',
                         4:'Invalid uid',
                         5:'The user can\'t be in two games at one time',
                         6:'The game with such name is already created',
                         #7:'Invalid game options',
                         8:'Game is not started yet',
                         9:'You can\'t skip your turn',
                         10:'You are not active player',
                         11:'Invalid cards combination',
                         12:'You must defend all cards'
                         }
        self._games = games.Games()
        self._players = players.Registered_Players()
        self._generator = server_generator.Server_Generator()
        self._temp_id = 0
        self._test_mode = False
        self._compatibility_test_mode = False
    def set_compatibility_test_mode(self):
        self._compatibility_test_mode = True
    def _in_compatibility_test_mode(self):
        return self._compatibility_test_mode
    def set_test_mode(self):
        '''Enables test mode of the game server.
        '''
        self._test_mode = True
    def _in_test_mode(self):
        '''Return True if the server is in test mode.
        Returns False otherwise.
        '''
        return self._test_mode
    def handle_register(self, command):
        '''Handles 'register' command, processes it, returns a response.
        '''
        name = command.get_name()
        if self._players.name_exists(name):
            return self._generator.register_response(False, self.MESSAGES[1], '')
        new_id = self._generate_id(name)
        self._players[new_id] = players.Registered_Player(name)
        return self._generator.register_response(True, self.MESSAGES[0], new_id)
    def handle_games_list_request(self):
        '''Handles 'get list of games' command, processes it, returns a response.
        '''
        return self._generator.list_of_games_response(self._games)
    def handle_join(self, command):
        '''Handles 'join' command, processes it, returns a response.
        '''
        uid = command.get_uid()
        game_name = command.get_game_name()
        if not uid in self._players.keys():
            return self._generator.join_game_response(False, self.MESSAGES[4])
        if not game_name in self._games.keys():
            return self._generator.join_game_response(False, self.MESSAGES[3])
        if self._players[uid].is_playing_now():
            return self._generator.join_game_response(False, self.MESSAGES[5])
        if not self._games[game_name].needs_players():
            return self._generator.join_game_response(False, self.MESSAGES[2])
        self._games[game_name].add_registered_player(uid, self._players[uid])
        self._players[uid].starts_playing(game_name)
        return self._generator.join_game_response(True, self.MESSAGES[0])
    def handle_create(self, command):
        '''Handles 'create' command, processes it, returns a response.
        '''
        uid = command.get_uid()
        game_name = command.get_game_name()
        number_of_players = command.get_number_of_players()
        attack6 = command.get_attack6()
        first_attack5 = command.get_first5()
        retransfer = command.get_retransfer()
        if not uid in self._players.keys():
            return self._generator.join_game_response(False, self.MESSAGES[4])
        if game_name in self._games.keys():
            return self._generator.join_game_response(False, self.MESSAGES[6])
        if self._players[uid].is_playing_now():
            return self._generator.join_game_response(False, self.MESSAGES[5])
        #game optionss invalid?
        self._games.new_game(game_name, number_of_players, attack6, first_attack5,
                             retransfer, self._in_test_mode(), self._in_compatibility_test_mode())
        self._games[game_name].add_registered_player(uid, self._players[uid])
        self._players[uid].starts_playing(game_name)
        return self._generator.create_game_response(True, self.MESSAGES[0])
    def handle_game_status_request(self, command):
        '''Handles 'get game status' command, processes it, returns a response.
        '''
        uid = command.get_uid()
        game_name = self._players[uid].get_playing_game()
        if game_name == '':
            return self._generator.join_game_response(False, self.MESSAGES[10])
        game = self._games[game_name]
        status = game.game_started()
        msg = 0
        if not game.game_started(): msg = 8
        return self._generator.get_game_status_response(
                                            status, self.MESSAGES[msg], game_name, game, uid)
    def _get_game_by_uid(self, uid):
        '''Returns game object by uid of participating player.
        '''
        return self._games[self._players[uid].get_playing_game()]
    def _get_player_by_uid(self, uid):
        '''Returns player object by player's uid.
        '''
        return self._get_game_by_uid(uid).get_players_hash()[uid]
    def _add_name_to_cards(self, uid, cards_to_change):
        '''Adds a name of player with specified uid to
        cards cards_to_change.
        '''
        name = self._get_player_by_uid(uid).get_name()
        if isinstance(cards_to_change, cards.Cards):
            for card in cards_to_change:
                card.set_owner(name)
        elif isinstance(cards_to_change, table.Table):
            for card in cards_to_change.get_covering_cards():
                card.set_owner(name)
        return cards_to_change
    def handle_skip_request(self, command):
        '''Handles 'skip' command, processes it, returns a response.
        '''
        uid = command.get_uid()
        msg = self._common_check(command)
        if msg != None:
            return self._generator.skip_response(False, msg)
        if self._get_player_by_uid(uid).is_defender():
            return self._generator.skip_response(False, self.MESSAGES[9])
        game = self._get_game_by_uid(uid)
        if game.throwing():
            if game.next_throw_on_attacker_exists():
                game.set_next_throw_on_attacker()
            else:
                if game.get_table().has_uncovered_cards():
                    game.get_players_hash().make_defender_active()
                else:
                    game.table_to_out()
                    game.reset_throw_on_status()
                    game.set_next_defender_attacker(False)
            return self._generator.skip_response(True, self.MESSAGES[0])
        return self._generator.skip_response(False, self.MESSAGES[9])    
    def handle_attack_request(self, command):
        '''Handles 'attack' command, processes it, returns a response.
        '''
        uid = command.get_uid()
        msg = self._common_check(command)
        if msg != None:
            return self._generator.attack_response(False, msg)
        game = self._get_game_by_uid(uid)
        attack_cards = self._add_name_to_cards(uid, command.get_cards())
        if not game.throwing():
            if not game.check_first_attacker_cards(attack_cards):
                return self._generator.attack_response(False, self.MESSAGES[11])
            game.get_players_hash().get_attacker().take_away_cards(attack_cards)
            game.get_table().put_on_cards(attack_cards)
            game.get_players_hash().make_defender_active()
            return self._generator.attack_response(True, self.MESSAGES[0])
        if not game._check_throw_on_cards(command):
            return self._generator.attack_response(False, self.MESSAGES[11])
        game.get_players_hash().get_attacker().take_away_cards(attack_cards)
        game.get_table().put_on_cards(attack_cards)
        if game.next_throw_on_attacker_exists():
            game.set_next_throw_on_attacker()
        else:
            game.get_players_hash().make_defender_active()
        return self._generator.skip_response(True, self.MESSAGES[0])
    def handle_take_request(self, command):
        '''Handles 'take' command, processes it, returns a response.
        '''
        uid = command.get_uid()
        msg = self._common_check(command)
        if msg != None:
            return self._generator.take_response(False, msg)
        game = self._get_game_by_uid(uid)
        if game.throwing():
            game.reset_throw_on_status()
        game.get_players_hash().get_defender().give_cards(game.table_cards_to_player())
        game.set_next_defender_attacker(True)
        return self._generator.take_response(True, self.MESSAGES[0])
    def handle_retransfer_request(self, command):
        '''Handles 'retransfer' command, processes it, returns a response.
        '''
        uid = command.get_uid()
        msg = self._common_check(command)
        if msg != None:
            return self._generator.retransfer_response(False, msg)
        game = self._get_game_by_uid(uid)
        if game.get_table().has_covered_cards():
            return self._generator.retransfer_response(False, self.MESSAGES[11])
        if not game.retransfer_allowed():
            return self._generator.retransfer_response(False, self.MESSAGES[11])
        retransfer_cards = self._add_name_to_cards(uid, command.get_cards())
        if game.retransfer_cards(retransfer_cards):
            return self._generator.retransfer_response(True, self.MESSAGES[0])
        return self._generator.retransfer_response(False, self.MESSAGES[11])
    def handle_cover_request(self, command):
        '''Handles 'cover' command, processes it, returns a response.
        '''
        uid = command.get_uid()
        msg = self._common_check(command)
        if msg != None:
            return self._generator.cover_response(False, msg)
        cover_set = self._add_name_to_cards(uid, command.get_cards())
        game = self._get_game_by_uid(uid)
        if not game.cards_can_cover_table(cover_set, game.get_trump()):
            return self._generator.cover_response(False, self.MESSAGES[11])
        if game.get_table().get_number_of_uncovered_cards() > cover_set.get_number_of_items():
            return self._generator.cover_response(False, self.MESSAGES[12])
        has_covered = game.get_table().has_covered_cards()
        game.get_players_hash().get_defender().take_away_cards(cover_set.get_covering_cards())
        game.get_table().cover(cover_set)
        if not has_covered:
            game.set_next_throw_on_attacker()
        else:
            game.reset_throw_on_status()
            game.set_next_throw_on_attacker()
        return self._generator.cover_response(True, self.MESSAGES[0])
    def handle_quit_request(self, command):
        '''Handles 'quit' command, processes it, returns a response.
        '''
        if not command.is_valid():
            return self._generator.quit_response(False, self.MESSAGES[11])
        uid = command.get_uid()
        if not uid in self._players.keys():
            return self._generator.quit_response(False, self.MESSAGES[4])
        if not self._players[uid].is_playing_now():
            return self._generator.quit_response(False, self.MESSAGES[11])
        game = self._get_game_by_uid(uid)
        if game.playing():
            player = game.get_players_hash()[uid]
            if not player.is_winner():
                game.finish_game(player)
            game.dec_players()
            if not self._in_test_mode():
                self._players[uid].stops_playing()
        else:
            game.dec_players()
            self._players[uid].stops_playing()
            if game.all_players_left_game():
                self._games.delete_game(game)
                if self._in_test_mode():
                    self._reset_id()
                    self._delete_reged_players()
        return self._generator.quit_response(True, self.MESSAGES[0])
    def _delete_reged_players(self):
        '''Deletes all registered players.
        '''
        while len(self._players.keys()) != 0:
            self._players.popitem()
    def _delete_games(self):
        '''Deletes all games.
        '''
        while len(self._games.keys()) != 0:
            self._games.popitem()    
    def _common_check(self, command):
        '''Performs a common check of an incoming command.
        '''
        uid = command.get_uid()
        if not command.is_valid():
            return self.MESSAGES[11]
        if not uid in self._players.keys():
            return self.MESSAGES[4]
        if not self._players[uid].is_playing_now():
            return self.MESSAGES[11]
        if not self._check_active(uid):
            return self.MESSAGES[10]
    def _check_active(self, uid):
        '''Checks if the player with specified uid
        is active.
        '''
        order = self._get_player_by_uid(uid).get_order()
        active = self._get_game_by_uid(uid).get_active_player()
        if order != active:
            return False
        return True
    def handle_restart_request(self, command):
        self.set_compatibility_test_mode()
        self._delete_reged_players()
        self._delete_games()
        return self._generator.quit_response(True, self.MESSAGES[0])
    def handle_command(self, command):
        '''Handles all commands. Calls a proper handler and
        return its results.
        '''
        command_type = command.get_type()
        if command_type == 'register':
            return self.handle_register(command)
        elif command_type == 'joinGame':
            return self.handle_join(command)
        elif command_type == 'createGame':
            return self.handle_create(command)
        elif command_type == 'getListOfGames':
            return self.handle_games_list_request()
        elif command_type == 'getGameStatus':
            return self.handle_game_status_request(command)
        elif command_type == 'skip':
            return self.handle_skip_request(command)
        elif command_type == 'attack':
            return self.handle_attack_request(command)
        elif command_type == 'take':
            return self.handle_take_request(command)
        elif command_type == 'retransfer':
            return self.handle_retransfer_request(command)
        elif command_type == 'cover':
            return self.handle_cover_request(command)
        elif command_type == 'quit':
            return self.handle_quit_request(command)
        elif command_type == 'restart':
            return self.handle_restart_request(command)