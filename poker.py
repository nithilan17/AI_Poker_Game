from collections import Counter
import random

class Card:
    '''Card Class - suit, rank'''
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def get_suit(self):
        return self.suit
    
    def get_rank(self):
        return self.rank
    
    def card_to_str(self):
        return (self.get_rank() + self.get_suit())

class Deck:
    '''Deck Class - list of cards'''
    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        '''Creates a list of 52 strings representing each card in a deck'''
        suits = ['♥', '♦', '♣', '♠']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        '''Shuffles the created list of 52 cards'''
        random.shuffle(self.cards)

    def deal(self, num_cards):
        '''Remove the first shuffled card in the list and return it'''
        if len(self.cards) < num_cards: # If not enough cards
            return None
        dealt_cards = []
        for i in range(num_cards):
            dealt_cards.append(self.cards.pop())
        return dealt_cards

class PokerGame:
    '''PokerGame Class - contains methods involved in poker game functionality'''
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

    def burn_card(self):
        '''Burns the top card in the deck'''
        self.deck.cards.pop()

    def pre_flop_message(self, card1, card2): 
        rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        if(card1.suit == card2.suit):
            return "Look out for the flush draw! We got matching suits!"
        if(card1.rank == card2.rank):
            if(card1.rank == 'A'):
                return "Pocket Rockets! This is the best hand in poker!"
            return "Woohoo! We got a pair!"
        
        if ('7' in {card1.rank, card2.rank}) and ('2' in {card1.rank, card2.rank}):  # If either card is 7 and the other is 2 (or vice versa)
            return "This is a 7-2 off suit, the worst hand in poker"
    
        total_value = rank_values[card1.rank] + rank_values[card2.rank]

        if total_value >= 20:
            return "This is a very good starting hand! We should definately raise or reraise on this!"
        
        if total_value > 14:
            return "This is a good starting hand! We can play aggressively or call here!"
        
        if total_value > 9:
            return "This hand is decent. Consider playing conservative here."
        else:
            return "This hand is weak. We should probably fold or bluff here."
        
    def deal_hand(self, num_players):
        '''Deals 2 cards to number of players, specified by parameter num_players '''
        hands = []
        for i in range(num_players):
            hand = self.deck.deal(2)
            if hand is None:
                return None
            hands.append(hand)
        return hands
    
    def get_deck(self):
        '''Getter method for the deck'''
        return self.deck

    def evaluate_hand_str(self, hand,community_cards):
        hand_value = self.evaluate_hand(hand,community_cards)

        if hand_value == 100:
            return "Royal Flush"
        elif hand_value >= 90:
            return "Straight Flush"
        elif hand_value >= 80:
            return "Quads"
        elif hand_value >= 70:
            return "Full House"
        elif hand_value >= 60:
            return "Flush"
        elif hand_value >= 50:
            return "Straight"
        elif hand_value >= 40:
            return "Trips"
        elif hand_value >= 30:
            return "Two Pair"
        elif hand_value >= 20:
            return "Pair"
        else:
            return "High Card"

    def deal_community_card(self):
        '''Deal the 5 community cards as a list of 5 Cards'''
        community = []
        self.burn_card() # pre flop burn
        for i in range(3):
            nextcard = self.deck.deal(1)[0]
            community.append(nextcard)
        self.burn_card() # pre turn burn
        for i in range(1):
            nextcard = self.deck.deal(1)[0]
            community.append(nextcard)
        self.burn_card() # pre river burn
        for i in range(1):
            nextcard = self.deck.deal(1)[0]
            community.append(nextcard)
        return community

    def get_flop(self, community_cards):
        '''After calling deal_community_card, returns the first 3 of the community cards'''
        return community_cards[:3]
    
    def get_turn(self, community_cards):
        '''After calling deal_community_card, returns the 4th community card'''
        return community_cards[3]
    
    def get_river(self, community_cards):
        '''After calling deal_community_card, returns the 5th community card'''
        return community_cards[4]
    
    def evaluate_hand(self, hand, community_cards):
        '''This method evaluates a hand and assigns it to a numerical value. Note: the straight logic and decimal additions of tiebreakers were written by ChatGPT.'''
        all_cards = hand + community_cards
        suits = [card.suit for card in all_cards]
        ranks = [card.rank for card in all_cards]

        rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)

        flush = any(count >= 5 for count in suit_counts.values())

        # Check for straight
        straight = False
        straight_high = None
        straight_ranks = sorted(set(rank_values[card.rank] for card in all_cards))
        if len(straight_ranks) >= 5:

            if set(straight_ranks) == {2, 3, 4, 5, 14}:  # Ace low straight
                straight = True
                straight_high = 5

            for i in range(len(straight_ranks) - 4):
                if straight_ranks[i + 4] - straight_ranks[i] == 4:
                    straight = True
                    straight_high = straight_ranks[i + 4]
                    break
        sorted_ranks = sorted(set(rank_values[card.rank] for card in all_cards))

        if flush and straight:
            if straight_high == 14: 
                return 100  # Royal Flush
            return 90  # Straight Flush
        
        elif 4 in rank_counts.values():
            quad_rank = rank_values[rank_counts.most_common(1)[0][0]]
            return 80 + quad_rank * 0.1  # Quads (Four of a Kind)
        
        elif (len(rank_counts) == 4 or len(rank_counts) == 3) and 3 in rank_counts.values() and 2 in rank_counts.values():
            trip_rank = rank_values[rank_counts.most_common(1)[0][0]]
            pair_rank = rank_values[rank_counts.most_common(2)[1][0]]
            return 70 + trip_rank*0.1 + pair_rank*0.001  # Full House
        
        elif flush:
            common_suits = [suit for suit, count in suit_counts.items() if count >= 5]
            common_cards = [card for card in all_cards if card.suit in common_suits]
            flush_cards = [rank_values[card.rank] for card in common_cards]
            flush_cards.sort(reverse=True)
            flush_val = 0
            for i in range(0,5):
                flush_val += 0.01**((i+1))*flush_cards[i]
            return 60 + flush_val # Flush
        
        elif straight: # account for ties
            return 50 + straight_high * 0.1  # Straight
        
        elif 3 in rank_counts.values():  
            trips_rank = rank_values[rank_counts.most_common(1)[0][0]]
            kicker_ranks = [rank_values[rank] for rank, count in rank_counts.items() if count != 3]
            kicker_ranks.sort(reverse=True)
            kicker = 0
            for i in range(0,2):
                kicker += 0.01**(2*(i+1))*kicker_ranks[i]
            return 40 + trips_rank*0.1 + kicker # Trips (Three of a Kind)
        
        elif len(rank_counts) != 6 and 2 in rank_counts.values():
            pair_ranks = sorted(rank_values[rank] for rank, count in rank_counts.items() if count == 2)
            kicker_ranks = [rank_values[rank] for rank, count in rank_counts.items() if count == 1]
            kicker_ranks.sort(reverse=True)
            kicker = 0.000001*kicker_ranks[0]
            return 30 + pair_ranks[1] * 0.1 + pair_ranks[0] * 0.0001 + kicker # Two Pair
        
        elif len(rank_counts) == 6: # work on kicker 
            pair_rank = rank_values[rank_counts.most_common(1)[0][0]]
            kicker_ranks = [rank_values[rank] for rank, count in rank_counts.items() if count == 1]
            kicker_ranks.sort(reverse=True)
            kicker = 0
            for i in range(0,3):
                kicker += 0.01**(2*(i+1))*kicker_ranks[i]
            return 20 + pair_rank*0.01 + kicker  # One Pair
        
        else:
            sorted_ranks.sort(reverse=True)
            kicker = 0
            for i in range(0,5):
                kicker += 0.1**(2*(i+1))*sorted_ranks[i]
            return 10 + kicker  # High Card
