#!/usr/bin/env python
# coding: utf-8

# # Milestone Project 2 - Walkthrough Steps Workbook
# Below is a set of steps for you to follow to try to create the Blackjack Milestone Project game!

# ## Game Play
# To play a hand of Blackjack the following steps must be followed:
# 1. Create a deck of 52 cards
# 2. Shuffle the deck
# 3. Ask the Player for their bet
# 4. Make sure that the Player's bet does not exceed their available chips
# 5. Deal two cards to the Dealer and two cards to the Player
# 6. Show only one of the Dealer's cards, the other remains hidden
# 7. Show both of the Player's cards
# 8. Ask the Player if they wish to Hit, and take another card
# 9. If the Player's hand doesn't Bust (go over 21), ask if they'd like to Hit again.
# 10. If a Player Stands, play the Dealer's hand. The dealer will always Hit until the Dealer's value meets or exceeds 17
# 11. Determine the winner and adjust the Player's chips accordingly
# 12. Ask the Player if they'd like to play again

# ## Playing Cards
# A standard deck of playing cards has four suits (Hearts, Diamonds, Spades and Clubs) and thirteen ranks (2 through 10, then the face cards Jack, Queen, King and Ace) for a total of 52 cards per deck. Jacks, Queens and Kings all have a rank of 10. Aces have a rank of either 11 or 1 as needed to reach 21 without busting. As a starting point in your program, you may want to assign variables to store a list of suits, ranks, and then use a dictionary to map ranks to values.

# ## The Game
# ### Imports and Global Variables
# ** Step 1: Import the random module. This will be used to shuffle the deck prior to dealing. Then, declare variables to store suits, ranks and values. You can develop your own system, or copy ours below. Finally, declare a Boolean value to be used to control <code>while</code> loops. This is a common practice used to control the flow of the game.**
# 
#     suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
#     ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
#     values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
#              'Queen':10, 'King':10, 'Ace':11}

# In[1]:


import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True


# ### Class Definitions
# Consider making a Card class where each Card object has a suit and a rank, then a Deck class to hold all 52 Card objects, and can be shuffled, and finally a Hand class that holds those Cards that have been dealt to each player from the Deck.

# **Step 2: Create a Card Class**<br>
# A Card object really only needs two attributes: suit and rank. You might add an attribute for "value" - we chose to handle value later when developing our Hand class.<br>In addition to the Card's \_\_init\_\_ method, consider adding a \_\_str\_\_ method that, when asked to print a Card, returns a string in the form "Two of Hearts"

# In[2]:


class Card:
    
    def __init__(self,suits,ranks):
        self.suits = suits
        self.ranks = ranks
    
    def __str__(self):
        return self.ranks + ' of ' + self.suits


# **Step 3: Create a Deck Class**<br>
# Here we might store 52 card objects in a list that can later be shuffled. First, though, we need to *instantiate* all 52 unique card objects and add them to our list. So long as the Card class definition appears in our code, we can build Card objects inside our Deck \_\_init\_\_ method. Consider iterating over sequences of suits and ranks to build out each card. This might appear inside a Deck class \_\_init\_\_ method:
# 
#     for suit in suits:
#         for rank in ranks:
# 
# In addition to an \_\_init\_\_ method we'll want to add methods to shuffle our deck, and to deal out cards during gameplay.<br><br>
# OPTIONAL: We may never need to print the contents of the deck during gameplay, but having the ability to see the cards inside it may help troubleshoot any problems that occur during development. With this in mind, consider adding a \_\_str\_\_ method to the class definition.

# In[3]:


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


# TESTING: Just to see that everything works so far, let's see what our Deck looks like!

# In[4]:


test_deck = Deck()
print(test_deck)


# Great! Now let's move on to our Hand class.

# **Step 4: Create a Hand Class**<br>
# In addition to holding Card objects dealt from the Deck, the Hand class may be used to calculate the value of those cards using the values dictionary defined above. It may also need to adjust for the value of Aces when appropriate.

# In[5]:


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
        


# **Step 5: Create a Chips Class**<br>
# In addition to decks of cards and hands, we need to keep track of a Player's starting chips, bets, and ongoing winnings. This could be done using global variables, but in the spirit of object oriented programming, let's make a Chips class instead!

# In[6]:


class Chips:
    
    def __init__(self):
        self.total = 1000  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


# ### Function Defintions
# A lot of steps are going to be repetitive. That's where functions come in! The following steps are guidelines - add or remove functions as needed in your own program.

# **Step 6: Write a function for taking bets**<br>
# Since we're asking the user for an integer value, this would be a good place to use <code>try</code>/<code>except</code>. Remember to check that a Player's bet can be covered by their available chips.

# In[7]:


def take_bet(funds):
    
    while True:
        bet = int(input('Please place your bet: '))
        if bet <= funds:
            return bet
            print("Your bet has been accepted.")
            break
        else:
            print("You do not have enouth chips to bet!")    


# **Step 7: Write a function for taking hits**<br>
# Either player can take hits until they bust. This function will be called during gameplay anytime a Player requests a hit, or a Dealer's hand is less than 17. It should take in Deck and Hand objects as arguments, and deal one card off the deck and add it to the Hand. You may want it to check for aces in the event that a player's hand exceeds 21.

# In[8]:


def hit(deck,hand):
    
    hand.add_card(deck.deal())
    
    if hand.value > 21:
        hand.adjust_for_ace()


# **Step 8: Write a function prompting the Player to Hit or Stand**<br>
# This function should accept the deck and the player's hand as arguments, and assign playing as a global variable.<br>
# If the Player Hits, employ the hit() function above. If the Player Stands, set the playing variable to False - this will control the behavior of a <code>while</code> loop later on in our code.

# In[9]:


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


# **Step 9: Write functions to display cards**<br>
# When the game starts, and after each time Player takes a card, the dealer's first card is hidden and all of Player's cards are visible. At the end of the hand all cards are shown, and you may want to show each hand's total value. Write a function for each of these scenarios.

# In[10]:


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


# **Step 10: Write functions to handle end of game scenarios**<br>
# Remember to pass player's hand, dealer's hand and chips as needed.

# In[11]:


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

# In[14]:


while True:
    # Print an opening statement
    print('Welcome to Blackjack Game \n')

    
    # Create & shuffle the deck, deal two cards to each player

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


# And that's it! Remember, these steps may differ significantly from your own solution. That's OK! Keep working on different sections of your program until you get the desired results. It takes a lot of time and patience! As always, feel free to post questions and comments to the QA Forums.
# # Good job!
