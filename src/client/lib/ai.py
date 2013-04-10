'''Contains definition of Ai class and additional classes - Player_Cards_Probabilities
and Players_Cards_Probabilities.
'''

DECK = "0deck"
OUT = "0out"
TABLE = "0table"

F1 = "first_attacking"
F2 = "first_attacked"
M1 = "multiple_attacking"
M2 = "multiple_attacked"

import cards
import table
import requestor
import client_generator
import server_response
import client_parser

def cards_converter(smth):
    '''Converts list of cards.Card objects to strings.
    '''
    converted = []
    for x in smth:
        if isinstance(x, cards.Card):
            converted.append(x.get_card_str())
        else:
            converted.append(x)
    return converted

class Player_Cards_Probabilities(dict):
    '''Stores cards probabities for a single player.
    '''
    def __init__(self):
        self.number = 6
        for value in cards.VALUES:
            for suit in cards.SUITS:
               self[suit + value] = 0
    def recalculate_probabilities(self, card, added, miss_them = []):
        '''Recalculates player's probabilities so that
        sum of probabilities stays the same - equals his number of cards.
        '''
        old_sum = 0.0
        for card_name in self.keys():
            if (card_name != card) and (self[card_name] != 1) and not (card_name in miss_them):
                old_sum = old_sum + self[card_name]
        new_sum = 0.0 + old_sum - added
        if old_sum == 0:
            return False
        k = new_sum/old_sum
        if (k < 0):
            return False
        for card_name in self.keys():
            if (card_name != card) and (self[card_name] != 1) and not (card_name in miss_them):
                self[card_name] = self[card_name] * k
        return True
    def all_cards_known(self):
        '''Checks if all cards of this player have probabilitiy 0 or 1.
        '''
        for probability in self.values():
            if not probability in [0, 1]:
                return False
        return True
    def set_number_of_cards(self, n):
        '''Changes number of player's cards.
        '''
        self.number = n
    def get_number_of_cards(self):
        '''Gets number of player's cards.
        '''
        return self.number

class Players_Cards_Probabilities(dict):
    '''Stores data about all players' cards probabilites.
    '''
    #Initializing table
    def __init__(self, players, owner, cards, trump = None):
        self.n = 5
        self._file = "probability_table"
        self.insert_player(DECK)
        self.insert_player(OUT)
        self.insert_player(TABLE)
        self[TABLE].set_number_of_cards(0)
        self[OUT].set_number_of_cards(0)
        self[DECK].set_number_of_cards(36 - len(players)*6) 
        if len(players) == 6:
            trump = None
        for player in players:
            self.insert_player(player)
        #remember our cards
        for card in cards:
            self[owner][card] = 1
        #calculte initial probabilities
        player_fill = 6/30.0
        deck_fill = 0.0
        if trump != None:
            self[DECK][trump] = 1
            deck_fill = (29 - 6*(len(players)-1))/29.0
            player_fill = 6/29.0
        #fill in
        for deck_card in self[DECK].keys():
            if (deck_card != trump) and not (deck_card in cards):
                self[DECK][deck_card] = deck_fill
        for player in self.keys():
            if player not in [owner, DECK, OUT, TABLE]:
                for player_card in self[player].keys():
                    if (player_card != trump) and not (player_card in cards):
                        self[player][player_card] = player_fill
    def get_str_table(self):
        '''Returns string presentation of this object.
        For tester module only.
        '''
        return str(self)
    def insert_player(self, name):
        '''Inserts new player, initializes his table.
        '''
        self[name] = Player_Cards_Probabilities()
    def check_number_of_cards(self, number_of_cards):
        '''Changes probabilities so now players have new number of cards.
        Proportionality of probabilities is kept.
        '''
        for name in number_of_cards.keys():
            counter = 0
            for card in self[name].keys():
                if self[name][card] == 1:
                    counter = counter + 1
            old = self[name].get_number_of_cards() - counter
            if old == 0:
                continue
            new = number_of_cards[name] - counter
            k = float(new) / old
        self[name].set_number_of_cards(number_of_cards[name])
        for card in self[name].keys():
                if self.probability_changeable(name, card):
                    added = self[name][card] * (k - 1)
                    self[name][card] = self[name][card] * k
                    self.recalculate_column_probabilities(name, card, added)
        return True

    #These methods must be used for changing table values
    def inc(self, name, card_name, delta):
        '''Increments the probability of 'card_name' card on hands
        of player with name 'name'.
        '''
        if not self.probability_changeable(name, card_name):
            return False
        if not correct_probability(self[name][card_name] + delta):
            return False
        self[name][card_name] = self[name][card_name] + delta
        if not self.recalculate_probabilities(name, card_name, delta):
            return False
        return True
    def mul(self, owner, card, times):
        '''Multiplies the possibility of 'card' at 'owner' 'times' times.
        '''
        if times <= 0:
            return False
        if not self.probability_changeable(owner, card):
            return False
        old_value = self[owner][card]
        new_value = old_value * times
        if new_value > 1:
            new_value = 1
        if not self.correct_probability(new_value):
            return False
        self[owner][card] = new_value
        if not self.recalculate_probabilities(owner, card, new_value - old_value):
            return False
        return True
    #Methods used for changing values
    def correct_probability(self, p):
        '''Checks if p is a correct probability value.
        '''
        return (p >= 0) and (p <= 1)
    def probability_changeable(self, name, card_name):
        '''Checks if it is possible to change the probability of
        'card_name' card on hands of player with name 'name'.
        '''
        return not ( self._noone_has(card_name) or
                     self._someone_has(card_name) or
                     self[name].all_cards_known() )
    def recalculate_probabilities(self, name, card, added, miss_them = []):
        '''Recalculates probabilities of cards of player with name 'name'
        and changes all other probabilities in the table to make it consistent.
        '''
        result = self[name].recalculate_probabilities(card, added, miss_them)
        result = result and self.recalculate_column_probabilities(name, card, added)
        return result
    def recalculate_column_probabilities(self, name, card, added):
        '''Recalculates probabilities of the card 'card' on hands of other players,
        and then recalculates probabilities of other cards on hands of each of these players.
        '''
        new_sum = 1.0 - self[name][card]
        old_sum = new_sum + added
        k = new_sum / old_sum
        result = True
        for player_name in self.keys():
            if player_name != name:
                to_add = (k - 1) * self[player_name][card]
                self[player_name][card] = self[player_name][card] + to_add
                self[player_name].recalculate_probabilities(card, to_add)
        return True

    #Methods used for setting owner of cards and getting owner
    def set_owner(self, card, name):
        '''Sets the owner of the card.
        '''
        result = True
        if self[name][card] == 1:
            return False
        old_value = self[name][card]
        self[name][card] = 1
        result = self.recalculate_probabilities(name, card, 1 - old_value)
        for player_name in self.keys():
            if name != player_name:
                old_value = self[player_name][card]
                self[player_name][card] = 0
                result = result and self[player_name].recalculate_probabilities(card, -old_value)

    def set_noone_has(self, card):
        '''Rememberes that card was sent to out.
        '''
        self.set_owner(card, OUT)
    def set_table_has(self, card):
        '''Rememberes that card is on the table.
        '''
        self.set_owner(card, TABLE)
    def _noone_has(self, card_name):
        '''Checks that noone has this card.
        '''
        for player_name in self.keys():
            if self[player_name][card_name] != 0:
                 return False
        return True
    def _someone_has(self, card_name):
        '''Checks if one of the players has this card with
        probability 1.
        '''
        for player_name in self.keys():
            if self[player_name][card_name] == 1:
                 return True
        return False

    #String representation
    def output(self, file=None):
        '''Outputs the table to the file.
        '''
        if file == None:
            file = self._file
        f = open(file + ".txt", mode = 'w')
        f.write("\t" + TABLE)
        f.write("\t\t" + DECK)
        f.write("\t\t" + OUT)
        for name in self.keys():
            if name in [DECK, TABLE, OUT]:
                continue
            f.write("\t\t" + name)
        f.write("\n")
        for suit in cards.SUITS:
            for value in cards.VALUES:
                card = suit + value
                f.write(card + "\t")
                f.write(str(int(self[TABLE][card] * (10**self.n)) * (10**-self.n)))
                f.write("\t\t")
                f.write(str(int(self[DECK][card] * (10**self.n)) * (10**-self.n)))
                f.write("\t\t")
                f.write(str(int(self[OUT][card] * (10**self.n)) * (10**-self.n)))
                f.write("\t\t")
                for name in self.keys():
                    if name in [DECK, OUT, TABLE]:
                        continue
                    f.write(str(int(self[name][card] * (10**self.n)) * (10**-self.n)))
                    f.write("\t\t")
                f.write("\n")
            f.write("\n")
        f.close()
        return ""


