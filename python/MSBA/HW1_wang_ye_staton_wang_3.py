
# coding: utf-8

# In[1]:

#Problem: The Google of Quotes
#Group members: S. Wang, Y. Ye, M. Staton, W. Wang
#Version 1.1


# In[2]:

#to access math.log(), and regex functions
import math, re
#to access collections.Counter() function which counts the occurence of items in a list
from collections import Counter
#to facilitate timing the script
from time import time


# In[3]:

#start timing
start_time0 = time()


# In[4]:

#make a handle on the file
quotes_file = open("quotes.txt", "r")


# In[5]:

#make an empty list to store the quotes
quote_list = []

#read in one line each time
new_line = quotes_file.readline()

#join the adjacent two lines to make a full quote
while len(new_line) != 0:
    
    str1, str2 = new_line.strip("\r\n"), quotes_file.readline().strip("\r\n")
        
    quote_list.extend([" - ".join([str1, str2])])
    
    new_line = quotes_file.readline()


# In[6]:

#for safety, close the handle. This can also be done with "with open() as handle"
quotes_file.close()


# In[7]:

#this function take one quote and make a list of the unique words in that quote
def words_in_quote(quote):
    
    pattern = "\W+"
    
    word_list = [word.lower() for word in re.split(pattern, quote)]
    
    while "" in word_list:
        
        word_list.remove("")
        
    return word_list


# In[8]:

#define a function to count the occurence of a word in an object which could be a string or list
#this hurts performance.
#tried *.count() function, but it will return "happy".count("appy") returns 1, i.e. it treats string as list
def count_ocur(obj, elem):
    
    count = 0
    
    if type(obj) == list:
        
        for i in range(0, len(obj)):

            if str(obj[i]).lower() == elem.lower():

                count += 1

        return count
    
    elif type(obj) == str:
        
        obj_list = re.split("[^a-zA-Z0-9_]+", obj.lower())
        
        for j in range(0, len(obj_list)):
            
            if obj_list[j] == elem:
                
                count += 1
                
        return count
    
    else:
        
        return 0


# In[9]:

#define a function to create a posting list given a list of full quotes
def postings_list(quotes):
    
    start_time = time()
    
    if type(quotes) != list:
        
        print "This function only takes list arguments."
        
        return {}
    
    postings_list_dict = {}
                
    for pair in [(quote, dict(Counter(words_in_quote(quote)))) for quote in quotes]:
        
        postings_list_dict[pair[0]] = pair[1]
        
    end_time = time()
    
    print end_time - start_time

    return postings_list_dict


# In[10]:

start_time = time()
postings_list_dict = postings_list(quote_list)
end_time = time()
print end_time - start_time


# In[25]:

#define a function to create a reverse posting list given a list of full quotes
def rev_postings_list(quotes):
    
    start_time = time()
    
    if type(quotes) != list:
        
        print "This function only takes list arguments."
        
        return {}
    
    rev_postings_list_dict = {}
    
    words = []
    
    start_time_listcomprehension1 = time()

    [words.extend(words_in_quote(quote)) for quote in quote_list]

    words = Counter(words).keys()
    
    print "[words.extend(words_in_quote(quote)) for quote in quote_list] took", time() - start_time_listcomprehension1, "seconds."

    start_time_forloop = time()
    
    inner_listcomprehension_time = 0
    
    for word in words:
        
        start_time_innerloop = time()

        quote_word_list = [(quote, words_in_quote(quote).count(word)) for quote in quotes]
        
        inner_listcomprehension_time += time() - start_time_innerloop

        rev_postings_list_dict[word] = {}

        for elem in quote_word_list:

            if elem[1] > 0:

                rev_postings_list_dict[word][elem[0]] = elem[1]
                
    print "for loop took:", time() - start_time_listcomprehension1, "seconds."
    
    print "the inner list comprehension took", inner_listcomprehension_time, "seconds in total."
                
    end_time = time()
    
    print end_time - start_time
          
    return rev_postings_list_dict


# In[26]:

#warning: trying printing reverse_postings_list_dict foreshadows disaster!
start_time = time()
reverse_postings_list_dict = rev_postings_list(quote_list)
end_time = time()
print end_time - start_time


# In[13]:

