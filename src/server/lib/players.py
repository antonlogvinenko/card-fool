import cards


class Player:
    '''Player oject. Keeps only player's name.
    '''
    def __init__(self, name = ''):
        self._name = name
    def get_name(self):
        '''Returns players name.
        '''
        return self._name


class Player_In_Game(Player):
    '''Presents data containing inside the game object.
    '''
    def __init__(self, registered_player, order):
        '''Uses registered_player of Registered_Player class and
        player's order in the game for initialization.
        '''
        self._cards = cards.Cards()
        self._status = ''
        self._order = order
        self._active = False
        self._reg_entry = registered_player
    def get_name(self):
        '''Returns player's name
        '''
        return self._reg_entry.get_name()
    def get_order(self):
        '''Returns player's order in the game.
        '''
        return self._order
    def get_cards(self):
        '''Returns player's cards.
        '''
        return self._cards
    def get_cards_str(self):
        '''Returns string representation of player's cards.
        '''
        if self.get_number_of_cards() != 0:
            return ''.join([
                            '[' + str(card) + ']' for card in self._cards
                            ])
        else:
            return ''
    def get_number_of_cards(self):
        '''Returns number of player's cards.
        '''
        return len(self._cards)
    def get_number_of_cards_str(self):
        '''Returns '[x]' where x is number of player's cards.
        '''
        return '[' + str(self.get_number_of_cards()) + ']'
    def get_status(self):
        '''Returns player's status.
        '''
        return self._status
    def make_attacker(self):
        '''Makes player an atacker - assigns status.
        '''
        self._status = '_attacker_'
    def make_defender(self):
        '''Makes player a defender - assigns status.
        '''
        self._status = '_defender_'
    def clear_status(self):
        '''Clears player's status.
        '''
        if not self.finished_playing():
            self._status = ''
    def finished_playing(self):
        '''Returns True if player has finished playing
        (is winner or fool). Otherwise returns True.
        '''
        return self.get_status() in ['_winner_', '_fool_']
    def is_attacker_or_defender(self):
        '''Returns True if player is attacker or defender.
        Returns False otherwise.
        '''
        return self.is_defender() or self.is_attacker()
    def is_defender(self):
        '''Returns True if players is defender.
        Returns False otherwise.
        '''
        return self.get_status() == '_defender_'
    def is_attacker(self):
        '''Returns True if player is attacker.
        Returns False otherwise.
        '''
        return self.get_status() == '_attacker_'
    def is_winner(self):
        '''Returns True if player is winner, False otherwise.
        '''
        return self.get_status() == '_winner_'
    def is_fool(self):
        '''Returns True if player is a fool, False otherwise.
        '''
        return self.get_status() == '_fool_'
    def _stops_playing(self):
        '''Sets the 'playing_game' field in this player's
        registration object empty.
        '''
        self._reg_entry.stops_playing()
    def make_fool(self):
        '''Makes player a fool.
        '''
        self._status = '_fool_'
    def make_winner(self):
        '''Makes player a winner.
        '''
        self._status = '_winner_'
    def has_card(self, card):
        '''Returs True if player has the card.
        Returns False otherwise.
        '''
        return self._cards.has_card(card)
    def has_cards(self, cards_check):
        '''Returns True if player has cards_check.
        Returns False otherwise.
        '''
        for card in cards_check:
            if not self._cards.has_card(card):
                return False
        return True
    def give_card(self, card):
        '''Adds a card to the player's cards.
        '''
        self._cards.add_card(card)
    def give_cards(self, to_give):
        '''Adds to_give cards to the player's cards.
        '''
        self._cards.add_cards(to_give)
    def take_away_card(self, card):
        '''Removes card from player's cards.
        '''
        self._cards.extract_card(card)
    def take_away_cards(self, to_take):
        '''Removes cards from player's cards.
        '''
        self._cards.extract_cards(to_take)


class Registered_Player(Player):
    '''For storing data about registered player.
    '''
    def __init__(self, name = '', playing_game = ''):
        Player.__init__(self, name)
        self._playing_game = playing_game
    def is_playing_now(self):
        '''Returns True if this player is in game now.
        '''
        return self._playing_game != ''
    def get_playing_game(self):
        '''Returns the name of playing game.
        Return '' if player is not in game.
        '''
        return self._playing_game
    def starts_playing(self, game_name):
        '''Sets the name of the game player
        starts playing.
        '''
        self._playing_game = game_name
    def stops_playing(self):
        '''Removes player's previous played game.
        '''
        self._playing_game = ''


