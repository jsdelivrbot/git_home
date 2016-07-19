import re
import random


#--------------------------------------------------
def countdown(n):
    if n <= 0:
        print 'Takeoff!!'   # base case
    else:
        print n
        countdown(n-1)      # recurse case
        #print n * 10

'''
print
print
countdown(5)
print
print
'''

#--------------------------------------------------
def visualize (n):
    space = ' ' * (4 * n)
    print space, 'VIZ: solving', n

    if n <= 0:
        print space, 'VIZ: BASE returning 0' # base case
        return 0
    else:
        recurse = visualize(n - 1)      # recurse case call
        result = n + recurse
        print space, 'VIZ: RECURSE returning', result
        return result

print
print
print visualize(5)
print
print


#--------------------------------------------------
# I am allowing entry of negative numbers.
# This could be changed to match the
# mathematical definition of factorial.
def factorial(num):
    if num <= 0:
        return 1                    # base case

    recurse = factorial(num - 1)    # recurse case
    result = num * recurse
    return result
'''
print
print
print factorial(5)
print factorial(4)
print factorial(3)
print factorial(-5)
print
print
'''

#--------------------------------------------------
def write_file(msg):
    f = open('results.txt', 'a')
    print "WRITE_FILE: Writing to results.txt:", msg
    f.write(msg + "\n")
    f.close()

'''
print
print
write_file("This is a test.")
write_file("Another line.")
write_file("One more.")
print
print
'''

#--------------------------------------------------
def read_write(file_to_read, file_to_write):
    writer = open(file_to_write, 'a')
    with open(file_to_read, 'r') as reader:
        for line in reader:
            writer.write(line)
            print "READ_WRITE: Writing to {}: {}".format(file_to_write, line),
    writer.close()
'''        
print
print
read_write('results.txt', 'results2.txt')
print
print
'''
#--------------------------------------------------
def wordcount():
    words = ['the', 'cat', 'sat', 'on', 'the', 'wall',
             'and', 'the', 'cat', 'sat', 'on', 'the',
             'mat','where','the','rat','usually','sat',
             'and','the','cat','sat','on','the','rat']
    unique_words = str(tuple(set(words)))
    
    while True:
        word = raw_input("WORDCOUNT: Enter 0 or one of these: " + unique_words + ": ").lower()
        if word == "0":
            return
        
        counter = 0
        for item in words:
            if word == item:
                counter += 1
        print
        print "\nWORDCOUNT", counter, word, "\n\n"
        print
'''       
print
print
wordcount()
print
print
'''

#--------------------------------------------------
def indexer():
    words = ['the', 'cat', 'sat', 'on', 'the', 'wall',
             'and', 'the', 'cat', 'sat', 'on', 'the',
             'mat','where','the','rat','usually','sat',
             'and','the','cat','sat','on','the','rat']

    index = {}    
    for item in words:
        if index.has_key(item):
            index[item] += 1
        else:
            index[item] = 1

    for key, val in index.items():
        print "INDEXER:", val, key
'''
print
print
indexer()
print
print
'''
#--------------------------------------------------
def cipher():
    base = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    translate ='GnWkmEJIRQsHLzPSdqVoxfrZbTyOBXhNiwCDcupUYMKgAjlavtFe'

    while True:
        word = raw_input("\n\nCIPHER: Enter 0 to STOP or another word: ")

        if word == '0':
            print 'CIPHER: STOPPING'
            return
        
        if word[0] == '1':
            translate, base = base, translate
            word = word[1:]

        result = ""
        for chr in word:
            result = result + (translate[base.index(chr)])
        print word, "-->", result

'''
print
print
cipher()
print
print
'''

