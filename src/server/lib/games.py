'''Containts definition of Game and Games classes.
'''

import deck
import table
import cards
import players

class Game:
    '''Class representing a single game.
    '''
    def __init__(self, number = 2, attack6cards= False, first5cards = False,
                 retransfer  = False, test_mode = False, compatibility_test_mode = False):
        self._test_mode = test_mode
        self._compatibility_test_mode = compatibility_test_mode
        self._players = players.Players_In_Game()
        self._deck = deck.Deck(compatibility_test_mode)
        if not (test_mode or compatibility_test_mode):
            self._deck.shuffle()
        self._trump_card = self._deck.show_trump_card()
        self._trump_card = self._deck.show_trump_card()
        self._table = table.Table()
        self._out = cards.Cards()
        self._number_of_players = number
        self._retransfer = retransfer
        self._first_attack_5cards = first5cards
        self._attack_6cards = attack6cards
        self._attack_counter = 0
        self._finished = False
        self._first_turn = True
        self._players_left = 0
        self._primary_attacker = None
        self._primary_defender = None
    def _param_encl(self, smth):
        '''Returns '{smth}'
        '''
        return '{' + smth + '}'
    '''Get game information
    '''
    def test_mode(self):
        '''Returns True if the game_server and the game are in test mode.
        False otherwise.
        '''
        return self._test_mode
    def compatibility_test_mode(self):
        '''Returns True if the game_server and
        the game are in comaptibility mode.
        False otherwise.
        '''
        return self._compatibility_test_mode
    def get_number_of_players(self):
        '''Returns number of players in the game.
        '''
        return self._number_of_players
    def get_trump_str(self):
        '''Return [cA] if cA is a trump.
        '''
        return '[' + str(self._trump_card) + ']'
    def _now_first_turn(self):
        '''Returns True if the current turn is the first.
        '''
        return self._first_turn
    def _finish_first_turn(self):
        '''Finishes the first turn.
        '''
        self._first_turn = False
    def get_trump(self):
        '''Returns the trump (cards.Card object).
        '''
        return self._trump_card
    def get_table_str(self):
        '''Returns string representation of the table.
        '''
        return str(self._table)
    def get_table(self):
        '''Returns game's table.
        '''
        return self._table
    def get_deck_str(self):
        '''Returns string representation of the deck.
        '''
        return self._deck.get_common_repr()
    def get_deck(self):
        '''Returns game's deck.
        '''
        return self._deck
    def get_out(self):
        '''Returns games's out.
        '''
        return self._out
    def get_out_str(self):
        '''Returns string representation of game's out.
        '''
        return self._out.get_str_repr()
    def get_options(self):
        '''Returns string with game options.
        '''
        response = self._param_encl('numberOfPlayers' + str(self.get_number_of_players()))
        if self.attack_6cards():
            response += self._param_encl('attack6Cards')
        if self.first_5cards():
            response += self._param_encl('firstAttack5Cards')
        if self.retransfer_allowed():
            response += self._param_encl('canRetransfer')
        return response
    def dec_players(self):
        '''Memorizes one player left the game.
        '''
        self._players_left = self._players_left + 1
    def all_players_left_game(self):
        '''Returns True if all players left the game.
        '''
        return self._players_left == self.get_number_of_players()
    def get_players(self):
        '''Return players in game.
        '''
        players = self._players.get_players_in_game()
        players.sort()
        return players
    def get_players_hash(self):
        '''Returns player in game with their names.
        '''
        return self._players
    def needs_players(self):
        '''Returns True if game needs players to start.
        '''
        return self._number_of_players > self._players.get_number_of_players()
    def retransfer_allowed(self):
        '''Returns True if retransfer option is enabled.
        '''
        return self._retransfer
    def first_5cards(self):
        '''Returns True if first attack 5 cards restriction is enabled.
        '''
        return self._first_attack_5cards
    def attack_6cards(self):
        '''Returns True if attack 6 cards restriction is enabled.
        '''
        return self._attack_6cards
    def get_active_player(self):
        '''Returns the number of active player in the game.
        '''
        return self._players.get_active_player()
    def playing(self):
        '''Returns True if the game is not finished.
        False otherwise.
        '''
        return not self._finished
    def finished(self):
        '''Returns True if the game is finished.
        False otherwise.
        '''
        return self._finished
    def game_started(self):
        '''Returns True if the game is already started.
        '''
        return not self.needs_players()
    def _give_cards_to_player(self, player):
        '''Gives to the 'player' player cards from the deck.
        '''
        if player.get_number_of_cards() < 6:
            player.give_cards(self._deck.take_cards(6 - player.get_number_of_cards()))
    def finish_game(self, player_fool=None):
        '''Finishes game. Sets winners and a fool players.
        '''
        for player in self._players.get_players_in_game():
            player.make_winner()
        if player_fool != None:
            player_fool.make_fool()
        self._finished = True
    def check_players_statuses(self):
        '''Makes players without cards winners.
        If only one player has cards he becomes a fool.
        '''
        winners = 0
        possible_fool = None
        for player in self._players.get_players_in_game():
            if player.get_number_of_cards() == 0:
                player.make_winner()
                winners = winners + 1
            else:
                possible_fool = player
        if winners == self.get_number_of_players():
            self.finish_game()
        if winners + 1 == self.get_number_of_players():
            self.finish_game(possible_fool)
    def set_next_defender_attacker(self, defender_took_cards):
        '''Sets next defender and attacker.
        '''
        self._table.clear()
        self._finish_first_turn()
        attacker = self._players.get_attacker()
        defender = self._players.get_defender()
        attacker_order = attacker.get_order()
        defender_order = defender.get_order()
        self._give_cards_check_finishing(defender_took_cards)
        if not self.finished():
            if not defender_took_cards:
                if defender.is_winner():
                    self._players.make_attacker_after(defender_order)
                else:
                    self._players.make_attacker(defender_order)
                new_attacker_order = self._players.get_attacker().get_order()
                self._players.set_active_player(new_attacker_order)
                self._players.make_defender_after(new_attacker_order)
            else:
                self._players.make_attacker_after(defender_order)
                new_attacker_order = self._players.get_attacker().get_order()
                self._players.set_active_player(new_attacker_order)
                self._players.make_defender_after(new_attacker_order)
            self._primary_attacker = self._players.get_attacker()
            self._primary_defender = self._players.get_defender()
    def _give_cards_check_finishing(self, defender_took_cards):
        '''Give cards to players. Check if the game is finished.
        '''
        attacker = self._primary_attacker
        defender = self._primary_defender
        self._give_cards_to_player(attacker)
        for player in self._players.get_players_in_game():
            if player not in [attacker, defender]:
                self._give_cards_to_player(player)
        self._give_cards_to_player(defender)
        self.check_players_statuses()
    def _defender_has_additional_cards(self, retransfer_cards):
        '''Checks if defender has all retransfer_cards cards.
        '''
        defender = self._players.get_defender()
        defender_added = False
        for card in retransfered_cards:
            if not defender.has_card(card):
                if not self._table.has_card(card):
                    return False
            else:
                defender_added = True
        return defender_added
    def retransfer_cards(self, retransfer_cards):
        '''Make all operations retransferring cards to another player.
        '''
        if not retransfer_cards.all_different():
            return False
        if not self._players.get_defender().has_cards(retransfer_cards):
            return False
        new_defender = self._players.get_defender_for_retransfer()
        if new_defender == None:
            return False
        for card in retransfer_cards:
            if not self.get_table().has_same_value(card.get_value()):
                return False
        to_cover = retransfer_cards.get_number_of_cards() + self.get_table().get_number_of_cards()
        if new_defender.get_number_of_cards() < to_cover:
            return False 
        if not self._table.add_retransfered(retransfer_cards):
            return False
        self.get_players_hash().get_defender().take_away_cards(retransfer_cards)
        if new_defender.is_attacker():
            new_attacker = self.get_players_hash().get_defender()
            self._players.make_attacker(new_attacker.get_order())
        self._players.make_defender(new_defender.get_order())
        self._players.make_defender_active()
        return True
    def check_first_attacker_cards(self, attack_cards):
        '''Checks cards that are put on the table by the first attacker.
        '''
        if not attack_cards.all_different():
            return False
        defender_to_cover = attack_cards.get_number_of_cards()
        defender_can_cover = self._players.get_defender().get_cards().get_number_of_cards()
        if not self._table.possible_to_put_cards(attack_cards):
            return False
        if not self._attacker_has_cards(attack_cards):
            return False
        if defender_to_cover > defender_can_cover:
            return False
        return True
    def _check_throw_on_cards(self, command):
        '''Checks cards thrown by a player.
        '''
        to_throw = command.get_cards()
        length = to_throw.get_number_of_cards()
        defender_to_cover = self._table.get_number_of_uncovered_cards() + length
        all_to_cover = self._table.get_number_of_items() + length
        defender_can_cover = self._players.get_defender().get_cards().get_number_of_cards()
        if not to_throw.all_different():
            return False
        for card in to_throw:
            if not self._table.possible_to_throw_on(card):
                return False
        if not self._attacker_has_cards(to_throw):
            return False
        if all_to_cover > 6 and self.attack_6cards():
            return False
        if self._now_first_turn() and (all_to_cover > 5) and self.first_5cards():
            return False
        if defender_to_cover > defender_can_cover:
            return False
        return True
    def cards_can_cover_table(self, cover_set, trump_card):
        '''Returns True if cover_set can be used for covering table.
        False otherwise.
        '''
        trump_suit = trump_card.get_suit()
        for pair in cover_set:
            if not self._table.has_as_not_covered(pair[0]):
                return False
            pair[0].set_trump_suit(trump_suit)
            pair[1].set_trump_suit(trump_suit)
            if not pair[0] < pair[1]:
                return False
        if not self._defender_has_cards(cover_set.get_covering_cards()):
            return False
        if not cover_set.convert_to_cards().all_different():
            return False
        return True
    def _defender_has_cards(self, attack_cards):
        '''Returns True if current defender has attack_cards cards.
        False otherwise.
        '''
        defender_cards = self._players.get_defender().get_cards()
        for card in attack_cards:
            if not defender_cards.has_card(card):
                return False
        return True
    def _attacker_has_cards(self, attack_cards):
        '''Returns True if current attacker has attack_cards cards.
        False otherwise.
        '''
        attacker_cards = self._players.get_attacker().get_cards()
        for card in attack_cards:
            if not attacker_cards.has_card(card):
                return False
        return True
    def throwing(self):
        '''Returns True if throwing is started.
        '''
        return self._attack_counter != 0
    def _inc_throw_on_attacker(self):
        '''Memorizes one player has thrown cards.
        '''
        self._attack_counter = self._attack_counter + 1
    def next_throw_on_attacker_exists(self):
        '''Returns True if next player to throw on exists.
        Return False otherwise.
        '''
        possible_attackers = []
        for player in self._players.values():
            if not (player.finished_playing() or player.is_defender()):
                possible_attackers.append(player)
        return self._attack_counter != len(possible_attackers)
    def reset_throw_on_status(self):
        '''Resets throwing on players counter.
        '''
        self._attack_counter = 0
    def set_next_throw_on_attacker(self):
        '''Makes next player to throw on an attacker.
        '''
        after = None
        if not self.throwing():
            after = self._players.get_defender().get_order()
        else:
            after = self._players.get_attacker().get_order()
        self._players.make_attacker_after(after)
        self._players.set_active_player(self._players.get_attacker().get_order())
        self._inc_throw_on_attacker()
        return True
    def _get_least_trump_value(self, player_cards):
        '''Returns the least trump value in player_cards.
        '''
        trump_value = None
        trump_suit = self.get_trump().get_suit()
        for player_card in player_cards:
            player_suit = player_card.get_suit()
            player_value = player_card.get_value()
            if player_suit == trump_suit:
                if trump_value == None:
                    trump_value = player_value
                elif cards.VALUES.index(trump_value) > cards.VALUES.index(player_value):
                    trump_value = player_value
        return trump_value
    def _number_with_least_trump(self, players_cards):
        '''Returns the number of list of cards
        in players_cards with the least trump.
        '''
        least = None
        prev_trump_value = None
        for player_cards in players_cards:
            trump_value = self._get_least_trump_value(player_cards)
            if trump_value != None:
                if prev_trump_value == None:
                    prev_trump_value = trump_value
                    least = players_cards.index(player_cards)
                elif cards.VALUES.index(trump_value) < cards.VALUES.index(prev_trump_value):
                    prev_trump_value = trump_value
                    least = players_cards.index(player_cards)
        return least
    def _start_game(self):
        '''Prepare everything for playing.
        '''
        if self.compatibility_test_mode():
            for i in range(1, self._players.get_number_of_players()+1):
                player = self._players.get_by_order(i)
                player.give_cards(self._deck.take_cards(6))
                if i == 1:
                    player.make_attacker()
                    self._players.set_active_player(1)
                    self._players.make_defender_after(1)
        else:
            least = None
            players_cards = None
            while least == None:
                players_cards = []
                for i in range(self.get_number_of_players()):
                    players_cards.append(self._deck.take_cards(6))
                if not self.test_mode():
                    least = self._number_with_least_trump(players_cards)
                else:
                    least = 0
            players_names = self._players.keys()
            for i in range(self.get_number_of_players()):
                player = self._players.get_by_order(i+1)
                player.give_cards(players_cards[i])
                if i == least:
                    player.make_attacker()
                    self._players.set_active_player(player.get_order())
                    self._players.make_defender_after(player.get_order())
        self._primary_attacker = self._players.get_attacker()
        self._primary_defender = self._players.get_defender()
                
                
    '''    least = None
        players_cards = cards.Cards()
        while least == None:
            if not self.test_mode():
                self._deck.shuffle()
            self._trump_card = self._deck.show_trump_card()
            for i in range(self.get_number_of_players()):
                players_cards.append(self._deck.take_cards(6))
            if not self.test_mode():
                least = self._number_with_least_trump(players_cards)
            else:
                least = 0
        players_names = self._players.keys()
        for i in range(self.get_number_of_players()):
            player = self._players[players_names[i]]
            player.give_cards(players_cards[i])
            if i == least:
                player.make_attacker()
                self._players.set_active_player(player.get_order())
                self._players.make_defender_after(player.get_order())'''

    def add_registered_player(self, uid, registered_player):
        '''Adds a new player to the game.
        '''
        if self.needs_players():
            self._players.new_player(uid, registered_player)
            if not self.needs_players():
                self._start_game()
            return True
        return False
    def table_cards_to_player(self):
        '''Returns all cards from table.
        '''
        self._remove_names_from_table()
        return self.get_table().convert_to_cards()
    def _remove_names_from_table(self):
        '''Removes all names of cards' owners from cards
        on the table.
        '''
        for card in self._table.convert_to_cards():
            card.forget_owner()
    def table_to_out(self):
        '''Sends cards on table to out.
        '''
        self._remove_names_from_table()
        self.send_to_out(self._table.convert_to_cards())
    def send_to_out(self, to_send):
        '''Sends to_out (card or a cover pair) to out.
        '''
        if isinstance(to_send, list):
            self._out.add_cards(to_send)
        else:
            self._out.add_card(to_send)


class Games(dict):
    '''For storing all game objects.
    '''
    def new_game(self, name, number, attack6cards, first5cards,
                 retransfer, test_mode=False, compatibility_test_mode=False):
        '''Adds a new game.
        '''
        self[name] = Game(number, attack6cards, first5cards,
                          retransfer, test_mode, compatibility_test_mode)
    def get_game_objects(self):
        '''Returns objects representing all existing games.
        '''
        return self.values()
    def get_game_names(self):
        '''Returns a list with names of all games.
        '''
        game_names = self.keys()
        game_names.sort()
        return game_names
    def delete_game(self, game):
        '''Delete specified game.
        '''
        other_games = {}
        while len(self.keys()) != 0:
            poped = self.popitem()
            if poped[1] != game:
                other_games[poped[0]] = poped[1]
        self.update(other_games)