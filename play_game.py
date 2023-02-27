#imports the DeckOfCards file which has the Class referenced throughout this code
import DeckOfCards as dc
from numpy.random import rand
import random

#creates a function of the game to loop through.
#Series of if statements with the possible outcomes to the game.
def play_game():
    deck = dc.DeckOfCards()
    
    #The deck is printed, shuffled, and printed again to show proper functionality
    print("Deck before shuffled:\n")
    deck.print_deck()
    print("----------------\n")
    
    deck.shuffle_deck()

    print("Deck after shuffled:\n")    
    deck.print_deck()
    print("----------------\n")
    
    
    #deal two cards to the user
    card = deck.get_card()
    card2 = deck.get_card()
    
    #initialize user score to 0 and dealer score to random number.
    #add values from drawn cards to user's hand.
    score = 0
    dealer_score = random.randint(17, 23)
    
    score += card.val
    score += card2.val
    
    #Shows the user what their cards and score are.
    print("Card number 1 is: ", card.face, "of", card.suit)
    print("Card number 2 is: ", card2.face, "of", card2.suit)
    print("Your score is: ", score, "\n")
    
    if score > 21:
        print("Player busted, dealer wins!")
    
    else:
    # ask user if they would like a "hit" (another card)
        hit = input("would you like a hit? (y or n)\n")
        
        
        #if loop to run through the different possible game outcomes.
        #if the user will continue to have the option to hit as long as their score is <= 21
        if hit == 'y':
            card3 = deck.get_card()
            score += card3.val
            print("\nCard number 3 is: ", card3.face, "of", card3.suit)
            print("Your new score is: ", score, "\n")
            #if the users score is above 21, they bust regardless of the dealer's score
            #If they don't bust, user may take another hit or finish the game.
            if score > 21:
                print("Player busted! Dealer wins!")
            #User choses to hit and receive 4th card. If not, scores are calculated and game end.
            else:
                hit1 = input("would you like another hit? (y or n)\n")
                if hit1 == 'y':
                    card4 = deck.get_card()
                    score += card4.val
                    print("\nCard number 4 is: ", card4.face, "of", card4.suit)
                    print("Your new Score is: ", score, "\n")
                    
                    if score > 21:
                        print("Busted! Dealer wins!\n")
                    #Last card user can receive.
                    else:
                        hit2 = input("would you like another hit? (y or n)\n")
                        if hit2 == 'y':
                            card5 = deck.get_card()
                            score += card5.val
                            print("\nCard number 5 is: ", card5.face, "of", card5.suit)
                            print("Your new Score is: ", score, "\n")
                            
                            if score > 21:
                                print("Busted! Dealer wins!\n")
                            #Automatically win if user's score is less than 21
                            else:
                                print("5 Card Charlie! Congrats you won!")
                                
                        #user doesn't hit and final scores are calculated
                        elif hit2 == 'n':
                            print("Your final score is: ", score)
                            print("The dealer's final score is: ", dealer_score, "\n")
                            
                            if dealer_score > 21:
                                print("Dealer buster, you win!\n")
                            
                            elif score > dealer_score and score < 22:
                                print("Congrats you won!\n")
                            
                            elif dealer_score >= score and dealer_score < 22:
                                print("Dealer won!\n")
                            
                            
                #If the user doesn't hit, final scores are calculated and winner decided
                elif hit1 =='n':
                    print("Your final score is: ", score)
                    print("The dealer's final score is: ", dealer_score, "\n")
                    
                    if dealer_score > 21:
                        print("Dealer busted, you win!")
                    
                    elif score > dealer_score and score < 22:
                        print("Congrats you won!\n")
                    
                    elif dealer_score >= score and dealer_score < 22:
                        print("Dealer won!\n")
            
    
        elif hit =='n':
            #print("Your final score is: ", score)
            print("The dealer's score is: ", dealer_score, "\n")
        
            if dealer_score > 21:
                print("Dealer busted, you win!")
            
            elif score > dealer_score and score < 22:
                print("Your score is higher, you won!\n")
            
            elif dealer_score >= score and score < 22:
                print("Dealer's score is higher, dealer won!\n")
    
        else:
            print("What was that?")

########################

# Starts playing the game
print("Welcome to black Jack!\n")
#The game function from above is played here.
play_game()

while True:
    #The section below lets the player play again if they want to
    play_again = input("Would you like to play again? (y or n)\n")
    #calls the play_game function so the user can play the game again.
    if play_again == 'y':
        play_game()
    #If they select "n" then the game finishes and so does this while loop
    elif play_again == 'n':
        print("Thanks for playing!")
        break
    #If the user selects something other than "y" or "n" then the
    #input prompt is shown again for a correct answer.
    else:
        print("Sorry, please try again")
        continue
