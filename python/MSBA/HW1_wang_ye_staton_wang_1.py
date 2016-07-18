
# coding: utf-8

# In[ ]:

#Problem: Rock, Paper, Scissors
#Group members: S.Wang, Y. Ye, M. Staton, W. Wang


# In[ ]:

import random #to access randint()


# In[ ]:

def rock_paper_scissors(): #
    
    computer_choices = ["Rock", "Paper", "Scissors"] #initialize the computer choices set
    
    usr_choices = {"r":"Rock", "p":"Paper", "s":"Scissors"} #initialize the user choices set
    
    rounds = 0 #initialize round counter

    usr_wins = 0 #initialize how many rounds user wins
    
    computer_wins = 0 #initialize how many rounds computer wins
    
    usr_pref = {"r": 1, "p": 1, "s": 1} #initialize user's preference, adjust the values to tune bias-variance
    
    #define a winning set for the user
    winning_set = [
        ["Rock", "Scissors"],
        ["Paper", "Rock"],
        ["Scissors", "Paper"]
    ]
    
    print "Welcome to the game."
    
    while True:
        
        rounds += 1 #count this round
        
        random_int = random.randint(0, sum(usr_pref.values())) #generate a random float value
        
        computer_index = 0 #initialize the index of computer's choice
        
        #the following code adjust computer's choice according to user's historic moves
        if random_int <= usr_pref["r"]:
            
            computer_index = 1
        
        elif random_int <= usr_pref["r"] + usr_pref["p"]:
            
            computer_index = 2
            
        else:
            
            computer_index = 0
            
        usr_choice = "" #initialize the user's choice as empty
        
        while usr_choice not in ["r", "p", "s", "q"]:
            
            usr_choice = raw_input("Make your choice\n[r]ock\n[p]aper\n[s]cissors\n[q]uit\n:").lower()
            
        if usr_choice == "q":
            
            print "Total rounds: ", rounds
            print "You >>> ", usr_wins, " : ", computer_wins, " <<< Computer"
            print "Draws: ", rounds - usr_wins - computer_wins
            
            for key, value in usr_pref.items():
                
                print key, value
            
            print "Bye"
            
            return
        
        computer_move = computer_choices[computer_index]
        
        usr_move = usr_choices[usr_choice]
        
        print "Your move -> ", usr_move, ":", computer_move, " <- Computer's move"
        
        if [usr_move, computer_move] in winning_set:
            
            print "Congrats, you won!"
            
            usr_wins += 1
            
        elif usr_move == computer_move:
            
            print "Almost."
            
        else:
            
            print "Sorry mate, not today."
            
            computer_wins += 1

        usr_pref[usr_choice] += 1     
        
    return
    


# In[ ]:

#let's start the game
rock_paper_scissors()