class Ai:
    '''Contains all methods for extracting info from statuses
    and generating actions.
    '''
    def __init__(self, req=None, uid=None):
        self._uid = uid
        self._probs = None
        self._trump_card = None
        self._out = cards.Cards()
        self._saved_table = table.Table()
        self._options = [False, False, False]
        self._number_of_cards = 0
        self.prev_status = None
        self.new_status = None
        self.prev_state = None
        self.new_state = None
        self.requestor = req
        self._name = ""
        self.last_action_failed = False
        self.queued_commands = []
        self.gener = client_generator.Client_Generator()
        self._parser = client_parser.Client_Parser()
        self._file = "thought_records"
    def log(self, *smth):
        '''Logging function.
        Logs to a "standard_file_name + uid" file.
        '''
        f = open(self._file + self._uid, "a")
        for s in smth:
            f.write(str(smth) + " ")
        f.write("\n")
        f.close()
    def set_requestor(self, requestor):
        '''Sets object for communicating with the server.
        '''
        self.requestor = requestor
    def set_uid(self, uid):
        '''Sets player's uid.
        '''
        self._uid = uid
    def reset(self):
        '''Resets some data.
        '''
        self._probs = None
        self._trump_card = None
        self.prev_status = None
        self.new_status = None
        self.prev_state = None
        self.new_state = None
        self.requestor = req
        self.last_action_failed = False
        self.queued_commands = []
    #Game options getters & setter
    def retransfer_allowed(self):
        '''Retuns True if retransfer is allowed.
        Returns False otherwise.
        '''
        return self._options[2]
    def first_attack5_restrict(self):
        '''Retuns True if first attack 5 cards restriction is on.
        Returns False otherwise.
        '''
        return self._options[1]
    def attack6_restrict(self):
        '''Retuns True if attack 6 cards restriction is on.
        Returns False otherwise.
        '''
        return self._options[0]
    def set_options(self, options):
        self._options = options

    #Functions comparing previous and new statuses
    def get_thrown_on_cards(self):
        '''Get all cards thrown on.
        '''
        left = self.prev_status.get_table().get_bottom_cards()
        right = self.new_status.get_table().get_bottom_cards()
        return right[len(left):len(right)]
    def same_covering_cards(self):
        '''Checks if tables have equal covering cards.
        '''
        left = self.prev_status.get_table().get_covering_cards()
        right = self.new_status.get_table().get_covering_cards()
        if len(left) != len(right):
            return False
        for i in range(len(left)):
            if left[i] != right[i]:
                return False
        return True
    def statuses_are_different(self):
        '''Checks if statuses have differences.
        '''
        prev = self.prev_status
        new = self.new_status
        if not self.same_turn():
            return True
        data = {}
        for player in prev.get_all_players_info():
            data[player.get_name()] = [player.get_number_of_cards(), player.get_status()]
        for player in new.get_all_players_info():
            if ((player.get_number_of_cards() != data[player.get_name()][0]) or
                (player.get_status() != data[player.get_name()][1])):
                return True
        my_prev_cards = [str(card) for card in prev.get_my_info().get_cards()]
        my_new_cards = [str(card) for card in new.get_my_info().get_cards()]
        if len(my_prev_cards) != len(my_new_cards):
            return True
        for card in my_prev_cards:
            if not card in my_new_cards:
                return True
        return False
    def same_defender(self):
        '''Checks if defender is the same.
        '''
        pd = self.prev_status.get_defender().get_order()
        nd = self.new_status.get_defender().get_order()
        return pd == nd
    def same_turn_with_defender(self):
        '''Checks if the turn is the same and defender is
        not changed.
        '''
        return self.same_turn() and self.same_defender()
    def same_turn(self):
        '''Checks if same turn continues.
        '''
        if self.first_status():
            return True
        if (len(self.prev_status.get_out()) != len(self.new_status.get_out())):
            return False
        ptable = self.prev_status.get_table()
        ntable = self.new_status.get_table()
        plen = len(ptable)
        nlen = len(ntable)
        if plen > nlen:
            return False
        for i in range(plen):
            if isinstance(ntable[i], cards.Card):
                if not isinstance(ptable[i], cards.Card):
                    return False
                if ptable[i] != ntable[i]:
                    return False
            else:
                if isinstance(ptable[i], cards.Card):
                    if ptable[i] != ntable[i][0]:
                        return False
                elif (ntable[i][0] != ptable[i][0]) or (ntable[i][1] != ntable[i][1]):
                    return False
        return True
    def cards_sent_to_out(self):
        '''Returns True if all cards were sent to out.
        Otherwise returns False.
        '''
        set = cards_converter(self.prev_status.get_table().convert_to_cards())
        out = cards_converter(self.new_status.get_out())
        for card in set:
            if not card in out:
                return False
        return True
    def new_table_empty(self):
        return self.new_status.get_table().is_empty()    
    #Functions for getting common game status info
    def is_active(self):
        '''Checks if i am an active player.
        '''
        return self.new_status.get_my_info().is_active()
    def half_game_passed(self):
        '''Checks if half game has passed.
        '''
        return int(self.new_status.get_cards_in_deck()) < 18
    def empty_deck(self):
        '''Checks if deck is almost empty.
        '''
        return int(self.new_status.get_cards_in_deck()) <= 1
    def quarter_game_passed(self):
        '''Checks if quarter game has passed.
        '''
        return int(self.new_status.get_cards_in_deck()) < 20
    def last_cover_quarter_game(self):
        '''Checks if last quarter of a game goes on.
        '''
        return int(self.new_status.get_cards_in_deck()) < 14
    def last_attack_quarter_game(self):
        '''Checks if last quarter of a game goes on.
        '''
        return int(self.new_status.get_cards_in_deck()) < 7
    def action_failed(self):
        '''Checks if previous action failed.
        '''
        return self.last_action_failed
    def is_first_turn(self):
        '''Checks if out is empty == first turn goes.
        '''
        return len(self.new_status.get_out()) == 0
    def first_attack_in_turn(self):
        '''Checks if no covered cards on the table.
        '''
        return not self.new_status.get_table().has_covered_cards()
    def not_first_status(self):
        '''Checks if got status isn't first.
        '''
        return self.prev_status != None
    def first_status(self):
        '''Checks if got status is first.
        '''
        return self.prev_status == None
    def is_coverable(self, a, b):
        '''Checks if b can cover a.
        '''
        trump_suit = self.new_status.get_trump_card().get_suit()
        if a.get_suit() == b.get_suit():
            return cards.VALUES.index(a.get_value()) < cards.VALUES.index(b.get_value())
        if b.get_suit() == trump_suit:
            return True
        return False
    def get_trump_suit(self):
        '''Returns trump suit.
        '''
        return self.new_status.get_trump_card().get_suit()
    def calc_average_value(self, bottom):
        '''Calculated average cards value.
        '''
        value = 0.0
        for card in bottom:
            value += cards.VALUES.index(card.get_value())
            if card.get_suit() == self.get_trump_suit():
                value = value + 9
        value = value / len(bottom)
        return value

    #Queue methods
    def queue_command(self, cmd):
        '''Queues any command.
        '''
        self.queued_commands.append(cmd)
    def queue_attack_cards(self, attack_cards):
        '''Queues attack commands for all card sets in attack_cards.
        '''
        for set in attack_cards:
            self.queue_command(self.gener.attack(self._uid, set))
    def queue_retransfer_cards(self, set):
        '''Queues retransfer commands for given set.
        '''
        self.queue_command(self.gener.retransfer(self._uid, set))
    def queue_cover_cards(self, cover_cards):
        '''Queues  cover commands for given cards.
        to_cover contains cards to be covered. cover_cards contains
        all possible sets to use for covering.
        '''
        for set in cover_cards:
            self.queue_command(self.gener.cover(self._uid, set))
    def queue_throw_on_cards(self, throw_on_cards):
        '''Queues throw_on (==attack) commands for all card sets in attack_cards.
        '''
        for set in throw_on_cards:
            self.queue_command(self.gener.attack(self._uid, set))
    def queue_quit(self):
        '''Queues quit command.
        '''
        self.queue_command(self.gener.quit(self._uid))
    def queue_take(self):
        '''Queues take command.
        '''
        self.queue_command(self.gener.take(self._uid))
    def queue_skip(self):
        '''Queues skip command.
        '''
        self.queue_command(self.gener.skip(self._uid))
    def clear_queue(self):
        '''Clears queue.
        '''
        self.queued_commands = []
    def print_queue(self):
        '''Prints queue.
        '''
        print self.queued_commands
    def get_str_queue(self):
        '''Returns string presentation of the queue.
        '''
        return str(self.queued_commands)


    #Extracting all possible information
    def think(self, status):
        '''Extracts all possible information from status,
        from difference of new and previous statuses.
        '''
        if status.game_continues():
	    self.initiate(status)
            self.get_data_from_new_status(status)
            self.extract_differ_info()
            self.memorize_as_prev_status()

    #Initiation
    def initiate(self, status):
        '''Initiates probability table if first status receive.
        '''
        if self.prev_status == None:
            self._probs = Players_Cards_Probabilities(
                              [player.get_name() for player in status.get_all_players_info()],
                              status.get_my_info().get_name(),
                              [str(card) for card in status.get_my_info().get_cards()],
                              str(status.get_trump_card()))
            self._name = status.get_my_info().get_name()
            self.set_options(status.get_game_options())

    #Extracting data from status
    def get_data_from_new_status(self, status):
        '''Extracts simple data - from table, out, etc.
        '''
        self.new_status = status
        self.extract_out_info()
        self.extract_table_info()
        self.extract_my_cards_info()
        self.check_number_of_cards()
        self.get_table_state()
    def get_name(self):
        '''Returns players name.
        '''
        return self._name
    def extract_my_cards_info(self):
        '''Remembers what cards do I have.
        '''
        my_cards = self.new_status.get_my_info().get_cards()
        for card in my_cards:
            self._probs.set_owner(str(card), self.get_name())
    def extract_out_info(self):
        '''Remembers what cards sent to out.
        '''
        for card in self.new_status.get_out():
            self._probs.set_noone_has(str(card))
    def extract_table_info(self):
        '''Remembers what cards are on the table and uses
        some differential info to know that some cards were taken from table
        but we missed proper status.
        '''
        table_cards = cards_converter(self.new_status.get_table().convert_to_cards())
        out_cards = cards_converter(self.new_status.get_out())
        my_name = self.new_status.get_my_info().get_name()
        my_cards = cards_converter(self.new_status.get_my_info().get_cards())
        for card in table_cards:
            self._probs.set_table_has(card)
        if self.not_first_status():
            prev_defender = self.prev_status.get_defender().get_name()
            for card in self._probs[my_name].keys():
                if ((self._probs[my_name][card] == 1) and not (card in my_cards) and
                    not (card in table_cards) and not (card in out_cards)):
                    self._probs.set_owner(card, prev_defender)
   
    def get_table_state(self):
        '''Detects table's status used for extracting differential info.
        '''
        if self.new_status.get_table().is_empty():
           self.new_state = F1
        elif (not self.new_status.get_table().has_covered_cards()
            and self.new_status.defender_is_active()):
            self.new_state = F2
        elif (self.new_status.get_table().has_covered_cards()
              and self.new_status.attacker_is_active()):
            self.new_state = M1
        elif (self.new_status.get_table().has_covered_cards()
              and self.new_status.defender_is_active()):
            self.new_state = M2
    def check_number_of_cards(self):
        '''Sets new number of cards for players and deck.
        '''
        new_numbers = {}
        my_name = self.new_status.get_my_info().get_name()
        for player in self.new_status.get_other_players_info():
            new_numbers[player.get_name()] = int(player.get_number_of_cards())
        new_numbers[my_name] = len(self.new_status.get_my_info().get_cards())
        new_numbers[DECK] = self.new_status.get_cards_in_deck()
        self._probs.check_number_of_cards(new_numbers)
    def memorize_as_prev_status(self):
        '''Memorize new status as a previous one.
        '''
        self.prev_status = self.new_status
        self.prev_state = self.new_state
    #Extracting differential info
    def extract_differ_info(self):
        '''Extracts all possible differential information.
        '''
        if self.not_first_status() and self.statuses_are_different():
            self.extract_throwing_info()
            self.extract_retransfer_info()
            self.extract_attacked_info()
            self.extract_covering_info()
    def throwing_on(self):
        '''Checks if throwing on is going on now.
        '''
        if not self.same_turn():
            return False
        if self.new_state in [M1, M2]:
            return True
        return False 
    def extract_throwing_info(self):
        '''Extract some data about who threw on cards.
        '''
        if not self.throwing_on():
            return
        if self.same_covering_cards():
            #trying to get throwers
            throwers = dict()
            new_attacker_name = ""
            prev_attacker_order = 0
            for player in self.new_status.get_all_players_info():
                if player.get_status() == "_attacker_":
                    new_attacker_name = player.get_name()
            for player in self.prev_status.get_all_players_info():
                if player.get_status() != "_defender_":
                    throwers[player.get_order()] = player.get_name()
                    if player.get_status() == "_attacker_":
                        prev_attacker_order = player.get_order()
            if (self.prev_state == F1 or self.prev_state == F2):
                prev_attacker_order = prev_attacker_order + 1
            first_order = []
            second_order = []
            for order in throwers.keys():
                if order >= prev_attacker_order:
                    first_order.append(throwers[order])
                else:
                    second_order.append(throwers[order])
            #getting throwable values
            throwers = first_order + second_order
            thrown_on = self.get_thrown_on_cards()
            throwable_values = []
            for card in self.prev_status.get_table().convert_to_cards():
                if not card.get_value() in throwable_values:
                    throwable_values.append(card.get_value())
            #about each player who could throw on
            for thrower in throwers:
                if (self.new_state == M1) and (thrower == new_attacker_name):
                    break
                thrower_cards = []
                #what did he throw on?
                for card in thrown_on:
                    if card.get_owner() == thrower:
                        thrower_cards.append(card)
                #make a conclusion about his cards
                for card_value in throwable_values:
                    not_thrown = []
                    for suit in cards.SUITS:
                        not_thrown.append(suit + card_value)
                    for card in thrower_cards:
                        if card.get_value() == card_value:
                            not_thrown.pop(not_thrown.index(card.get_card_str()))
                    for card in not_thrown:
                        self._probs.mul(thrower, card, 0.9)
                if thrower == new_attacker_name:
                    break
        else:
            throwers = []
            thrown_on = self.get_thrown_on_cards()
            throwable_values = []
            #get all throwers
            for card in thrown_on:
                if not card.get_owner() in throwers:
                    throwers.append(card.get_owner())
            #get all throwable values
            for card in self.prev_status.get_table().convert_to_cards():
                if not card.get_value() in throwable_values:
                    throwable_values.append(card.get_value())
            for thrower in throwers:
                #what did he throw on?
                thrower_cards = []
                for card in thrown_on:
                    if card.get_owner() == thrower:
                        thrower_cards.append(card)
                #what could he throw on?
                for card_value in throwable_values:
                    not_thrown = []
                    for suit in cards.SUITS:
                        not_thrown.append(suit + card_value)
                    for card in thrower_cards:
                        if card.get_value() == card_value:
                            not_thrown.pop(not_thrown.index(card.get_card_str()))
                    for card in not_thrown:
                        self._probs.mul(thrower, card, 0.9)
    def extract_retransfer_info(self):
        '''If F1-F2 or F2-F2 then extracts info about
        retransferd cards. Otherwise does nothing.
        '''
        if not self.same_turn():
            return
        if self.prev_state != F2 or self.new_state != F2:
            return
        new_defender = self.new_status.get_defender().get_order()
        old_defender = self.prev_status.get_defender().get_order()
        names = []
        for card in self.new_status.get_table().convert_to_cards():
            if not card.get_owner() in names:
                names.append(card.get_owner())
        if new_defender == old_defender and len(names) == 1:
            return
        #retrasnfer, know for sure
        added = self.get_thrown_on_cards()
        card_value = added[0].get_value()
        names = []
        for card in added:
            if not card.get_owner() in names:
                names.append(card.get_owner())
        for name in names:
            retransferer_cards = []
            for card in added:
                if card.get_owner() == name:
                    retransferer_cards.append(card)
            not_retransfered = []
            for suit in cards.SUITS:
                not_retransfered.append(suit + card_value)
            for card in retransferer_cards:
                if card.get_card_str() in not_retransfered:
                    not_retransfered.pop(not_retransfered.index(card.get_card_str()))
            for card in not_retransfered:
                self._probs.mul(name, card, 0.9)
    def extract_attacked_info(self):
        '''If F1-F2 then extracts info about attacker's cards.
        '''
        attacker = self.new_status.get_attacker().get_name()
        me = self.new_status.get_my_info().get_name()
        if attacker == me:
            return
        if not self.same_turn():
            return
        if not ((self.prev_state == F1) and (self.new_state == F2)):
            return
        attack = self.new_status.get_table().convert_to_cards()
        missed = []
        card_value = attack[0].get_value()
        card_suit = attack[0].get_suit()
        trump_suit = self.new_status.get_trump_card().get_suit()
        for suit in cards.SUITS:
            missed.append(suit + card_value)
        for card in attack:
            if card.get_card_str() in missed:
                missed.pop(missed.index(card.get_card_str()))
        if len(attack) == 1:
            if card_suit != trump_suit:
                for i in range(0, cards.VALUES.index(card_value)):
                    for suit in cards.SUITS:
                        if suit != trump_suit:
                            add = suit + cards.VALUES[i]
                            if not add in missed:
                                missed.append(suit + cards.VALUES[i])
            else:
                for value in cards.VALUES:
                    for suit in cards.SUITS:
                        if suit != trump_suit:
                            add = suit + value
                            if not add in missed:
                                missed.append(add)
                for i in range(0, cards.VALUES.index(card_value)):
                    add = card_suit + cards.VALUES[i]
                    missed.append(add)
        if len(attack) == 1:
            coef = 0.9
        else:
            coef = 0.8
        for card in missed:
            self._probs.mul(self.new_status.get_attacker().get_name(), card, coef)
    def extract_covering_info(self):
        '''Extracts info about how player covers cards.
        If it is possible, remembers what cards he took.
        '''
        defender = self.prev_status.get_defender().get_name()
        if self.same_turn():
            #take new pairs
            left = self.prev_status.get_table().get_covering_cards()
            right = self.new_status.get_table().get_covering_cards()
            right_covered = self.new_status.get_table().get_covered_cards()
            miss = len(left)
            length = len(right) - miss
            pairs = []
            for i in range(miss, miss + length):
                pairs.append([right_covered[i], right[i]])
            trump_suit = self.prev_status.get_trump_card().get_suit()
            #get data
            for pair in pairs:
                b = pair[0]
                t = pair[1]
                not_used = []
                if (t.get_suit() == trump_suit) and (b.get_suit() != trump_suit):
                    for i in range(cards.VALUES.index(b.get_value()) + 1, len(cards.VALUES)):
                        not_used.append(b.get_suit() + cards.VALUES[i])
                    for i in range(0, cards.VALUES.index(t.get_value())):
                        not_used.append(trump_suit + cards.VALUES[i])
                else:
                    for i in range(cards.VALUES.index(b.get_value()) + 1,
                                   cards.VALUES.index(t.get_value())):
                        not_used.append(b.get_suit() + cards.VALUES[i])
                for used in right:
                    if used.get_card_str() in not_used:
                        not_used.pop(not_used.index(used.get_card_str()))
                for card in not_used:
                    self._probs.mul(defender, card, 0.7)
        elif not self.cards_sent_to_out() and self.new_table_empty():
            if not self.retransfer_allowed() or (self.prev_state in [M1, M2]):
                took_cards = self.prev_status.get_table().convert_to_cards()
                for card in took_cards:
                    self._probs.set_owner(card.get_card_str(), defender)
            else:
                #may be handle this situation in another way
                took_cards = self.prev_status.get_table().convert_to_cards()
                for card in took_cards:
                    self._probs.set_owner(card.get_card_str(), defender)

    #Generating strategies
    def generate_strategy(self):
        '''Generate strategies and try them.
        '''
        if self.new_status.get_my_info().is_playing():
            if self.is_active():
                self.prepare_strategies()
                self.try_and_forget()
                while (self.action_failed()):
                    self.try_and_forget()
    def prepare_strategies(self):
        '''Generate proper strategies.
        '''
        
        me = self.new_status.get_my_info()
        if me.is_attacker():
            if self.new_state == F1:
                self.generate_attack()
            else:
                self.generate_throw_on()
        elif me.is_defender():
            self.generate_defence()
    def try_and_forget(self):
        '''Use generated strategies.
        '''
        cmd = self.queued_commands.pop(0)
        result = self._parser.parse_response(self.requestor.make_request(cmd))
        if result.get_status():
            self.last_action_failed = False
            self.clear_queue()
        else:
            self.last_action_failed = True
    def generate_attack(self, twice=False):
        '''Generate all possible attack combinations,
        sort them.
        '''
        #exceptional situation
        my_cards = self.new_status.get_my_info().get_cards()
        if int(self.new_status.get_cards_in_deck()) == 0:
            value = my_cards[0].get_value()
            all_eq_value = True
            for card in my_cards:
                if card.get_value() != value:
                    all_eq_value = False
                    break
            if all_eq_value:
                self.queue_attack_cards(my_cards)
        defender = self.new_status.get_defender().get_name()
        #make a set of possible attacking cards
        restrict = 36
        if self.attack6_restrict():
            restrict = 6
        if self.first_attack5_restrict() and self.is_first_turn():
            restrict = 5
        restrict = min(self.new_status.get_defender().get_number_of_cards(), restrict)
        new_cards = []
        if not self.last_attack_quarter_game() and not twice:
            for card in my_cards:
                if card.get_suit() != self.get_trump_suit():
                    new_cards.append(card)
            my_cards = new_cards
        attacks = self.generate_attack_set(my_cards, restrict)
        #calculate each attack set's average value
        #calculate probabilities of attack's success based on questions:
        #1)will cover? 2)will throw on? 3)can retransfer?
        prob_attacks = []
        for attack in attacks:
            #value:
            value = 0.0
            for card in attack:
                value = value + cards.VALUES.index(card.get_value())
                if card.get_suit() == self.get_trump_suit():
                    value = value + 9.0
            value = value / len(attack)
            #retransfer probability:
            retransfers = 0.0
            if self.retransfer_allowed():
                retransfers = self.calc_retransfer_probability(attack, defender)
            #cover probability:
            covers = self.calc_cover_probability(attack, defender)
            #throw_on possibility:
            throw_on = self.calc_throw_on_probability(attack, defender)
            #remember data
            prob_attacks.append([attack, value, retransfers, covers, throw_on])
        #sorting by value and dividing into groups
        sort1 = lambda x, y: long(x[1]*1000).__cmp__(long(y[1]*1000))
        mix = lambda r, c, t: 3*(1 - r) + t + 4*(1 - c)
        sort2 = lambda x, y: long(mix(y[2], y[3], y[4])*1000).__cmp__(long(mix(x[2], x[3], x[4])*1000))
        prob_attacks.sort(sort1)
        if not self.empty_deck():
            if not self.last_attack_quarter_game():
                a = len(prob_attacks)/3
                b = 2*len(prob_attacks)/3
                prob_attacks[0:a].sort(sort2)
                prob_attacks[a:b].sort(sort2)
                prob_attacks[b:len(prob_attacks)].sort(sort2)
            else:
                a = len(prob_attacks)/2
                prob_attacks[0:a].sort(sort2)
                prob_attacks[a:len(prob_attacks)].sort(sort2)
        else:
            prob_attacks.sort(sort2)    
        if len(prob_attacks) == 0:
            self.generate_attack(True)
        #queue cards in a proper order
        self.queue_attack_cards([prob_attack[0] for prob_attack in prob_attacks])
        #self.queue_quit()
    def generate_throw_on(self):
        '''Generate all possible throw on combinations,
        sort them.
        '''
        table_values = []
        table_in_cards = self.new_status.get_table().convert_to_cards()
        for card in table_in_cards:
            if not card.get_value() in table_values:
                table_values.append(card.get_value())
        mycards = self.new_status.get_my_info().get_cards()
        #exceptional situation: if can and should retransfer all
        if self.new_status.get_cards_in_deck() == 0:
            can_throw_all = True
            for card in mycards:
                if not card.get_value() in table_values:
                    can_throw_all = False
                    break
                if can_throw_all:
                    self.queue_throw_on_cards(mycards)
        defender = self.new_status.get_defender().get_name()
        #how many cards may i throw on?
        restrict = 36
        if self.attack6_restrict():
            restrict = 6
        if self.first_attack5_restrict() and self.is_first_turn():
            restrict = 5
        attacked_number = len(self.new_status.get_table().get_bottom_cards())
        restrict = min(self.new_status.get_defender().get_number_of_cards(),
                       restrict - attacked_number)
        #what cards can i throw on?
        can_throw = []
        for card in mycards:
            if card.get_value() in table_values:
                can_throw.append(card)
        new_cards = []
        if not self.last_attack_quarter_game():
            for card in can_throw:
                if card.get_suit() != self.get_trump_suit():
                    new_cards.append(card)
            can_throw = new_cards
        attacks = self.generate_throw_on_set(can_throw, restrict)
        #calculate each attack set's average value
        #calculate probabilities of attack's success based on questions:
        #1)will cover? 2)will throw on? 3)can retransfer?
        for i in range(len(attacks)):
            attack = attacks[i]
            #value:
            value = float(0)
            for card in attack:
                value = value + cards.VALUES.index(card.get_value())
                if card.get_suit() == self.get_trump_suit():
                    value = value + 9
            value = value / len(attack)
            #cover probability:
            covers = self.calc_cover_probability(attack, defender)
            #throw_on possibility:
            throw_on = self.calc_throw_on_probability(attack, defender)
            #remember data
            attacks[i] = [attack, value, covers, throw_on]
        #sorting by value and dividing into groups
        sort1 = lambda x, y: long(x[1]*1000).__cmp__(long(y[1]*1000))
        mix = lambda c, t: 3*(1 - c) + t
        sort2 = lambda x, y: long(mix(y[2], y[3])*1000).__cmp__(long(mix(x[2], x[3])*1000))
        attacks.sort(sort1)
        if not self.empty_deck():
            if not self.last_attack_quarter_game():
                a = len(attacks)/3
                b = 2*len(attacks)/3
                attacks[0:a].sort(sort2)
                attacks[a:b].sort(sort2)
                attacks[b:len(attacks)].sort(sort2)
            else:
                a = len(attacks)/2
                attacks[0:a].sort(sort2)
                attacks[a:len(attacks)].sort(sort2)
        else:
            attacks.sort(sort2)
        #queue cards in a proper order
        self.queue_throw_on_cards([attack[0] for attack in attacks])
        self.queue_skip()
    def generate_defence(self):
        '''Tries to generate defence combinations.
        '''
        new_table = self.new_status.get_table() 
        to_cover = new_table.get_uncovered_cards()
        all_bottom = new_table.get_bottom_cards()
        my_cards = self.new_status.get_my_info().get_cards()
        trump_suit = self.new_status.get_trump_card().get_suit()
        #trying to retransfer
        if self.retransfer_allowed() and self.first_attack_in_turn():
            value = new_table.convert_to_cards()[0].get_value()
            retransfer_set = cards.Cards()
            for card in my_cards:
                if card.get_value() == value:
                    retransfer_set.append(card)
            #1) if can and if should retransfer all:
            if len(retransfer_set) == len(my_cards):
                #also if has no trumps
                if int(self.new_status.get_cards_in_deck()) == 0:
                    self.queue_retransfer_cards(retransfer_set)
            #2)end game condition or full age check :_
            if not self.half_game_passed():
                if self.calc_average_value(all_bottom) > 11:
                    self.queue_take()
            #3) simple retransfer
            if len(retransfer_set) != 0:
                #exclude trump cards from retransfering cards
                if len(retransfer_set) != 1:
                    for card in retransfer_set:
                        if (card.get_suit() == trump_suit) and not self.last_cover_quarter_game():
                            retransfer_set.pop(retransfer_set.index(card))
                            break
                    self.queue_retransfer_cards(retransfer_set)
                else:
                    if (retransfer_set[0].get_suit() != trump_suit) or self.last_cover_quarter_game():
                        self.queue_retransfer_cards(retransfer_set)
                #retransfer with all left cards
                #use = []
                #for set in retransfer_set:
                #    if len(set) > len(use):
                #        use = set
                
        #now trying to cover
        new_cards = []
        if not self.last_cover_quarter_game():
            for card in my_cards:
                if card.get_suit() != self.get_trump_suit():
                    new_cards.append(card)
            my_cards = new_cards
        covering_sets = self.generate_covering_sets(to_cover, my_cards)
        for i in range(len(covering_sets)):
            cover_set = covering_sets[i]
            #value:
            value = float(0)
            for card in cover_set.get_covering_cards():
                value = value + cards.VALUES.index(card.get_value())
                if card.get_suit() == self.get_trump_suit():
                    value = value + 9
            value = value / len(cover_set)
            #throw_on probability:
            throw_on = self.calc_throw_on_probability(cover_set.get_covering_cards(),
                                                      self.new_status.get_my_info().get_name())
            #remember data
            covering_sets[i] = [cover_set, value, throw_on]
        #sorting by value and dividing into groups
        sort1 = lambda x, y: long(x[1]*1000).__cmp__(long(y[1]*1000))
        mix = lambda c, t: 3*(1 - c) + t
        sort2 = lambda x, y: long(y[2]*1000).__cmp__(long(x[2]*1000))
        covering_sets.sort(sort1)
        a = len(covering_sets) / 3
        b = 2*len(covering_sets) / 3
        covering_sets[0:a].sort(sort2)
        covering_sets[a:b].sort(sort2)
        covering_sets[b:len(covering_sets)].sort(sort2)
        #queue cards in a proper order
        self.queue_cover_cards([cover_set[0] for cover_set in covering_sets])
        self.queue_take()
        #self.queue_quit()
    def calc_retransfer_probability(self, attack, defender):
        '''Calculates the probability the 'defender' will
        retransfer 'attack' cards.
        '''
        possib = 0.0
        values = []
        for card in attack:
            if not card.get_value() in values:
                values.append(card.get_value())
        for value in values:
            for suit in cards.SUITS:
                possib = possib + self._probs[defender][suit + value]
        if possib >= 1:
            return 1
        else:
            return possib
    def calc_cover_probability(self, attack, defender):
        '''Calculates maximum probability of covering for attack cards.
        '''
        pairs = self.calc_all_cover_probability(attack, defender)
        max = [[], 0]
        for pair in pairs:
            if pair[1] > max[1]:
                max = pair
        return max[1]
    def calc_all_cover_probability(self, attack, defender):
        '''Is used by calc_cover_probability funciton.
        Generates all possible sets to cover 'attack' cards
        and calculates probability of being used by your enemy
        for each of those sets.
        '''
        if len(attack) != 0:
            head = attack[0]
            right = self.calc_all_cover_probability(attack[1:len(attack)], defender)
            new_seq = []
            to_check = []
            trump_suit = self.new_status.get_trump_card().get_suit()
            for i in range(cards.VALUES.index(head.get_value()) + 1, len(cards.VALUES)):
                to_check.append(head.get_suit() + cards.VALUES[i])
            if head.get_suit() != trump_suit:
                for value in cards.VALUES:
                    to_check.append(trump_suit + value)
            for variant in right:
                for card in to_check:
                    if not card in variant[0]:
                        entry = [[], 1]
                        entry[0].extend(variant[0])
                        new_seq.append(entry)
                        entry[0].append(card)
                        entry[1] = entry[1] * self._probs[defender][card]
            return new_seq
        else:
            return [[[], 1]]
    def calc_throw_on_probability(self, attack, defender):
        '''Calculates probability of throwing on.
        Possible to change this function: make it return 'possib'
        even if it is greater than 1. The greater the values is
        the greater the possible number of throwing on cards becomes.
        '''
        possib = 0.0
        values = []
        for card in attack:
            if not card.get_value() in values:
                values.append(card.get_value())
        for player in self._probs.keys():
            if player in [OUT, TABLE, DECK, defender]:
                continue
            for value in values:
                for suit in cards.SUITS:
                    possib = possib + self._probs[player][suit + value]
        #May change here:
        if possib >= 1:
            return 1
        else:
            return possib
    def generate_attack_set(self, cards_set, length):
        '''Takes list of cards.Card object and length of attack list.
        Generate all possible attack lists.
        '''
        V = cards.VALUES
        S = cards.SUITS
        def sort_func(x, y):
            if S.index(x.get_suit()) > S.index(y.get_suit()):
                return 1
            elif V.index(x.get_value()) > V.index(y.get_value()):
                return 1
            else:
                return -1
                    
        set = []
        set.extend([[card] for card in cards_set])
        while length > 1:
            plus_set = []
            for attack in set:
                for add in cards_set:
                    if (add.get_value() == attack[0].get_value()) and not (add in attack):
                        new = []
                        new.extend(attack)
                        new.append(add)
                        new.sort(sort_func)
                        if not (new in plus_set or new in set):
                            plus_set.append(new)
            set.extend(plus_set)
            length = length - 1
        return set
    def generate_throw_on_set(self, cards_set, length):
        '''Takes list of cards.Card object and length of attack list.
        Generate all possible throw_on lists.
        '''
        V = cards.VALUES
        S = cards.SUITS
        def sort_func(x, y):
            if S.index(x.get_suit()) > S.index(y.get_suit()):
                return 1
            elif V.index(x.get_value()) > V.index(y.get_value()):
                return 1
            else:
                return -1
                    
        set = []
        set.extend([[card] for card in cards_set])
        while length > 1:
            plus_set = []
            for attack in set:
                for add in cards_set:
                    if not add in attack:
                        new = []
                        new.extend(attack)
                        new.append(add)
                        new.sort(sort_func)
                        if not (new in plus_set or new in set):
                            plus_set.append(new)
            set.extend(plus_set)
            length = length - 1
        return set
    def generate_covering_sets(self, to_cover, use_cards):
        '''Takes list of cards.Card objects to cover and list of cards.Card
        objects to use. Returns all possible cover sets. Returns [] if it's not
        posible to cover.
        '''
        if len(to_cover) != 0:
            first = to_cover.pop(0)
            right = self.generate_covering_sets(to_cover, use_cards)
            extension = []
            for set in right:
                used = set.get_covering_cards()
                for card in use_cards:
                    if self.is_coverable(first, card) and not card in used:
                        new_table = table.Table()
                        new_table.extend(set)
                        new_table.put_on_card(first)
                        new_table.cover_card(first, card)
                        equals_set = False
                        new_coverings = new_table.get_covering_cards()
                        coverings = []
                        if not equals_set:
                            extension.append(new_table)
            return extension
        else:
            return [table.Table()]