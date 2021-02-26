#!/usr/bin/env python
# coding: utf-8

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self,suits,ranks):
        self.suits = suits
        self.ranks = ranks
    
    def __str__(self):
        return self.ranks + ' of ' + self.suits

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                newcard = Card(suit,rank)
                self.deck.append(newcard)
    
    def __str__(self):
        return f'{len(self.deck)}'

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop(0)

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.ranks]
        if card.ranks == 'Ace':
            self.aces += 1
            
    def adjust_for_ace(self):
        if self.aces > 0:
            self.value -= 10

class Chips:
    
    def __init__(self):
        self.total = 1000  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(funds):
    
    while True:
        bet = int(input('Please place your bet: '))
        if bet <= funds:
            return bet
            print("Your bet has been accepted.")
            break
        else:
            print("You do not have enouth chips to bet!")    


def hit(deck,hand):
    
    hand.add_card(deck.deal())
    
    if hand.value > 21:
        hand.adjust_for_ace()


def hit_or_stand(deck,hand):
    global playing # to control an upcoming while loop
    
    answer = ""
    playing = True
    
    while answer not in ["H","S"] or answer == 'H':
        answer = input('Hit or Stand? H or S: ').upper()
        if answer == "H":
            hit(deck,hand)
            print(hand.cards[-1])
            
        elif answer == "S":
            playing = False
            break
        else:
            print('Sorry, you need to choose H or S.')


def show_some(player,dealer):
    
    print('\nPlayer cards: \n')
    for card in player.cards:
        print(f'{card}')
        
    print(f'Total Player value: {player.value}\n')
    
    print('Dealer cards: \n')
    print(f'***Hidden***')
    for card in dealer.cards[1:]:
        print(f'{card}')
        
    hidden_card = dealer.cards[0]
    dealer_value = dealer.value - values[hidden_card.ranks]
    
    print(f'Total Dealer value: {dealer_value}')
    
def show_all(player,dealer):
    
    print('\nPlayer cards: \n')
    for card in player.cards:
        print(f'{card}')
        
    print(f'Total Player value: {player.value}\n')
    
    print('Dealer cards: \n')
    for card in dealer.cards:
        print(f'{card}')
        
    print(f'Total Dealer value: {dealer.value}\n')
    
    pass


def player_busts(player_hand,dealer_hand,chips):
    print("Player BUST!")
    chips.lose_bet()

def player_wins(player_hand,dealer_hand,chips):
    print("Player Wins!")
    chips.win_bet()

def dealer_busts(player_hand,dealer_hand,chips):
    print("Dealer BUST!")
    chips.win_bet()
    
def dealer_wins(player_hand,dealer_hand,chips):
    print("Dealer Wins!")
    chips.lose_bet()
    
def push():
    print('Draw')
    pass


# ### And now on to the game!!


while True:
    print('Welcome to Blackjack Game \n')

    newdeck = Deck()
    newdeck.shuffle()
    
    dealer_hand = Hand()
    player_hand = Hand()
    
    hit(newdeck,dealer_hand)
    hit(newdeck,player_hand)
    hit(newdeck,dealer_hand)
    hit(newdeck,player_hand)

    # Set up the Player's chips
    player_chips = Chips()
    player_chips.total = int(input('Player deposit your chips: '))
    
    # Prompt the Player for their bet
    player_chips.bet = take_bet(player_chips.total)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    playing = True
    
    while playing == True:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(newdeck,player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        else:
            while dealer_hand.value < 17:
                hit(newdeck,dealer_hand)
        
    
        # Show all cards
        show_all(player_hand,dealer_hand)
    
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif player_hand.value > dealer_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        elif player_hand.value < dealer_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        else:
            push()
    
    # Inform Player of their chips total 
    print(f'Player your current chips are: {player_chips.total}\n')
    # Ask to play again
    if input('Do you want to play again?"("Y/N")" ').upper() == 'Y':
        True
    else:
        break