#define a function to create a reverse posting list given a list of full quotes
def rev_postings_list_2(quotes):
    
    start_time = time()
    
    if type(quotes) != list:
        
        print "This function only takes list arguments."
        
        return {}
    
    rev_postings_list_dict = {}
    
    forward_dict = postings_list(quotes)
    
    for quote, word_count in forward_dict.items():
        
        for word, count in word_count.items():
            
            if word not in rev_postings_list_dict:
                
                rev_postings_list_dict[word] = {}
                
                rev_postings_list_dict[word][quote] = count
                
            else:
                
                rev_postings_list_dict[word][quote] = count
                
    end_time = time()
    
    print end_time - start_time
          
    return rev_postings_list_dict


# In[14]:

#warning: trying printing reverse_postings_list_dict foreshadows disaster!
start_time = time()
reverse_postings_list_dict = rev_postings_list_2(quote_list)
end_time = time()
print end_time - start_time


# In[15]:

#this function take a tuple of (quote, word) and returns the TF_IDF index of word in quote
def tf_idf((quote, word)):
    
    word = str(word).lower()
    
    if quote not in postings_list_dict:
        
        print "The quote is not found."
        
        return 0
    
    if word not in reverse_postings_list_dict:
                
        print "The word is not found."
        
        return 0
    
    max_ocur_in_quote = max([value for (key, value) in postings_list_dict[quote].items() ])
        
    TF = float(count_ocur(quote, word)) / max_ocur_in_quote
        
    N = len(quote_list)
        
    n = len([(key, value) for (key, value) in reverse_postings_list_dict[word].items() if value > 0])
        
    IDF = math.log(float(N/n))
        
    TF_IDF = TF * IDF
        
    return TF_IDF


# In[16]:

tf_idf(("We are all worms, but I do believe I am a glow-worm. - Winston Churchill", "we"))


# In[17]:

#print TF_IDF index of "entertainer" in the Marlon Brando quote to verify the result
start_time = time()
print tf_idf((quote_list[16], "entertainer"))
end_time = time()
print end_time - start_time


# In[18]:

#define a function to search a single word in all quotes
def sg_word_search(default_word=""):
    
    if len(default_word) == 0:
        
        word = ""

        while len(word) == 0:

            word = str(raw_input("Type in a word to search, or \"!!!\" to quit: ")).lower().strip()

            if word == "!!!":

                print "See you next time."

                return {}
            
    else:
        
        word = default_word
        
    search_dict = {}
    
    if word not in reverse_postings_list_dict:
        
        print word, "is not found."
        
        return {}
        
    retrieved_quotes = [key for (key, value) in reverse_postings_list_dict[word].items() if value > 0]
    
    for quote in retrieved_quotes:
        
        search_dict[quote] = tf_idf((quote, word))
        
        #print word, " in ", quote, word in quote
    
    return search_dict


# In[19]:

#this function takes a list of words and return all the quotes containing any of the words
#and shows the sum of the TF_IDF index of every word in every quote 
def mul_word_search():
    
    words = []
    
    while True:
        
        if len(words) == 0:
            
            text = str(raw_input("Type one word and Enter\n\"!!!\" >>> quit\n:")).lower().strip()
        
        else:
            
            text = str(raw_input("Type one word and Enter\n\"???\" >>> start searching\n\"!!!\" >>> quit\n:")).lower().strip()
        
        if text == "!!!":
            
            print "See you next time."
            
            return {}           
        
        if text == "???" and len(words) > 0:
            
            break
        
        else:
            
            words.extend(text)
            
            continue
            
    while "" in words:
        
        words.remove("")
        
    words = [str(s).lower() for s in words]
    
    search_dict2 = {}
    
    retrieved_quotes2_unmerged = map(sg_word_search, words)
    
    retrieved_quotes2_merged = []
    
    for i in range(0, len(retrieved_quotes2_unmerged)):
        
        retrieved_quotes2_merged += retrieved_quotes2_unmerged[i]
    
    retrieved_quotes2_unique = Counter(retrieved_quotes2_merged).keys()
        
    for quote in retrieved_quotes2_unique:
        
        new_params = [(quote, word) for word in words]
        
        search_dict2[quote] = sum(map(tf_idf, new_params))
        
    return search_dict2


# In[20]:

#print out a sample result of calling sg_word_search on keyword "and"
#check the length of the returned list to verify the result
start_time = time()
len(sg_word_search())
end_time = time()
print end_time - start_time


# In[21]:

#print out the result of mul_word_search
start_time = time()
print mul_word_search()
end_time = time()
print end_time - start_time


# In[22]:

#stop timing and print out total running time
end_time0 = time()

print "Total running time", end_time0 - start_time0, "seconds"

