def visualize(num):
    if num <= 0:
        return 0
    else:
        return num + visualize(num - 1)

#print visualize(5), visualize(10), visualize(-1)

def factorial(num):
    if num <= 1:
        return 1
    else:
        return num * factorial(num - 1)

#print factorial(5), factorial(4), factorial(3)

def write_file():
    msg = raw_input("Type in message:")
    f = open("message.txt", "a")
    f.write(msg + "\n")
    f.close()

#write_file()

def read_write(file_to_read, file_to_write):
    with open(file_to_read, "r") as f:
        with open(file_to_write, "a") as g:
            g.write(f.read())
        
#read_write("message.txt", "copy.txt")

def wordcount(lst):
    rank = {}
    for word in lst:
        rank[word] = lst.count(word)

    while len(rank) > 0:
        for key in rank:
            if rank[key] == max(rank.values()):
                print key, rank[key]
                rank.pop(key)
                break

lst = ['the', 'cat', 'sat', 'on', 'the', 'wall', 'and', 'the', 'cat',\
'sat', 'on', 'the', 'mat', 'where', 'the', 'rat', 'usually', 'sat',\
'and', 'the', 'cat', 'sat', 'on', 'the', 'rat']
#wordcount(lst)

def indexer():

    print lst

    usr_input = raw_input("What are you looking for: ")
    
    if usr_input.lower() == "stop":
        return False

    elif lst.count(usr_input) == 0:
        print "It's not here."
        return False

    else:
        index_lst = []
        for i in range(0, len(lst)):
            if lst[i] == usr_input:
                index_lst.append(i)
        print index_lst
        return True

#indexer()
import re
def analyze(data_file, results_file):
    f = open(data_file, "r")
    g = open(results_file, "a")
    for line in f:
        numbers = re.split(",|\n", line)
        for i in range(0, len(numbers)):
            if len(numbers[i]) == 0:
                numbers.pop(i)
            else:
                numbers[i] = int(numbers[i])
        numbers.sort()
        minimum = min(numbers)
        maximum = max(numbers)
        median = numbers[(len(numbers)+1)/2] if len(numbers) % 2 ==0 else\
        (numbers[len(numbers)/2] + numbers[len(numbers)/2+1]) / 2
        local_range = maximum - minimum
        total = sum(numbers)
        mean = float(total / len(numbers))
        result = {"min": minimum, "max": maximum, "median": median, "range": local_range, "total": total,\
            "mean": mean}
        g.write(str(result) + "\n")
    f.close()
    g.close()

#analyze("data.txt", "copy.txt")

import random

def hangman():
    word_list = ["fantastic", "bombardment", "knowledge"]
    random_index = random.randint(0, 2)
    word = word_list[random_index]
    mask = ["-"] * len(word)
    count = len(word) + 3
    
    for letter in mask:
        print letter,

    print "\nHave a try, you have {} chances to guess it.\n".format(count)

    while count > 0:
        character = ""
        while len(character) != 1:
            character = (raw_input("Make a guess: ")).lower()

        for i in range(0, len(word)):
            if word[i] == character:
                mask[i] = word[i]
        
        for letter in mask:
            print letter,

        print "\n"

        if "".join(mask) == word:
            print "You've got it!"
            break

        count -= 1

    else:
        print "Sorry, almost.\nThe word is {}.".format(word)

#hangman()

def palindrome(word):
    word = word.lower()
    for i in range(0, len(word)/2):
        if word[i] != word[len(word)-i-1]:
            #print "It is not a palindrome."
            return False
    else:
        #print "It is a palindrome."
        return True

#palindrome()

def odometer():
    for i in range(0, 10**6-2):
        num = "{:0>6}".format(i)
        num_1 = "{:0>6}".format(i+1)
        num_2 = "{:0>6}".format(i+2)
        if palindrome(num[2:]) and palindrome(num_1[1:])\
        and palindrome(num_2):
            print i
    
odometer()
