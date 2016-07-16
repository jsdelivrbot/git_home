
# coding: utf-8

# In[1]:

#Problem: Rock, Paper, Scissors
#Group members: S.Wang, Y. Ye, M. Staton, W. Wang


# In[2]:

import random #to access randint()


# In[3]:

def rock_paper_scissors(): #
    
    computer_choices = ["Rock", "Paper", "Scissors"] #initialize the computer choices set
    
    usr_choices = {"r":"Rock", "p":"Paper", "s":"Scissors"} #initialize the user choices set
    
    rounds = 0 #initialize round counter

    usr_wins = 0 #initialize how many rounds user wins
    
    usr_pref = {"r": 1, "p": 1, "s": 1} #initialize user's preference
    
    #define a winning set for the user
    winning_set = [
        ["Rock", "Scissors"],
        ["Paper", "Rock"],
        ["Scissors", "Paper"]
    ]
    
    print "Welcome to the game."
    
    sig = "" #initialize the signal as empty
    
    while sig not in ["y", "n"]:
        
        sig = raw_input("Type [y] to start, or [n] to quit: ").lower() #ask the user if he wants to play
        
        if sig == "n":
            
            print "Bye"
            
            return
        
    while sig == "y":
        
        rounds += 1 #count this round
        
        random_int = random.randint(1, sum(usr_pref.values())) #generate a random float value
        
        computer_index = 0 #initialize the index of computer's choice
        
        #the following code adjust computer's choice according to user's historic moves
        if random_int <= usr_pref["r"]:
            
            computer_index = 1
        
        elif random_int <= usr_pref["r"] + usr_pref["p"]:
            
            computer_index = 2
            
        else:
            
            computer_index = 0
        
        usr_choice = "" #initialize the user's choice as empty
        
        while usr_choice not in ["r", "p", "s"]:
            
            usr_choice = raw_input("Make your choice:\n[r]ock\n[p]aper\n[s]cissors\n").lower()
        
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

        usr_pref[usr_choice] += 1
        
        sig = "" #reset signal
        
        while sig not in ["y", "n"]:
            
            sig = raw_input("Play again? [y]es or [n]o: ").lower()
        
        if sig == "n":
            
            print "You have played ", rounds, " rounds and won ", usr_wins, " of them."
            
            for key, value in usr_pref.items():
                
                print key, value
            
            print "Bye"
            
            return
    


# In[4]:

#let's start the game
rock_paper_scissors()