class Registered_Players(dict):
    '''Stores registered players, uids are keys,
    instances of Registered_Player are values.
    '''
    def name_exists(self, name):
        '''Returns True if a player with such a name exists.
        Returns False otherwise.
        '''
        for x in self.values():
            if x.get_name() == name:
                return True
        return False
    def new_player(self, uid, name):
        '''Adds a new player to the hash.
        '''
        self[uid] = Registered_Player(name)


class Players_In_Game(dict):
    '''Stores info about players partisipating
    in the game.
    '''
    def __init__(self):
        self._active = 1
    def new_player(self, uid, registered_player):
        '''Adds a new player. Uses an existing
        registration entry.
        '''
        self[uid] = Player_In_Game(registered_player,
                                   self.get_number_of_players() + 1)
    def get_players_in_game(self):
        '''Returns objects representing all players in this game.
        '''
        return self.values()
    def get_number_of_players(self):
        '''Returns number of players.
        '''
        return len(self)
    def get_player_uid(self, some_player):
        for uid in self.keys():
            if self[uid] == some_player:
                return uid
    def is_next_to(self, a, b):
        '''Returns True if player a is next to player b.
        Returns False otherwise.
        '''
        return a.get_order() % self.get_number_of_players() + 1 == b.get_order()
    def get_defender_for_retransfer(self):
        '''Returns a player that will become defender in this retransfer attack.
        '''
        possible_new_defenders = []
        cur_defender_order = self.get_defender().get_order()
        for player in self.values():
            if not (player.is_defender() or player.finished_playing()):
                possible_new_defenders.append(player)
        after = None
        before = None
        for player in possible_new_defenders:
            if (player.get_order() < cur_defender_order):
                if (before == None) or (player.get_order() < before.get_order()):
                    before = player
            elif (after == None) or (after.get_order() > player.get_order()):
                after = player
        if after != None:
            return after
        return before
    def get_defender(self):
        '''Returns current defender.
        '''
        for player in self.values():
            if player.is_defender():
                return player
    def get_attacker(self):
        '''Returns current attacker.
        '''
        for player in self.values():
            if player.is_attacker():
                return player
    def get_by_order(self, order):
        for player in self.values():
            if player.get_order() == order:
                return player
    def make_defender(self, order):
        '''Finds a player with the specified order
        and makes him to defend.
        '''
        for player in self.values():
            if player.get_order() == order:
                player.make_defender()
            elif player.is_defender():
                    player.clear_status()
    def make_attacker(self, order):
        '''Finds a player with the specified order
        and makes him to attack.
        '''
        for player in self.values():
            if player.get_order() == order:
                player.make_attacker()
            elif player.is_attacker():
                    player.clear_status()
    def norm_order(self, order):
        '''Maps a number 'order' to a [1 .. number_of_players] set.
        '''
        remainder = order % self.get_number_of_players()
        if remainder == 0:
            return self.get_number_of_players()
        return remainder
    def make_attacker_after(self, order):
        '''Makes the player after player with order 'order' to attack.
        '''
        prev_attacker = self.get_attacker()
        if prev_attacker != None:
            prev_attacker.clear_status()
        possible_attackers = []
        for player in self.values():
            if not (player.is_defender() or player.finished_playing()):
                possible_attackers.append(player)
        set = False
        while not set:
            for player in possible_attackers:
                if player.get_order() == self.norm_order(order + 1):
                    player.make_attacker()
                    set = True
            order = order + 1
    def make_defender_after(self, order):
        '''Makes the player after player with order 'order' to defend.
        '''
        prev_defender = self.get_defender()
        if prev_defender != None:
            prev_defender.clear_status()
        possible_defenders = []
        for player in self.values():
            if not (player.is_attacker() or player.finished_playing()):
                possible_defenders.append(player)
        set = False
        while not set:
            for player in possible_defenders:
                if player.get_order() == self.norm_order(order + 1):
                    player.make_defender()
                    set = True
            order = order + 1
    def set_active_player(self, n):
        '''Makes a player with order n an active player.
        '''
        self._active = n
    def make_defender_active(self):
        '''Makes current defender active.
        '''
        self.set_active_player(self.get_defender().get_order())
    def make_attacker_active(self):
        '''Makes current attacker active.
        '''
        self.set_active_player(self.get_attacker())
    def get_active_player(self):
        '''Returns the order of active player.
        '''
        return self._active