#--------------------------------------------------
def basic_stats(number_list):

    count = len(number_list)
    stats = {}
    
    if count < 2:
        stats["error"] = "List should contain more than one number."

    else:
        number_list.sort()
        total = 0
        for num in number_list:
            total += num
        mean = float(total) / float(count)

        middle = count / 2
        if count % 2 == 0:
            median = float( ( number_list[middle-1] ) + float( number_list[middle] ) ) / 2
        else:
            median = float( number_list[middle] )

        max = number_list[-1]
        min = number_list[0]
        range = max - min

        stats["total"] = total
        stats["mean"] = mean
        stats["median"] = median
        stats["min"] = min
        stats["max"] = max
        stats["range"] = range    

    return "{:15} {:4} {}".format(number_list, "--->", stats)

'''
print
print

number_list = [5]
print basic_stats(number_list)

number_list = [10, 2]
print basic_stats(number_list)

number_list = [5, 4, 3, 2, 1]
print basic_stats(number_list)

print
print
'''

#--------------------------------------------------
def analyze (data_file, results_file):
    writer = open(results_file, 'w')
    with open(data_file, 'r') as reader:
        for line in reader:
            items = re.split(',', line)
            nums = []
            for item in items:
                nums.append(int(item))
            stats = basic_stats(nums)
            writer.write(stats + "\n")
            print "Writing to {}: {}".format(results_file, stats),
    writer.close()
'''        
print
print
analyze('001.txt', '001_stats.txt')
print
print
'''
#--------------------------------------------------
def check_game_status(string, valid_chars_list, guess_list):
    solved = True
    if guess_list:
        print "\n\nHANGMAN:  GUESS", len(guess_list), guess_list, "\n\n"

    for chr in string:
        if chr in valid_chars_list and chr in guess_list:
            print chr.upper(),
        else:
            print "_",
            solved = False
    print "\n\n"
    return solved
#--------------------------------------------------
def new_word(words, words_to_avoid):
    check_limit = len(words)
    counter = 0
    while True:
        counter += 1
        word = random.choice(words)
        if word not in words_to_avoid or counter > check_limit:
            return word
#--------------------------------------------------
def hangman():
    words =  ['SUPERNATURAL', 'HORSE', 'KITTY', "DOG", "NEWSPAPER",
              "PICTURE", "BLUE", "PENGUIN", "KETTLE"]
    guess = ""
    words_to_avoid = []
    
    while guess != "0":
        guess_tries = 0
        solved = False
        guess_list = []

        word = new_word(words, words_to_avoid)
        words_to_avoid.append(word)
        
        check_game_status(word, set(word), guess_list)
        guesses_allowed = len(word) + 3

        while guess != "0":
            guess = raw_input("HANGMAN: Guess a letter or type 0 to stop: ").upper()
            if guess == "0":
                print "HANGMAN: STOPPING"
                return
            
            guess_tries += 1
            guess_list.append(guess)
            solved = check_game_status(word, set(word), guess_list)
            if solved:
                print "\n\nHANGMAN: CONGRATULATIONS!  Try another word.\n\n"
                break
                
            elif guess_tries >= guesses_allowed:
                print "\n\nHANGMAN: SORRY, OUT OF GUESSSES!  Try another word.\n\n"
                break        
        

print
print
hangman()
print
print
#--------------------------------------------------
def palindrome():
    while True:
        word = raw_input("PALINDROME: Enter a word or 0 to stop. ")
        if word == "0":
            break
        
        # word == word[::-1] also works
        if word == ''.join(reversed(word)):
            print "PALINDROME:", word, "IS A PALINDROME!\n\n"
        else:
            print "PALINDROME:", word, "is NOT a palindrome!\n\n"
'''                            
print
print
palindrome()
print
print
'''
#--------------------------------------------------
def check_palindrome(word):
    return word == word[::-1]
#--------------------------------------------------
def odometer():
    for mileage in xrange(0, 1000000):
        if check_palindrome (str(mileage  ).zfill(6)[2:6]) \
        and check_palindrome(str(mileage+1).zfill(6)[1:6]) \
        and check_palindrome(str(mileage+2).zfill(6)[1:5]) \
        and check_palindrome(str(mileage+3).zfill(6)[0:6]):
            print "ODOMETER:", mileage
print
print
odometer()
print
print
#--------------------------------------------------
  

